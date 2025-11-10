import subprocess

# Simple command execution


# Run your commands
subprocess.Popen("uvicorn prediction_api:app --port 8000",shell=True)
subprocess.Popen("streamlit run app.py --server.port=8502 --server.address=0.0.0.0", shell=True)
subprocess.Popen("rclone mount gdrive:MyProject ./gdrive --vfs-cache-mode full",shell=True)
