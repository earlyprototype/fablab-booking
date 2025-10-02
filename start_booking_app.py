"""
Launcher script for FabLab Booking System
"""

import subprocess
import sys

print("="*60)
print("Starting FabLab Equipment Booking System")
print("="*60)
print("\nThe booking app will be available at:")
print("  http://localhost:8503")
print("\nMake sure the Nexus API is running on port 8300")
print("="*60 + "\n")

subprocess.run([
    sys.executable, "-m", "streamlit", "run",
    "app.py",
    "--server.port", "8503",
    "--server.headless", "true"
])

