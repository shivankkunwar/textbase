from textbase import bot, Message
from textbase.models import OpenAI
from typing import List

# Load your OpenAI API key
OpenAI.api_key = ""

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI language learning assistant. You can practice and learn a new language with me. 
I can provide vocabulary, quizzes, and even engage in conversations in your chosen language. 
Feel free to ask for vocabulary, grammar tips, or start a conversation to practice.
"""

@bot()
def on_message(message_history: List[Message], state: dict = None):

    try:
     # Extract user's message
        user_message = message_history[-1]['content']
        print(user_message)
        # Check if the user is asking for language learning content
        if "vocabulary" in user_message[0]['value'].lower():
            # Provide a vocabulary word and its translation
            bot_response = OpenAI.generate(
            system_prompt="Generate a new vocabulary word and its translation.",
            model="gpt-3.5-turbo",
            )
            response_text = bot_response
        elif "quiz" in user_message[0]['value'].lower():
            # Generate a language quiz question
            bot_response = OpenAI.generate(
            system_prompt="Generate a language quiz question.",
            model="gpt-3.5-turbo",
            )
            response_text = bot_response
        else:
            # Generate a natural language response
            bot_response = OpenAI.generate(
                system_prompt=SYSTEM_PROMPT,
                message_history=message_history,  # Assuming history is the list of user messages
                model="gpt-3.5-turbo",
            )
            response_text = bot_response

        response = {
            "data": {
                "messages": [
                    {
                        "data_type": "STRING",
                        "value": response_text
                    }
                ],
                "state": state
            },
            "errors": [
                {
                    "message": ""
                }
            ]
        }
    except Exception as e:
        # Handle exceptions and provide an error response
        response = {
            "data": {
                "messages": [
                    {
                        "data_type": "STRING",
                        "value": f"An error occurred: {str(e)}"
                    }
                ],
                "state": state
            },
            "errors": [
                {
                    "message": str(e)
                }
            ]
        }

    return {
        "status_code": 200,
        "response": response
    }