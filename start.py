import subprocess
import time
import sys

print("🚀 Starting Secure Multi-Agent Contract System...")
print("=" * 50)

try:
    print("🤖 Starting Agent B (Contract Parser)...")
    subprocess.Popen([sys.executable, "robot-b.py"])
    time.sleep(2)

    print("🤖 Starting Agent C (Contract Approver)...")
    subprocess.Popen([sys.executable, "robot-c.py"]) 
    time.sleep(2)

    print("🤖 Starting Agent A (Main UI & OAuth Handler)...")
    subprocess.Popen([sys.executable, "robot-a.py"])
    time.sleep(2)

    print("=" * 50)
    print("🎉 All agents are running!")
    print("🌐 Open your browser and go to: http://localhost:8000")
    print("=" * 50)
    
    # Keep the script running
    input("Press Enter to stop all agents...")
    
except KeyboardInterrupt:
    print("\n🛑 Stopping all agents...")