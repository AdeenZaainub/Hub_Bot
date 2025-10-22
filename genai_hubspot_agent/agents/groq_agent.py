import json
import os
from groq import Groq

# Load config
with open("../config/config.json") as f:
    config = json.load(f)

# Initialize Groq client
os.environ["GROQ_API_KEY"] = config["groq"]["api_key"]
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_response_from_lama(prompt: str, model: str = None) -> dict:
    """
    Sends a user prompt to Groq LLaMA model and returns a strict JSON response.
    """
    if model is None:
        model = config["groq"]["default_model"]

    # Wrap the prompt with instructions to return strict JSON
    structured_prompt = f"""
    You are an assistant that converts user CRM requests into a strict JSON format.
    Respond only with JSON, no extra text or markdown.

    Format strictly as:
    {{
        "action": "<create_contact|update_contact|create_deal|update_deal>",
        "params": {{ ... }}
    }}

    Examples:
    User: Create a contact named Ali with email ali@test.com
    Output: {{"action":"create_contact","params":{{"first_name":"Ali","email":"ali@test.com"}}}}

    User: Update contact sara@test.com set city to Lahore
    Output: {{"action":"update_contact","params":{{"email":"sara@test.com","updates":{{"city":"Lahore"}}}}}}

    Now respond for this user query:
    {prompt}
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": structured_prompt}],
        model=model
    )

    response_text = chat_completion.choices[0].message.content

    try:
        # Attempt to parse JSON strictly
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"error": f"Failed to parse query: {response_text}"}


if __name__ == "__main__":
    user_query = input("💬 Enter your query: ")
    result = get_response_from_lama(user_query)
    print("✅ Structured Response:", json.dumps(result, indent=2))
