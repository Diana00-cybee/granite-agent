# cli.py
import argparse
import sys
import logging

from main import initialize_engine, execute_single_task, load_config
from log import agent_logger


class Colors:
    SYSTEM = '\033[95m'       
    USER = '\033[92m'         
    AGENT = '\033[97m'        
    WARNING = '\033[93m'      
    ERROR = '\033[91m'        
    RESET = '\033[0m'         
    BOLD = '\033[1m'


def print_colored(text: str, color: str, end: str = "\n"):
    """Helper to print text in a specific color."""
    sys.stdout.write(f"{color}{text}{Colors.RESET}{end}")
    sys.stdout.flush()


def parse_args():
    parser = argparse.ArgumentParser(description="Granite Agent")
    parser.add_argument(
        "-c", "--config", 
        type=str, 
        default="config.yaml",
        help="Path to the YAML configuration file."
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Enable verbose debugging output in the console."
    )
    return parser.parse_args()


def run_cli():
    args = parse_args()

    if args.verbose:
        agent_logger.setLevel(logging.DEBUG)
        print_colored("[SYSTEM] Verbose mode enabled.", Colors.SYSTEM)

    print_colored(f"{Colors.BOLD}[SYSTEM] Booting Granite-3.3-2B Engine...{Colors.RESET}", Colors.SYSTEM)
    config = load_config(args.config)
    tokenizer, model = initialize_engine()

    system_prompt = config['agent_config']['prompts']['system_prompt']
    history = [{"role": "system", "content": system_prompt}]

    print_colored(f"\n{Colors.BOLD}--- Granite Agent ---{Colors.RESET}", Colors.AGENT)
    print_colored("Type 'exit' or 'quit' to stop.\n", Colors.SYSTEM)

    while True:
        try:
            user_in = input(f"{Colors.BOLD}{Colors.USER}User: {Colors.RESET}")
            
            if user_in.lower() in ['exit', 'quit']:
                print_colored("\n[SYSTEM] Shutting down agent. Goodbye!", Colors.SYSTEM)
                break
            
            if not user_in.strip():
                continue

            sys.stdout.write(f"{Colors.AGENT}{Colors.BOLD}Agent: {Colors.RESET}{Colors.AGENT}")
            sys.stdout.flush()

            execute_single_task(user_in, tokenizer, model, history)
            
            sys.stdout.write(Colors.RESET + "\n")

        except KeyboardInterrupt:
            print_colored("\n[SYSTEM] Interrupted by user. Shutting down.", Colors.WARNING)
            break
        except Exception as e:
            print_colored(f"\n[CRITICAL ERROR] {str(e)}", Colors.ERROR)


if __name__ == "__main__":
    run_cli()
