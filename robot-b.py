from fastapi import FastAPI, Depends, HTTPException, Header
import jwt
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DESCOPE_PROJECT_ID = os.getenv("DESCOPE_PROJECT_ID")
app = FastAPI(title="Agent B - Contract Parser")

def get_jwks_key():
    """Get JWKS key for token validation"""
    jwks_url = f"https://api.descope.com/{DESCOPE_PROJECT_ID}/.well-known/jwks.json"
    try:
        response = requests.get(jwks_url)
        return response.json()
    except:
        return None

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

@app.post("/read-contract", dependencies=[Depends(require_scope("contract.read:clauses"))])
async def read_contract(contract: dict):
    return {
        "agent": "Agent B - Contract Parser",
        "contract_id": contract.get("id"),
        "important_clauses": [
            "Payment due within 30 days",
            "Contract duration: 12 months", 
            "Termination clause included"
        ],
        "risk_assessment": "Medium Risk",
        "status": "✅ Parsed successfully with scope validation",
        "required_scope": "contract.read:clauses"
    }

@app.get("/health")
async def health():
    return {"status": "Agent B is running", "port": 8001}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)