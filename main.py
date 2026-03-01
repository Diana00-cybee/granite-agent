import yaml
import torch
import threading

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TextIteratorStreamer,
    StoppingCriteria,
    StoppingCriteriaList
)

from error import KillSwitchTriggeredError, InsufficientDataError
from tools import get_current_datetime, perform_web_search
from lora import apply_lora_adapter
from log import agent_logger


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

config = load_config()

class ThreadKillSwitch(StoppingCriteria):
    def __init__(self):
        self.halt_generation = False
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        return self.halt_generation

def initialize_engine():
    agent_logger.info("Initializing Granite-3.3-2B engine...")
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"
    )

    tokenizer = AutoTokenizer.from_pretrained(config['agent_config']['model']['repo_id'])
    
    model = AutoModelForCausalLM.from_pretrained(
        config['agent_config']['model']['repo_id'],
        quantization_config=bnb_config,
        device_map="auto",
        attn_implementation="sdpa",
        low_cpu_mem_usage=True,        
        torch_dtype=torch.float16,     
    )
    model.config.max_position_embeddings = 4096
    
    lora_repo = config['agent_config']['model'].get('lora_repo_id', 'none')
    if lora_repo and str(lora_repo).strip().lower() != 'none':
        model = apply_lora_adapter(model, lora_repo)
    
    model.config.max_position_embeddings = 4096
    torch.cuda.empty_cache()                    
    
    return tokenizer, model

def execute_single_task(user_input: str, tokenizer, model, message_history: list):
    if len(message_history) > 9: 
        trimmed_history = [message_history[0]] + message_history[-8:]
        message_history.clear()
        message_history.extend(trimmed_history)
        agent_logger.debug("VRAM Safety: History window rotated.")

    current_time = get_current_datetime()
    search_keywords = config['agent_config']['search_config'].get('keywords', [])
    search_data = ""
    
    if any(kw in user_input.lower() for kw in search_keywords):
        max_res = config['agent_config']['search_config'].get('max_results', 3)
        search_data = perform_web_search(user_input, max_results=max_res)

    grounded_input = (
        f"### Input:\n"
        f"--- DATA CONTEXT ---\n"
        f"SYSTEM_TIME: {current_time}\n"
        f"SEARCH_DATA_TRUTH: {search_data if search_data else 'NO DATA FOUND'}\n"
        f"--- END OF DATA ---\n\n"
        f"TASK: {user_input}\n\n"
        f"### Response:\n<think>\n"
    )

    message_history.append({"role": "user", "content": grounded_input})
    
    full_prompt = ""
    for msg in message_history:
        if msg['role'] == 'system':
            full_prompt += f"### Instruction:\n{msg['content']}\n\n"
        else:
            full_prompt += msg['content']

    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    kill_switch = ThreadKillSwitch()
    
    gen_kwargs = {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"],
        "streamer": streamer,
        "stopping_criteria": StoppingCriteriaList([kill_switch]),
        "max_new_tokens": config['agent_config']['generation']['max_new_tokens'],
        "max_length": 4096,
        "temperature": config['agent_config']['generation']['temperature'],
        "repetition_penalty": config['agent_config']['generation']['repetition_penalty'],
        "do_sample": True,
        "use_cache": True,
        "pad_token_id": tokenizer.eos_token_id
    }

    gen_thread = threading.Thread(target=model.generate, kwargs=gen_kwargs)
    gen_thread.start()

    generated_text = ""
    try:
        generated_text = "<think>\n"
        
        for new_text in streamer:
            generated_text += new_text
            print(new_text, end="", flush=True)
            
            if "User:" in generated_text:
                kill_switch.halt_generation = True 
                raise KillSwitchTriggeredError("User:", generated_text)

        gen_thread.join()
        print() 
        message_history.append({"role": "assistant", "content": generated_text.strip()})
        return generated_text.strip()

    except KillSwitchTriggeredError:
        gen_thread.join() 
        torch.cuda.empty_cache()
        print()
        return "[SYSTEM INTERVENTION: Boundary violation.]"

