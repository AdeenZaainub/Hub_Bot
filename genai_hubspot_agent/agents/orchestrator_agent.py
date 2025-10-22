# orchestrator_agent.py
import json
from hubspot_tools import create_contact_tool, update_contact_tool, create_deal_tool, hubspot_client
from email_agent import EmailAgent
from groq_agent import get_response_from_lama

# Initialize Email Agent
# -----------------------------
email_agent = EmailAgent()

# -----------------------------
# Tools mapping
# -----------------------------
tools_map = {
    "create_contact": create_contact_tool,
    "update_contact": update_contact_tool,
    "create_deal": create_deal_tool
}

# -----------------------------
# Helper functions
# -----------------------------
def extract_json(text) -> str:
    """Extract JSON part safely from text output."""
    if isinstance(text, dict):
        return json.dumps(text)  # Already a dict, convert to string
    elif isinstance(text, str):
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start:end+1]
    return "{}"

def map_payload_to_tool_input(payload: dict) -> dict:
    """Map Groq dynamic payload to StructuredTool input."""
    action = payload.get("action")
    params = payload.get("params", {})

    if action == "create_contact":
        return {
            "email": params.get("email"),
            "first_name": params.get("first_name") or params.get("name"),
            "last_name": params.get("last_name")
        }

    elif action == "update_contact":
        return {
            "contact_id": params.get("contact_id"),
            "updates": params.get("updates")
        }

    elif action == "create_deal":
        contact_email = params.get("email")
        contact = hubspot_client.get_contact_by_email(contact_email) if contact_email else None
        return {
            "deal_name": params.get("name") or params.get("deal_name"),
            "amount": params.get("amount"),
            "associated_contact_id": contact["id"] if contact else None
        }

    return params

def send_confirmation_email(payload: dict, result: dict):
    """Send email confirming HubSpot action."""
    email = payload.get("params", {}).get("email", "adeenzainub@gmail.com")
    subject = f"HubSpot Action Completed: {payload.get('action')}"
    body = f"The following action has been performed:\n\n{json.dumps(result, indent=2)}"
    email_agent.send_email(email, subject, body)

# -----------------------------
# Main Orchestrator

def orchestrator():
    print("-------Global Orchestrator Agent-----------\n")
    while True:
        user_query = input(" Enter your query (or write exit ): ").strip()
        if user_query.lower() == "exit":
            print("Thanks for using me . Bye!")
            break

        try:
            # 1️ Get dynamic structured payload from Groq
            groq_response = get_response_from_lama(user_query)
            payload = json.loads(extract_json(groq_response))

            action = payload.get("action")
            if not action or action not in tools_map:
                print(f"Error: Unknown action '{action}' or failed to parse Groq response.")
                continue

            #  Map dynamic payload to tool input
            tool_input = map_payload_to_tool_input(payload)

            #  Execute corresponding tool
            tool = tools_map[action]
            result = tool.invoke(tool_input)

            # Send confirmation email
            send_confirmation_email(payload, result)

            print("✅ Result:\n", json.dumps(result, indent=2))

        except json.JSONDecodeError:
            print("Error: Failed to parse query from Groq output.")
        except Exception as e:
            print(f"Error: {e}")


# Run orchestrator
# -----------------------------
if __name__ == "__main__":
    orchestrator()
