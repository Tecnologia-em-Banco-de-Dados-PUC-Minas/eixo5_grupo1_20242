from dotenv import load_dotenv
import os


load_dotenv(".ENV")
openai_api_key = os.environ.get("OPENAI_API_KEY")

print(openai_api_key)
