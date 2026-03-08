import datetime
import zoneinfo
import torch
import os
import re
import gc

from transformers import AutoProcessor, AutoModelForImageTextToText, BitsAndBytesConfig
from docling.document_converter import DocumentConverter

from validation import is_url_accessible
from scrape import scrape_url
from log import agent_logger
from ddgs import DDGS
from PIL import Image


def get_current_datetime():
    """Returns the current system time."""
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y | %H:%M:%S")


def get_world_clock():
    """Returns the current time across global timezones."""
    zones = {
        "Helsinki (Local)": "Europe/Helsinki",
        "New York (EST/EDT)": "America/New_York",
        "London (GMT/BST)": "Europe/London",
        "Tokyo (JST)": "Asia/Tokyo",
        "Sydney (AEST)": "Australia/Sydney",
        "UTC": "UTC"
    }
    
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    clock_data = ["--- WORLD CLOCK ---"]
    
    for city, tz_name in zones.items():
        try:
            tz = zoneinfo.ZoneInfo(tz_name)
            local_time = now_utc.astimezone(tz)
            clock_data.append(f"{city}: {local_time.strftime('%A, %b %d | %H:%M')}")
        except Exception as e:
            agent_logger.warning(f"Could not load timezone {tz_name}: {e}")
            continue
            
    clock_data.append("-------------------")
    return "\n".join(clock_data)


def read_local_document(file_path: str):
    """Reads local files using Docling."""
    if not os.path.exists(file_path):
        agent_logger.error(f"Document not found at path: {file_path}")
        return f"[ERROR: File not found at {file_path}]"

    agent_logger.info(f"Preparing to read local document: {file_path}")
    
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.txt', '.md', '.csv', '.log']:
            agent_logger.info(f"Bypassing Docling... Reading raw text file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            formatted_output = (
                f"--- LOCAL DOCUMENT: {os.path.basename(file_path)} ---\n"
                f"CONTENT:\n{content}\n"
                f"---------------------------\n"
            )
            return formatted_output

        agent_logger.info("Initializing Docling for document parsing...")
        converter = DocumentConverter()
        result = converter.convert(file_path)
        markdown_content = result.document.export_to_markdown()
        
        agent_logger.info(f"Document successfully parsed: {file_path}")
        
        formatted_output = (
            f"--- LOCAL DOCUMENT: {os.path.basename(file_path)} ---\n"
            f"CONTENT:\n{markdown_content}\n"
            f"---------------------------\n"
        )
        return formatted_output
        
    except Exception as e:
        agent_logger.error(f"Failed to read document: {str(e)}")
        return f"[ERROR: Failed to read document: {str(e)}]"


def analyze_local_image(image_path: str, user_prompt: str):
    """Loads Granite Vision and processes high-resolution images."""
    if not os.path.exists(image_path):
        agent_logger.error(f"Image not found at path: {image_path}")
        return f"[ERROR: File not found at {image_path}]"

    agent_logger.info(f"Lazy-loading Granite Vision for: {image_path}")
    
    try:
        gc.collect()
        torch.cuda.empty_cache()
        
        model_id = "ibm-granite/granite-vision-3.3-2b"
        processor = AutoProcessor.from_pretrained(model_id)
        
        vision_model = AutoModelForImageTextToText.from_pretrained(
            model_id,
            device_map="auto", 
            torch_dtype=torch.bfloat16, 
            attn_implementation="sdpa"  
        )
        
        image = Image.open(image_path).convert("RGB")
        image.thumbnail((2048, 2048)) 
        
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": "Describe this image in detail and answer the user's implicit request: " + user_prompt},
                ],
            }
        ]
        text_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
        
        inputs = processor(
            images=image,
            text=text_prompt,
            return_tensors="pt"
        ).to("cuda") 
        
        if "pixel_values" in inputs:
            inputs["pixel_values"] = inputs["pixel_values"].to(torch.bfloat16)

        agent_logger.info("Extracting high-resolution visual layout...")
        
        outputs = vision_model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.15,
            do_sample=True
        )
        
        generated_ids = outputs[0, inputs["input_ids"].shape[1]:]
        result_text = processor.decode(generated_ids, skip_special_tokens=True)
        
        formatted_output = (
            f"--- VISION EXTRACTION: {os.path.basename(image_path)} ---\n"
            f"OBSERVATION:\n{result_text.strip()}\n"
            f"---------------------------\n"
        )
        agent_logger.info(f"Vision extraction complete for: {image_path}")
        
    except Exception as e:
        agent_logger.error(f"Vision analysis failed: {str(e)}")
        formatted_output = f"[ERROR: Vision analysis failed: {str(e)}]"
        
    finally:
        agent_logger.info("Unloading Vision Model and running garbage collection...")
        if 'vision_model' in locals():
            del vision_model
        if 'processor' in locals():
            del processor
        if 'inputs' in locals():
            del inputs
        if 'outputs' in locals():
            del outputs
            
        gc.collect()
        torch.cuda.empty_cache()
        agent_logger.info("VRAM flushed... Returning to main text engine.")
        
    return formatted_output


