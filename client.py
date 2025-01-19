import time

COMMAND_FILE = "data/command.txt"
RESPONSE_FILE = "data/response.txt"

def send_command(command):
    """Write the command to the shared file and wait for a response."""
    # Clear the response file
    with open(RESPONSE_FILE, "w") as file:
        file.write("")  # Clear previous response

    # Write the command to the command file
    with open(COMMAND_FILE, "w") as file:
        file.write(command + "\n")

    print("[INFO] Command sent. Waiting for response...")

    # Wait for the response
    while True:
        try:
            with open(RESPONSE_FILE, "r") as file:
                response = file.read().strip()
                if response:  # Wait until the response file is updated
                    print("[INFO] Response received:")
                    print(response)
                    break
        except FileNotFoundError:
            time.sleep(1)  # Wait if the response file is not yet created

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python client.py <command>")
    else:
        command = " ".join(sys.argv[1:])
        send_command(command)
