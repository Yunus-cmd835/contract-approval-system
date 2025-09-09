from fastapi import FastAPI, Depends, HTTPException, Header
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

DESCOPE_PROJECT_ID = os.getenv("DESCOPE_PROJECT_ID")
app = FastAPI(title="Agent C - Contract Approver")

def validate_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    token = authorization.split("Bearer ")[1]
    
    try:
        # Simple validation - decode without verification for demo
        decoded = jwt.decode(token, options={"verify_signature": False})
        scopes = decoded.get("scope", "").split() if decoded.get("scope") else []
        return scopes
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def require_scope(required_scope: str):
    def check_scope(scopes: list = Depends(validate_token)):
        if required_scope not in scopes:
            raise HTTPException(status_code=403, detail=f"Missing scope: {required_scope}")
        return scopes
    return check_scope

@app.post("/approve-contract", dependencies=[Depends(require_scope("contract.sign"))])
async def approve_contract(data: dict):
    return {
        "agent": "Agent C - Contract Approver", 
        "contract_id": data.get("contract_id"),
        "decision": "APPROVED",
        "reason": "Contract meets all requirements",
        "status": "✅ Final approval completed with authorization",
        "required_scope": "contract.sign",
        "timestamp": "2025-01-09T10:00:00Z"
    }

@app.get("/health")
async def health():
    return {"status": "Agent C is running", "port": 8002}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)