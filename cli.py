import requests

C2_URL = "http://localhost:5000"

def list_agents():
    res = requests.get(f"{C2_URL}/agents")
    print("\nAvailable Agents:")
    for agent in res.json().get("agents", []):
        print(f" - {agent}")

def send_command():
    agent_id = input("Enter Agent ID: ")
    cmd = input("Command to send: ")
    res = requests.post(f"{C2_URL}/task", json={"agent_id": agent_id, "command": cmd})
    print(res.json())

def fetch_results():
    agent_id = input("Enter Agent ID: ")
    res = requests.get(f"{C2_URL}/results/{agent_id}")
    print("\n--- Output ---")
    for r in res.json().get("results", []):
        print(r)

def main():
    while True:
        print("\n=== C2 CLI ===")
        print("1. List Agents")
        print("2. Send Command")
        print("3. Fetch Results")
        print("4. Exit")
        choice = input("Select: ")

        if choice == '1':
            list_agents()
        elif choice == '2':
            send_command()
        elif choice == '3':
            fetch_results()
        elif choice == '4':
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main()