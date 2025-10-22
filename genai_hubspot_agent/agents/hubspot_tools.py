from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from hubspot_agent import HubSpotAgent

# Initialize HubSpot client
hubspot_client = HubSpotAgent()

# -----------------------------
# ✅ Tool Input Schemas
# -----------------------------
class CreateContactInput(BaseModel):
    email: str = Field(..., description="Email of the contact")
    first_name: str | None = Field(None, description="First name of the contact")
    last_name: str | None = Field(None, description="Last name of the contact")

class UpdateContactInput(BaseModel):
    contact_id: str = Field(..., description="HubSpot contact ID")
    updates: dict = Field(..., description="Dictionary of fields to update")

class CreateDealInput(BaseModel):
    deal_name: str = Field(..., description="Name of the deal")
    amount: float | None = Field(None, description="Deal amount")
    stage: str | None = Field("appointmentscheduled", description="Pipeline stage")
    associated_contact_id: str | None = Field(None, description="Associated contact ID")

# -----------------------------
# ✅ Tool Functions
# -----------------------------
def create_contact(email, first_name=None, last_name=None):
    return hubspot_client.create_contact(email, first_name, last_name)

def update_contact(contact_id, updates):
    return hubspot_client.update_contact(contact_id, updates)

def create_deal(deal_name, amount=None, stage="appointmentscheduled", associated_contact_id=None):
    return hubspot_client.create_deal(deal_name, amount, stage, associated_contact_id)

# -----------------------------
# ✅ Structured Tools
# -----------------------------
create_contact_tool = StructuredTool.from_function(
    func=create_contact,
    name="create_contact",
    description="Create a new contact in HubSpot CRM",
    args_schema=CreateContactInput
)

update_contact_tool = StructuredTool.from_function(
    func=update_contact,
    name="update_contact",
    description="Update an existing HubSpot contact by ID",
    args_schema=UpdateContactInput
)

create_deal_tool = StructuredTool.from_function(
    func=create_deal,
    name="create_deal",
    description="Create a new deal and associate it with a contact",
    args_schema=CreateDealInput
)

if __name__ == "__main__":
    print("🧪 Testing HubSpot Tools Integration...\n")

    try:
        # Test 1️⃣: Create a contact
        print("👉 Creating test contact...")
        contact_result = create_contact_tool.invoke({
            "email": "tool_test@example.com",
            "first_name": "Tool",
            "last_name": "Tester"
        })
        print("✅ Contact Created:", contact_result)

        # Test 2️⃣: Update contact (optional, only if you have contact_id)
        print("\n👉 Updating test contact (if created)...")
        if "id" in contact_result:
            update_result = update_contact_tool.invoke({
                "contact_id": contact_result["id"],
                "updates": {"firstname": "UpdatedTool"}
            })
            print("✅ Contact Updated:", update_result)
        else:
            print("⚠️ No contact ID returned; skipping update test.")

        # Test 3️⃣: Create a deal
        print("\n👉 Creating test deal...")
        deal_result = create_deal_tool.invoke({
            "deal_name": "Tool Test Deal",
            "amount": 3000
        })
        print("✅ Deal Created:", deal_result)

        print("\n🎯 All tests completed successfully!")

    except Exception as e:
        print("❌ Error during testing:", e)