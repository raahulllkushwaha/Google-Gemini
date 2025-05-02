import google.generativeai as genai
import os
import sys
import time
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal text
init()

def load_api_key():
    """Load and validate the API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(f"{Fore.RED}Error: GEMINI_API_KEY not found in environment.{Style.RESET_ALL}")
        print("Please create a .env file with your API key: GEMINI_API_KEY=your_key_here")
        sys.exit(1)
    return api_key

def initialize_chat(model_name="gemini-2.0-flash"):
    """Initialize the Gemini chat with the specified model."""
    try:
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat(history=[])
        return chat
    except Exception as e:
        print(f"{Fore.RED}Error initializing Gemini model: {e}{Style.RESET_ALL}")
        sys.exit(1)

def typing_effect(text):
    """Display text with a typing effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.005)  # Adjust speed as needed
    print()

def display_welcome():
    """Display a welcome message."""
    welcome_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════╗
║               GEMINI CHATBOT                     ║
╚══════════════════════════════════════════════════╝{Style.RESET_ALL}

Welcome! You're now chatting with Google's Gemini AI.
Type your messages below and press Enter to send.
Type {Fore.YELLOW}'exit', 'quit', or 'bye'{Style.RESET_ALL} to end the conversation.
Type {Fore.YELLOW}'clear'{Style.RESET_ALL} to clear the conversation history.
"""
    print(welcome_text)

def main():
    """Main function to run the chatbot."""
    api_key = load_api_key()
    genai.configure(api_key=api_key)
    
    display_welcome()
    
    chat = initialize_chat()
    conversation_active = True
    
    while conversation_active:
        try:
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
            
            # Handle special commands
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"{Fore.CYAN}Goodbye! Thanks for chatting.{Style.RESET_ALL}")
                break
            elif user_input.lower() == "clear":
                chat = initialize_chat()
                print(f"{Fore.YELLOW}Conversation history cleared.{Style.RESET_ALL}")
                continue
            elif not user_input.strip():
                continue
                
            # Display "typing" indicator
            print(f"{Fore.BLUE}Gemini is thinking...{Style.RESET_ALL}", end="\r")
            
            # Get response from Gemini
            response = chat.send_message(user_input)
            
            # Clear the "thinking" indicator
            print(" " * 25, end="\r")
            
            # Display the response with typing effect
            print(f"{Fore.BLUE}Gemini: {Style.RESET_ALL}", end="")
            typing_effect(response.text if response.text else "No response.")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Conversation terminated by user.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            print("Let's continue our conversation...")

if __name__ == "__main__":
    main()