def perform_web_search(query: str, max_results=5, trusted_sites=None):
    """Executes live web search and scrapes primary source."""
    commands_to_remove = [
        "search", "save", "whitelist", "markdown", "bullet point", "numbered", "clean", "paragraph", "no more than one sentence", 
        "no more than three sentences", "no more than five sentences", "no more than ten sentences"
    ]
    
    clean_query = query.lower()
    for cmd in commands_to_remove:
        clean_query = re.sub(rf'\b{cmd}\b', '', clean_query, flags=re.IGNORECASE)
    
    clean_query = re.sub(r'\b[\w-]+\.(pdf|docx|txt|html|pptx|md|log)\b', '', clean_query, flags=re.IGNORECASE)
    clean_query = re.sub(r'[^\w\s-]', '', clean_query).strip()
    
    if not clean_query:
        clean_query = query
        
    agent_logger.info(f"Sanitized query for search engine: '{clean_query}'")

    ddgs_results = []
    
    try:
        with DDGS() as ddgs:
            if trusted_sites:
                safe_sites = trusted_sites[:10] 
                site_operators = " OR ".join([f"site:{domain}" for domain in safe_sites])
                strict_query = f"{clean_query} ({site_operators})"
                
                agent_logger.info("Attempting Strict Media Search...")
                try:
                    ddgs_results = list(ddgs.text(strict_query, max_results=max_results))
                except Exception:
                    agent_logger.warning("Strict search failed... Preparing fallback.")
                    ddgs_results = []
            
            if not ddgs_results:
                agent_logger.info(f"Broad Search Triggered: '{clean_query}'")
                ddgs_results = list(ddgs.text(clean_query, max_results=max_results))
                
        results = []
        has_deep_context = False
        
        for i, r in enumerate(ddgs_results):
            if not has_deep_context:
                if not is_url_accessible(r['href']):
                    agent_logger.warning(f"Skipping dead link: {r['href']}")
                    continue
                    
                full_text = scrape_url(r['href'], max_chars=2500)
                
                if "[ERROR:" not in full_text and "[Content blocked" not in full_text:
                    results.append(
                        f"--- VALIDATED DEEP CONTEXT ---\n"
                        f"SOURCE: {r['href']}\n"
                        f"CONTENT:\n{full_text}\n"
                        f"---------------------------"
                    )
                    has_deep_context = True
                    agent_logger.info(f"Successfully validated context from: {r['href']}")
                    continue 
            
            results.append(f"SOURCE: {r['href']}\nSNIPPET: {r['body']}")
        
        if not results:
            agent_logger.warning(f"No results found for query: {clean_query}")
            return "No relevant web data found."
            
        total_sources = len(results)
        agent_logger.info(f"Total valid sources compiled: {total_sources}")
        
        formatted_results = f"[TOTAL SOURCES COMPILED: {total_sources}]\n\n" + "\n\n".join(results)
        return formatted_results
        
    except Exception as e:
        agent_logger.error(f"DDGS Search Error: {str(e)}")
        return f"Error connecting to search engine: {str(e)}"


def save_to_file(content: str, prompt_as_filename: str, extension=".txt"):
    """Saves text content to file named after the prompt."""
    try:
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        clean_name = re.sub(r'[^\w\s-]', '', prompt_as_filename).strip().replace(' ', '_')
        truncated_name = clean_name[:50] if len(clean_name) > 50 else clean_name
        
        if not truncated_name:
            truncated_name = "agent_output"

        file_path = os.path.join(output_dir, f"{truncated_name}{extension}")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        agent_logger.info(f"Successfully exported data to: {file_path}")
        return file_path
    except Exception as e:
        agent_logger.error(f"Failed to save file: {str(e)}")
        return None


def apply_formatting_filter(text: str, target_format: str):
    """Formats text into bullet, number, paragraph, or markdown."""
    clean_text = text.split("</think>")[-1].strip() if "</think>" in text else text.strip()
    
    if target_format == "markdown":
        md_text = re.sub(r'^(#+)(?=[^\s#])', r'\1 ', clean_text, flags=re.MULTILINE)
        return md_text
        
    lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
    list_marker_pattern = r'^\s*(?:\d+[\.\)]|[*\-+])\s+'

    if target_format == "bullets":
        formatted_lines = []
        for line in lines:
            content = re.sub(list_marker_pattern, '', line).strip()
            formatted_lines.append(f"- {content}")
        return "\n".join(formatted_lines)
    
    if target_format == "numbers":
        formatted_lines = []
        for i, line in enumerate(lines):
            content = re.sub(list_marker_pattern, '', line).strip()
            formatted_lines.append(f"{i+1}. {content}")
        return "\n".join(formatted_lines)
    
    if target_format == "clean":
        clean_lines = [re.sub(list_marker_pattern, '', line).strip() for line in lines]
        paragraph = " ".join(clean_lines)
        paragraph = re.sub(r'(\*\*|\*|__|_|#+)', '', paragraph)
        return re.sub(r'\s+', ' ', paragraph).strip()

    return clean_text
