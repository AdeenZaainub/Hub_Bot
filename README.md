# Hub_Bot
AI-powered autonomous agents to automate workflows. The Global Orchestrator interprets user queries via Groq LLaMA, HubSpot Agent manages CRM tasks, and Email Agent sends confirmations. Enables creating/updating contacts, deals, and automating repetitive business operations efficiently.

## Folder Structure

<img width="732" height="307" alt="image" src="https://github.com/user-attachments/assets/f052770a-bdd3-4fb2-b6a7-9fb1405f72c2" />



# Installation & Setup
cd genai_hubspot_agent

cd agents

## Install required Python packages:
### Install LangChain Community Edition
pip install langchain

### Install Groq API client
pip install groq

### Install requests for API calls
pip install requests

### (Optional) Install Pydantic for structured tool validation
pip install pydantic

## Create a configuration folder and file:
mkdir config

Inside the config folder, create a file named config.json with the following structure:

{
  "hubspot": {
    "access_token": "<HUBSPOT_ACCESS_TOKEN>"
  },
  "groq": {
    "api_key": "<GROQ_API_KEY>",
    "default_model": "<DEFAULT_MODEL_NAME>"
  },
  "email": {
    "smtp_server": "<SMTP_SERVER>",
    "smtp_port": 587,
    "email": "<YOUR_EMAIL>",
    "password": "<EMAIL_PASSWORD>"
  }
}

Replace the placeholders with your actual API keys and email credentials.
## Command to run the code 
python orchestrator_agent.py
## Example Quries
i want to create a deal with amount 600 and name bicycle

i want to create contact named as sara zafar  with email as sarazafar@gmail.com


