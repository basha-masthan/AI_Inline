import os
import sys
import subprocess

# Check and install dependencies if missing
def check_dependencies():
    required = ["openai", "python-dotenv", "colorama"]
    missing = []
    for package in required:
        try:
            if package == "python-dotenv":
                import dotenv
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("Dependencies installed successfully!\n")
        except Exception as e:
            print(f"Failed to install dependencies: {e}")
            print("Please run: pip install openai python-dotenv colorama")
            sys.exit(1)

check_dependencies()

from openai import OpenAI
from dotenv import load_dotenv
from colorama import init, Fore, Style


# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

def setup_config():
    """Interactive wizard to create .env file if it's missing."""
    print(Fore.CYAN + "------------------------------------------")
    print(Fore.CYAN + "      INITIAL CONFIGURATION SETUP")
    print(Fore.CYAN + "------------------------------------------" + Style.RESET_ALL)
    
    token = input(f"[{Fore.GREEN}INPUT{Style.RESET_ALL}] Enter your GitHub Token: ").strip()
    
    print(f"\n{Fore.YELLOW}Select preferred AI model:{Style.RESET_ALL}")
    models = {
        "1": ("gpt-4o", "Standard"),
        "2": ("gpt-4o-mini", "Faster"),
        "3": ("o1-preview", "Advanced Reasoning"),
        "4": ("o1-mini", "Advanced Reasoning Small"),
        "5": ("meta-llama-3.1-70b-instruct", "Llama-3-70b")
    }
    
    for key, (name, desc) in models.items():
        print(f"  {key}] {name} ({desc})")
    
    choice = input(f"[{Fore.GREEN}INPUT{Style.RESET_ALL}] Select model (1-5) [1]: ").strip() or "1"
    model_name = models.get(choice, models["1"])[0]

    with open(".env", "w") as f:
        f.write("# GitHub AI Assistant Config\n")
        f.write(f"GITHUB_TOKEN={token}\n")
        f.write(f"MODEL_NAME={model_name}\n")
    
    print(f"\n{Fore.GREEN}[SUCCESS] .env file created successfully!{Style.RESET_ALL}")
    print(Fore.CYAN + "------------------------------------------\n" + Style.RESET_ALL)
    
    # Reload environment variables
    load_dotenv()
    return token, model_name

def main():
    # Load environment variables from .env file
    load_dotenv()

    token = os.getenv("GITHUB_TOKEN")
    model = os.getenv("MODEL_NAME", "gpt-4o")

    # If token is missing, run the setup wizard
    if not token:
        token, model = setup_config()

    if not token:
        print(Fore.RED + "Error: GITHUB_TOKEN is required to run the assistant.")
        sys.exit(1)

    # Initialize the OpenAI client pointing to GitHub Models API
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=token,
    )


    print(Style.BRIGHT + Fore.CYAN + "=== GitHub AI Terminal Assistant ===")
    print(Fore.YELLOW + f"Using model: {model}")
    print(Fore.GREEN + "Type 'exit' or 'quit' to end the session.\n")

    chat_history = [
        {"role": "system", "content": "You are a helpful coding assistant running in a terminal."}
    ]

    while True:
        try:
            # Get user input
            user_input = input(Fore.BLUE + Style.BRIGHT + "You: " + Style.RESET_ALL)
            
            if user_input.lower() in ['exit', 'quit']:
                print(Fore.CYAN + "Goodbye!")
                break

            if not user_input.strip():
                continue

            # Add user message to history
            chat_history.append({"role": "user", "content": user_input})

            # Call the GitHub Models API
            print(Fore.MAGENTA + "AI is thinking..." + Style.RESET_ALL, end="\r")
            
            response = client.chat.completions.create(
                messages=chat_history,
                model=model,
                temperature=0.7,
                max_tokens=2048
            )

            # Get the assistant message
            assistant_message = response.choices[0].message.content
            
            # Print assistant message with formatting
            print(" " * 20, end="\r") # Clear the thinking line
            print(Fore.GREEN + Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
            print(assistant_message)
            print("-" * 40)

            # Add assistant message to history
            chat_history.append({"role": "assistant", "content": assistant_message})

        except KeyboardInterrupt:
            print(Fore.CYAN + "\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            print(Fore.RED + f"\nAn error occurred: {e}")
            break

if __name__ == "__main__":
    main()
