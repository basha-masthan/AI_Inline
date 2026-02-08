import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

def main():
    # Load environment variables from .env file
    load_dotenv()

    token = os.getenv("GITHUB_TOKEN")
    model = os.getenv("MODEL_NAME", "gpt-4o")

    if not token:
        print(Fore.RED + "Error: GITHUB_TOKEN not found in environment or .env file.")
        print("Please create a .env file with GITHUB_TOKEN=your_token")
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
