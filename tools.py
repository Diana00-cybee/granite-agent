import datetime
import os
import re

from validation import is_url_accessible
from scrape import scrape_url
from log import agent_logger
from ddgs import DDGS


def get_current_datetime():
    """Returns highly precise temporal string for model grounding."""
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y | %H:%M:%S")


def perform_web_search(query: str, max_results=5, trusted_sites=None):
    """Executes live web search and sanitizes the user prompt. """
    commands_to_remove = [
        "search", "save", "whitelist", "markdown", "bullet point", "numbered", "clean", "plain text", 
        "summary", "briefly", "paragraph", "no more than one sentence", "no more than three sentences", 
        "no more than five sentences", "no more than ten sentences"
    ]
    
    clean_query = query.lower()
    for cmd in commands_to_remove:
        clean_query = re.sub(rf'\b{cmd}\b', '', clean_query, flags=re.IGNORECASE)
    
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
                    agent_logger.warning("Strict search failed. Preparing fallback.")
                    ddgs_results = []
            
            if not ddgs_results:
                agent_logger.info(f"Broad Search Triggered: '{clean_query}'")
                ddgs_results = list(ddgs.text(clean_query, max_results=max_results))
                
        results = []
        has_deep_context = False
        
        for i, r in enumerate(ddgs_results):
            if not is_url_accessible(r['href']):
                agent_logger.warning(f"Skipping dead link: {r['href']}")
                continue

            if not has_deep_context:
                full_text = scrape_url(r['href'], max_chars=2500)
                
                if "[ERROR:" not in full_text and "[Content blocked" not in full_text:
                    results.append(
                        f"--- VALIDATED DEEP CONTEXT ---\n"
                        f"SOURCE: {r['href']}\n"
                        f"CONTENT:\n{full_text}\n"
                        f"---------------------------"
                    )
                    has_deep_context = True
                    agent_logger.info(f"Successfully validated deep context from: {r['href']}")
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
            
        agent_logger.info(f"Successfully exported research to: {file_path}")
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


