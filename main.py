import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("API key not found. Please check the .env file")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

parser = argparse.ArgumentParser(description="AI Agent Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

user_prompt = args.user_prompt

messages = [
    {
        "role": "user", 
        "content": user_prompt
    },
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
)

prompt_tokens = response.usage.prompt_tokens
response_tokents = response.usage.completion_tokens

if response.usage is None:
    raise RuntimeError("Usage object is not available right now. Please check it!")

if args.verbose is True:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokents}")

print(response.choices[0].message.content)