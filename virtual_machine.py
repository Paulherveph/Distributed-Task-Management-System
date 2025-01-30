import threading
import time
from virtual_disk import VirtualDisk

class VirtualMachine:
    def __init__(self, vm_id, disk_file):
        self.vm_id = vm_id
        self.disk = VirtualDisk(disk_file)
        self.task_queue = []
        self.processed_tasks = []  # Track processed tasks in memory
        self.lock = threading.Lock()

        # Simulate dual-core CPU
        self.cpu_cores = [
            threading.Thread(target=self.process_tasks, name=f"Core-1"),
            threading.Thread(target=self.process_tasks, name=f"Core-2")
        ]
        self.running = True
        for core in self.cpu_cores:
            core.start()

    def add_task(self, task):
        """Add a task to the queue."""
        with self.lock:
            self.task_queue.append(task)
            print(f"[INFO] Task added to VM {self.vm_id}: {task}")

    def process_tasks(self):
        """Process tasks using a CPU core."""
        while self.running:
            task = None
            # Acquire a task from the queue without holding the lock for processing
            with self.lock:
                if self.task_queue:
                    task = self.task_queue.pop(0)
                    print(f"[INFO] {threading.current_thread().name} picked task: {task}")

            # Process the task outside the lock
            if task:
                print(f"[INFO] {threading.current_thread().name} processing task: {task}")
                time.sleep(2)  # Simulate task processing delay
                self.disk.write_block(task["id"], task["id"], task["data"].encode("utf-8"))

                # Update processed tasks
                with self.lock:
                    self.processed_tasks.append(task)
                print(f"[INFO] Task completed. Data written: {task}")

    def update_task(self, task_id, new_data):
        """Update a task's data."""
        with self.lock:
            # Check the task queue
            for task in self.task_queue:
                if task["id"] == task_id:
                    task["data"] = new_data
                    print(f"[INFO] Task {task_id} updated in VM {self.vm_id}: {new_data}")
                    return True

            # Check processed tasks
            for task in self.processed_tasks:
                if task["id"] == task_id:
                    task["data"] = new_data
                    self.disk.write_block(task_id, task_id, new_data.encode("utf-8"))
                    print(f"[INFO] Processed task {task_id} updated in VM {self.vm_id}: {new_data}")
                    return True

            # If task not found
            print(f"[ERROR] Task {task_id} not found in VM {self.vm_id}.")
            return False

    def get_processed_tasks(self):
        """Retrieve processed tasks from both memory and the virtual disk."""
        processed_tasks = self.processed_tasks.copy()  # Start with in-memory processed tasks

        # Read processed tasks from the virtual disk
        disk_tasks = []
        for block_id in range(1, self.disk.num_blocks):  # Skip the index table block (block 0)
            task = self.disk.read_block(block_id)
            if task:
                disk_tasks.append(task)

        print(f"[INFO] Processed tasks retrieved from VM {self.vm_id}.")
        return processed_tasks + disk_tasks  # Combine memory & disk tasks

    def delete_task(self, task_id):
        """
        Delete a task from the queue and the disk.
        """
        with self.lock:
            # Remove task from in-memory queue
            self.task_queue = [task for task in self.task_queue if task["id"] != task_id]
            # Delete task from the disk
            task_deleted = self.disk.delete_task(task_id)

        if task_deleted:
            print(f"[INFO] Task {task_id} deleted from VM {self.vm_id}.")
            return True
        else:
            print(f"[ERROR] Task {task_id} not found in VM {self.vm_id}.")
            return False

    def stop(self):
        """Stop the VM."""
        self.running = False
        for core in self.cpu_cores:
            core.join()
