# Secure Multi-Agent Contract Workflow

## Project Overview
This project demonstrates a **Secure Multi-Agent Contract Workflow** using Descope OAuth for authentication. Multiple agents collaborate to handle contract upload, reading, and approval with proper role-based authorization. The workflow is fully automated and audit-logged.

**Hackathon Theme:** Theme 3 – Secure Multi-Agent Workflows  
**Team Name:** Zeal
**Team Member:** Yunus Evangeline A

---

## Features
- Multi-agent contract workflow: Upload → Read → Approve
- Role-based authorization using Descope OAuth
- Audit logging of all actions
- Simple web UI for login and contract upload
- Scalable FastAPI backend

---

## Tech Stack
- **Backend:** Python, FastAPI  
- **Authentication:** Descope OAuth  
- **Dependencies:** `requests`, `python-dotenv`, `uvicorn`  
- **UI:** Simple HTML served via FastAPI endpoints  
- **Optional Deployment:** Replit, Railway, Fly.io  

---

## Project Structure

contract-approval-system/
├── robot-a.py # Starts workflow and handles UI
├── robot-b.py # Reads and validates contract clauses
├── robot-c.py # Approves the contract
├── start.py # Launches all robots in sequence
├── .env # Environment variables (Descope credentials)
├── requirements.txt # Python dependencies
├── README.md


---

## Setup & Run

1. **Clone the repository**
```bash
git clone https://github.com/Yunus-cmd835/contract-approval-system
cd contract-approval-system

2.Install dependencies

python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt

3.Set environment variables in .env

DESCOPE_PROJECT_ID=P32STnuSogCMt4HniSQkVivvJ9P3
DESCOPE_CLIENT_ID=UDMyU1RudVNvZ0NNdDRIbmlTUWtWaXZ2SjlQMzpUUEEzMlNUdFhwaXc2d0Ezb2FQTld6bUdjOURnaTk=
DESCOPE_CLIENT_SECRET=Mz8NF1LT4t7JiDvoRTRLktJukbM6rXffTtAMV2XPT

4.start the Workflow

python start.py

5.Open the browser

http://localhost:8000

Upload a contract

Login with email (magic link via Descope)

Robot B reads and validates clauses

Robot C approves the contract

Audit log displays all actions

Demo

Recorded Demo : https://www.loom.com/share/ad8fb6b15a6d486aa9f1480f7f8c4eac?sid=417c635a-bda8-49cb-b095-4835d9559849

Max duration: 5 minutes

Shows workflow from upload → read → approval with UI

What Could Be Improved With More Time

Add rich text editor for contracts

Implement real-time collaboration between agents

Add folder organization in Google Drive / storage

Include role-based access control for multiple users
