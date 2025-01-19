from cloud import Cloud
from virtual_machine import VirtualMachine

COMMAND_FILE = "data/command.txt"
RESPONSE_FILE = "data/response.txt"

def main():
    # Initialize the cloud
    cloud = Cloud()

    # Create virtual machines with virtual disks
    vm1 = VirtualMachine(vm_id=1, disk_file="data/vm1_disk.bin")
    vm2 = VirtualMachine(vm_id=2, disk_file="data/vm2_disk.bin")

    cloud.add_vm(vm1)
    cloud.add_vm(vm2)

    print("[INFO] Cloud service is running...")

    while True:
        try:
            # Read the command file for incoming commands
            with open(COMMAND_FILE, "r") as file:
                command = file.read().strip()

            if command:
                print(f"[INFO] Processing command: {command}")
                response = cloud.process_command(command)

                # Write the response to the response file
                with open(RESPONSE_FILE, "w") as file:
                    file.write(response + "\n")

                # Clear the command file after processing
                with open(COMMAND_FILE, "w") as file:
                    file.write("")
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    main()
