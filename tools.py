import datetime
import os
import re

from scrape import scrape_url
from log import agent_logger
from ddgs import DDGS


def get_current_datetime():
    """Returns highly precise temporal string for model grounding."""
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y | %H:%M:%S")


def perform_web_search(query: str, max_results=5):
    """Executes live web search and deep-reads the top result."""
    agent_logger.info(f"External Search Triggered: '{query}'")
    
    try:
        results = []
        with DDGS() as ddgs:
            ddgs_results = list(ddgs.text(query, max_results=max_results))
            
            for index, r in enumerate(ddgs_results):
                if index == 0:
                    full_text = scrape_url(r['href'], max_chars=2500)
                    results.append(f"--- TOP RESULT (FULL TEXT) ---\nSOURCE: {r['href']}\nCONTENT:\n{full_text}\n---------------------------")
                else:
                    results.append(f"SOURCE: {r['href']}\nSNIPPET: {r['body']}")
        
        if not results:
            agent_logger.warning(f"No results found for query: {query}")
            return "No relevant web data found."
            
        return "\n\n".join(results)
        
    except Exception as e:
        agent_logger.error(f"DDGS Search Error: {str(e)}")
        return f"Error connecting to search engine: {str(e)}"


def save_to_file(content: str, prompt_as_filename: str):
    """Saves text content to file named after the prompt."""
    try:
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        clean_name = re.sub(r'[^\w\s-]', '', prompt_as_filename).strip().replace(' ', '_')
        truncated_name = clean_name[:50] if len(clean_name) > 50 else clean_name
        
        if not truncated_name:
            truncated_name = "agent_output"

        file_path = os.path.join(output_dir, f"{truncated_name}.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        agent_logger.info(f"Successfully exported research to: {file_path}")
        return file_path
    except Exception as e:
        agent_logger.error(f"Failed to save file: {str(e)}")
        return None


def apply_formatting_filter(text: str, target_format: str):
    """Formats text into bullets, numbers, or paragraphs."""
    clean_text = text.split("</think>")[-1].strip() if "</think>" in text else text.strip()
    lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
    
    strip_pattern = r'^[\d\.\-\*\s]+'

    if target_format == "bullets":
        formatted_lines = []
        for line in lines:
            content = re.sub(strip_pattern, '', line).strip()
            formatted_lines.append(f"- {content}")
        return "\n".join(formatted_lines)
    
    if target_format == "numbers":
        formatted_lines = []
        for i, line in enumerate(lines):
            content = re.sub(strip_pattern, '', line).strip()
            formatted_lines.append(f"{i+1}. {content}")
        return "\n".join(formatted_lines)
    
    if target_format == "clean":
        paragraph = " ".join(lines)
        return re.sub(r'[\*\#\_\[\]\(\)]', '', paragraph)

    return clean_text
