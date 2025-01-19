import sys
import struct
import os

BLOCK_SIZE = 512
NUM_BLOCKS = 1024

def read_virtual_disk(file_name, block_size=BLOCK_SIZE):
    """Read and parse the contents of a virtual disk using the index table."""
    tasks = []
    try:
        with open(file_name, "rb") as disk:
            # Read the index table from the first block
            index_table = disk.read(block_size)
            task_entries = index_table.rstrip(b'\x00')

            # Parse index entries (Task ID + Block Number pairs)
            for i in range(0, len(task_entries), 8):  # Each entry is 8 bytes
                task_id, block_number = struct.unpack("II", task_entries[i:i + 8])

                # Read the task data from the corresponding block
                disk.seek(block_number * block_size)
                block = disk.read(block_size)
                _, data_size = struct.unpack("II", block[:8])
                task_data = block[8:8 + data_size].decode("utf-8").strip('\x00')

                tasks.append({
                    "Block Number": block_number,
                    "Task ID": task_id,
                    "Data Size": data_size,
                    "Task Data": task_data
                })
    except FileNotFoundError:
        print(f"[ERROR] File '{file_name}' not found.")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    return tasks

def display_tasks(tasks):
    """Display tasks in a tabular format."""
    if not tasks:
        print("[INFO] No tasks found in the virtual disk.")
        return

    print(f"{'Block':<10}{'Task ID':<10}{'Data Size':<10}{'Task Data':<20}")
    print("-" * 50)
    for task in tasks:
        print(f"{task['Block Number']:<10}{task['Task ID']:<10}{task['Data Size']:<10}{task['Task Data']:<20}")

def clear_disk(file_name):
    """Clear all data in the virtual disk."""
    try:
        with open(file_name, "wb") as disk:
            disk.write(b'\x00' * (BLOCK_SIZE * NUM_BLOCKS))  # Overwrite with zeros
        print(f"[INFO] Successfully cleared the disk: {file_name}")
    except Exception as e:
        print(f"[ERROR] Failed to clear disk '{file_name}': {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_disk.py <command> <disk_file>")
        print("Commands:")
        print("  analyze      - Display tasks in the specified disk.")
        print("  clear-disk   - Clear all data from the specified disk.")
        print("Example:")
        print("  python analyze_disk.py analyze vm1_disk.bin")
        print("  python analyze_disk.py clear-disk vm1_disk.bin")
    else:
        command = sys.argv[1]
        disk_file = sys.argv[2]

        if command == "analyze":
            print(f"[INFO] Analyzing virtual disk: {disk_file}")
            tasks = read_virtual_disk(disk_file)
            display_tasks(tasks)
        elif command == "clear-disk":
            print(f"[INFO] Clearing virtual disk: {disk_file}")
            clear_disk(disk_file)
        else:
            print(f"[ERROR] Unknown command: {command}")
