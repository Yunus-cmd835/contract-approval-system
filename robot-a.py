import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Agent A - Main UI & OAuth Handler")

CLIENT_ID = os.getenv("DESCOPE_CLIENT_ID")
CLIENT_SECRET = os.getenv("DESCOPE_CLIENT_SECRET")

@app.get("/")
async def home():
    login_link = f"https://api.descope.com/oauth2/v1/apps/authorize?client_id={CLIENT_ID}&redirect_uri=http://localhost:8000/callback&response_type=code&scope=contract.upload contract.read:clauses contract.sign"
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Secure Multi-Agent Contract System</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .container {{ 
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 600px;
                width: 100%;
            }}
            h1 {{ 
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5em;
            }}
            .subtitle {{ 
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }}
            .agents {{ 
                display: flex;
                justify-content: space-around;
                margin: 30px 0;
                flex-wrap: wrap;
            }}
            .agent {{ 
                background: #f8f9fa;
                padding: 20px;
                border-radius: 15px;
                margin: 10px;
                flex: 1;
                min-width: 150px;
                border: 2px solid #e9ecef;
            }}
            .agent h3 {{ 
                margin: 0 0 10px 0;
                color: #495057;
            }}
            .scope {{ 
                background: #e3f2fd;
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.8em;
                color: #1976d2;
                margin: 5px 2px;
                display: inline-block;
            }}
            .login-btn {{ 
                background: linear-gradient(45deg, #4CAF50, #45a049);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 50px;
                font-size: 1.2em;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin-top: 20px;
                transition: transform 0.2s;
            }}
            .login-btn:hover {{ 
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            }}
            .flow-diagram {{ 
                margin: 30px 0;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 15px;
                border-left: 5px solid #4CAF50;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Secure Multi-Agent Contract System</h1>
            <p class="subtitle">Powered by Descope OAuth & Scope-Based Access Control</p>
            
            <div class="agents">
                <div class="agent">
                    <h3>🤖 Agent A</h3>
                    <p>OAuth Handler</p>
                    <div class="scope">contract.upload</div>
                </div>
                <div class="agent">
                    <h3>🔍 Agent B</h3>
                    <p>Contract Parser</p>
                    <div class="scope">contract.read:clauses</div>
                </div>
                <div class="agent">
                    <h3>✅ Agent C</h3>
                    <p>Final Approver</p>
                    <div class="scope">contract.sign</div>
                </div>
            </div>
            
            <div class="flow-diagram">
                <h3>🔄 Secure Agent Flow</h3>
                <p>User → Agent A (OAuth) → Agent B (Scope Validation) → Agent C (Final Approval)</p>
            </div>
            
            <a href="{login_link}" class="login-btn">
                🚀 Start Secure Contract Process
            </a>
            
            <p style="margin-top: 20px; font-size: 0.9em; color: #666;">
                Each agent operates with least-privilege access using Descope OAuth scopes
            </p>
        </div>
    </body>
    </html>
    """)

@app.get("/callback")
async def callback(code: str):
    try:
        # Exchange authorization code for access token
        response = requests.post(
            "https://api.descope.com/oauth2/v1/apps/token",
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "redirect_uri": "http://localhost:8000/callback"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code != 200:
            return HTMLResponse(f"""
            <h1>❌ OAuth Error</h1>
            <p>Status: {response.status_code}</p>
            <p>Response: {response.text}</p>
            <a href="/">Try Again</a>
            """)
        
        token_data = response.json()
        
        if "access_token" not in token_data:
            return HTMLResponse("""
            <h1>❌ Token Error</h1>
            <p>No access_token in response</p>
            <a href="/">Try Again</a>
            """)
        
        master_key = token_data["access_token"]
        contract = {"id": "contract_123", "content": "Sample contract for approval"}
        
        # Call Agent B (Contract Parser)
        try:
            robot_b_response = requests.post(
                "http://localhost:8001/read-contract",
                json=contract,
                headers={"Authorization": f"Bearer {master_key}"},
                timeout=5
            )
            robot_b_result = robot_b_response.json() if robot_b_response.status_code == 200 else {"error": f"Agent B failed: {robot_b_response.status_code}"}
        except Exception as e:
            robot_b_result = {"error": f"Agent B not available: {str(e)}"}
        
        # Call Agent C (Contract Approver)
        try:
            robot_c_response = requests.post(
                "http://localhost:8002/approve-contract", 
                json={"contract_id": "contract_123", "parsed_data": robot_b_result},
                headers={"Authorization": f"Bearer {master_key}"},
                timeout=5
            )
            robot_c_result = robot_c_response.json() if robot_c_response.status_code == 200 else {"error": f"Agent C failed: {robot_c_response.status_code}"}
        except Exception as e:
            robot_c_result = {"error": f"Agent C not available: {str(e)}"}
        
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Success - Multi-Agent Results</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 40px; background: #f0f8ff; }}
                .container {{ background: white; padding: 30px; border-radius: 15px; max-width: 800px; margin: 0 auto; }}
                .success {{ color: #4CAF50; }}
                .agent-result {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #4CAF50; }}
                .token-info {{ background: #e3f2fd; padding: 15px; border-radius: 10px; font-family: monospace; word-break: break-all; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="success">🎉 Multi-Agent OAuth Success!</h1>
                
                <div class="token-info">
                    <h3>🔐 Access Token (First 50 chars):</h3>
                    <code>{master_key[:50]}...</code>
                </div>
                
                <div class="agent-result">
                    <h3>🔍 Agent B (Contract Parser) Response:</h3>
                    <pre>{robot_b_result}</pre>
                </div>
                
                <div class="agent-result">
                    <h3>✅ Agent C (Contract Approver) Response:</h3>
                    <pre>{robot_c_result}</pre>
                </div>
                
                <a href="/" style="background: #2196F3; color: white; padding: 10px 20px; border-radius: 25px; text-decoration: none;">🔄 Test Again</a>
            </div>
        </body>
        </html>
        """)
        
    except Exception as e:
        return HTMLResponse(f"""
        <h1>❌ Unexpected Error</h1>
        <p>Error: {str(e)}</p>
        <a href="/">Try Again</a>
        """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)