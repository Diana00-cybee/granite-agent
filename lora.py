import sys

from log import agent_logger


try:
    from peft import PeftModel
except ImportError:
    agent_logger.error("The 'peft' library is required to load LoRA adapters.")
    agent_logger.error("Please install it via: pip install peft")
    sys.exit(1)


def apply_lora_adapter(base_model, lora_repo_id: str):
    """Wraps the base model with LoRA adapter."""
    if not lora_repo_id or str(lora_repo_id).strip().lower() == "none":
        agent_logger.debug("No LoRA adapter specified. Proceeding with base model.")
        return base_model

    agent_logger.info(f"Fetching and applying LoRA adapter from HF: {lora_repo_id}...")
    
    try:
        model_with_lora = PeftModel.from_pretrained(base_model, lora_repo_id)
        agent_logger.info(f"LoRA adapter '{lora_repo_id}' successfully fused to the base engine.")
        return model_with_lora
        
    except Exception as e:
        agent_logger.error(f"FATAL LORA ERROR: Could not load adapter '{lora_repo_id}'.")
        agent_logger.error(f"Details: {str(e)}")
        agent_logger.warning("Reverting to the standard base model to maintain execution.")
        return base_model
