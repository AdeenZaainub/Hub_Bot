# hubspot_agent.py
import json
import os
import requests

# Load configuration
with open(os.path.join(os.path.dirname(__file__), "../config/config.json")) as f:
    config = json.load(f)

class HubSpotAgent:
    def __init__(self):
        self.token = config["hubspot"]["access_token"]
        self.base_url = "https://api.hubapi.com"

    # -----------------------------
    # Create a new contact
    # -----------------------------
    def create_contact(self, email: str, first_name: str = None, last_name: str = None) -> dict:
        url = f"{self.base_url}/crm/v3/objects/contacts"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {"properties": {"email": email}}
        if first_name:
            data["properties"]["firstname"] = first_name
        if last_name:
            data["properties"]["lastname"] = last_name

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError(f"HubSpot API call failed: {response.text}")

    # -----------------------------
    # Update an existing contact
    # -----------------------------
    def update_contact(self, contact_id: str, updates: dict) -> dict:
        url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {"properties": updates}

        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to update contact: {response.text}")

    # -----------------------------
    # Create a deal
    # -----------------------------
    def create_deal(self, deal_name: str, amount: float = None, stage: str = "appointmentscheduled", associated_contact_id: str = None) -> dict:
        url = f"{self.base_url}/crm/v3/objects/deals"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        data = {
            "properties": {
                "dealname": deal_name,
                "dealstage": stage,
                "pipeline": "default"
            }
        }

        if amount:
            data["properties"]["amount"] = amount

        if associated_contact_id:
            data["associations"] = [{
                "to": {"id": associated_contact_id},
                "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3}]
            }]

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError(f"Failed to create deal: {response.text}")

# -----------------------------
# Optional test block
# -----------------------------
if __name__ == "__main__":
    agent = HubSpotAgent()

    # Test creating a contact
    contact = agent.create_contact("test@example.com", "Test", "User")
    print("Created contact ID:", contact["id"])

    # Test updating the contact
    updated = agent.update_contact(contact["id"], {"firstname": "UpdatedTest"})
    print("Updated firstname:", updated["properties"]["firstname"])

    # Test creating a deal
    deal = agent.create_deal("Test Deal", amount=1000, associated_contact_id=contact["id"])
    print("Created deal ID:", deal["id"])
