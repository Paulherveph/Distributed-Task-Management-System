from virtual_machine import VirtualMachine

class Cloud:
    def __init__(self):
        self.vms = []

    def add_vm(self, vm):
        """Add a virtual machine to the cloud."""
        self.vms.append(vm)
        print(f"[INFO] VM {vm.vm_id} added to the cloud.")

    def process_command(self, command):
        """Process a client command."""
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "add-task":
            if len(args) < 3:
                return "Usage: add-task <vm_id> <data> <task_id>"
            try:
                vm_id = int(args[0])
                task_id = int(args[-1])  # The last argument should always be the task ID
                data = " ".join(args[1:-1])  # Combine everything between the VM ID and Task ID
                task = {"id": task_id, "data": data}
                vm = next((vm for vm in self.vms if vm.vm_id == vm_id), None)
                if vm:
                    vm.add_task(task)
                    return f"Task added to VM {vm_id}: {task}"
                return f"[ERROR] VM {vm_id} not found."
            except ValueError:
                return "[ERROR] Invalid task ID format. Ensure it's an integer."

        elif cmd == "list-tasks":
            if len(args) != 1:
                return "Usage: list-tasks <vm_id>"
            vm_id = int(args[0])
            vm = next((vm for vm in self.vms if vm.vm_id == vm_id), None)
            if vm:
                tasks = vm.task_queue
                return f"Tasks in VM {vm_id}: {tasks}"
            return f"[ERROR] VM {vm_id} not found."

        elif cmd == "delete-task":
            if len(args) != 2:
                return "Usage: delete-task <vm_id> <task_id>"
            vm_id = int(args[0])
            task_id = int(args[1])
            vm = next((vm for vm in self.vms if vm.vm_id == vm_id), None)
            if vm:
                vm.task_queue = [t for t in vm.task_queue if t["id"] != task_id]
                return f"Task {task_id} deleted from VM {vm_id}"
            return f"[ERROR] VM {vm_id} not found."

        elif cmd == "update-task":
            if len(args) < 3:
                return "Usage: update-task <vm_id> <task_id> <new_data>"
            try:
                vm_id = int(args[0])
                task_id = int(args[1])
                new_data = " ".join(args[2:])
                vm = next((vm for vm in self.vms if vm.vm_id == vm_id), None)
                if vm:
                    updated = vm.update_task(task_id, new_data)
                    if updated:
                        return f"Task {task_id} in VM {vm_id} updated to: {new_data}"
                    return f"[ERROR] Task {task_id} not found in VM {vm_id}."
                return f"[ERROR] VM {vm_id} not found."
            except ValueError:
                return "[ERROR] Invalid task ID format. Ensure it's an integer."

        elif cmd == "get-processed-tasks":
            if len(args) != 1:
                return "Usage: get-processed-tasks <vm_id>"
            vm_id = int(args[0])
            vm = next((vm for vm in self.vms if vm.vm_id == vm_id), None)
            if vm:
                processed_tasks = vm.get_processed_tasks()
                return f"Processed tasks in VM {vm_id}: {processed_tasks}"
            return f"[ERROR] VM {vm_id} not found."

        elif cmd == "list-all-tasks":
            if len(args) != 1:
                return "Usage: list-all-tasks <vm_id>"
            vm_id = int(args[0])
            vm = next((vm for vm in self.vms if vm.vm_id == vm_id), None)
            if vm:
                all_tasks = vm.disk.list_all_tasks()
                return f"All tasks in VM {vm_id}: {all_tasks}"
            return f"[ERROR] VM {vm_id} not found."

        elif cmd == "clear-disk":
            if len(args) != 1:
                return "Usage: clear-disk <vm_id>"
            vm_id = int(args[0])
            vm = next((vm for vm in self.vms if vm.vm_id == vm_id), None)
            if vm:
                vm.disk.clear_disk()
                return f"Disk for VM {vm_id} has been cleared."
            return f"[ERROR] VM {vm_id} not found."

        return f"[ERROR] Unknown command: {cmd}"
