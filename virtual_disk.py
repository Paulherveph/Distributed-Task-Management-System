import os
import struct

class VirtualDisk:
    def __init__(self, file_name, block_size=512, num_blocks=1024):
        self.file_name = file_name
        self.block_size = block_size
        self.num_blocks = num_blocks

        # Create an empty binary file for the virtual disk
        if not os.path.exists(file_name):
            with open(file_name, "wb") as disk:
                disk.write(b'\x00' * (block_size * num_blocks))  # Initialize with zeros

    def write_block(self, block_number, task_id, data):
        """
        Write a task to a specific block.
        Each block stores: [Task ID (4 bytes), Data Size (4 bytes), Task Data].
        """
        if len(data) > self.block_size - 8:  # Reserve 8 bytes for Task ID and Data Size
            raise ValueError("Data exceeds available block size")

        # Prepare the block header and content
        header = struct.pack("II", task_id, len(data))  # Task ID (4 bytes) + Data Size (4 bytes)
        content = header + data.ljust(self.block_size - 8, b'\x00')  # Pad to full block size

        # Write to the specified block
        with open(self.file_name, "r+b") as disk:
            disk.seek(block_number * self.block_size)
            disk.write(content)

            # Update the index table in the first block
            self.update_index_table(task_id, block_number)

    def update_index_table(self, task_id, block_number):
        """
        Update the index table with Task ID and Block Number.
        The index table is stored in the first block of the disk.
        """
        with open(self.file_name, "r+b") as disk:
            disk.seek(0)
            index_table = disk.read(self.block_size)

            # Add the new entry to the index table
            task_index_entry = struct.pack("II", task_id, block_number)
            updated_table = index_table.rstrip(b'\x00') + task_index_entry

            # Write back the updated index table
            disk.seek(0)
            disk.write(updated_table.ljust(self.block_size, b'\x00'))

    def read_block(self, block_number):
        """
        Read and parse a task from a specific block.
        Returns a dictionary with Task ID and Task Data or None for empty blocks.
        """
        with open(self.file_name, "rb") as disk:
            disk.seek(block_number * self.block_size)
            block = disk.read(self.block_size)

            # Check if the block is uninitialized (all zeros)
            if block == b'\x00' * self.block_size:
                return None  # Return None for empty blocks

            # Parse the block header
            try:
                task_id, data_size = struct.unpack("II", block[:8])  # First 8 bytes
                task_data = block[8:8 + data_size].decode("utf-8").strip('\x00')

                if task_id == 0:  # Empty task
                    return None

                return {"id": task_id, "data": task_data}
            except struct.error:
                print(f"[ERROR] Malformed block at block number {block_number}.")
                return None

    def find_task_by_id(self, task_id):
        """
        Search for a task by its ID using the index table.
        Returns the task data if found.
        """
        with open(self.file_name, "rb") as disk:
            disk.seek(0)
            index_table = disk.read(self.block_size).rstrip(b'\x00')

            # Parse index table entries
            for i in range(0, len(index_table), 8):
                stored_task_id, block_number = struct.unpack("II", index_table[i:i + 8])
                if stored_task_id == task_id:
                    return self.read_block(block_number)
        return None

    def list_all_tasks(self):
        """
        Retrieve all tasks stored on the virtual disk.
        Stop scanning when an empty block is encountered.
        """
        tasks = []
        for block_number in range(1, self.num_blocks):  # Skip block 0 (index table)
            task = self.read_block(block_number)
            if task:
                tasks.append(task)  # Append valid task
            else:
                # Stop scanning once an empty block is found
                break
        print(f"[INFO] Completed scanning disk '{self.file_name}'. Total tasks found: {len(tasks)}")
        return tasks

    def delete_task(self, task_id):
        """
        Delete a task by its ID from the virtual disk.
        """
        with open(self.file_name, "r+b") as disk:
            # Read the index table from Block 0
            disk.seek(0)
            index_table = disk.read(self.block_size)
            updated_table = b""
            task_found = False

            # Parse the index table and remove the task entry
            for i in range(0, len(index_table.rstrip(b'\x00')), 8):
                stored_task_id, block_number = struct.unpack("II", index_table[i:i + 8])
                if stored_task_id == task_id:
                    # Clear the corresponding block on the disk
                    disk.seek(block_number * self.block_size)
                    disk.write(b'\x00' * self.block_size)  # Overwrite with zeros
                    task_found = True
                    print(f"[INFO] Block {block_number} cleared for Task ID {task_id}.")
                else:
                    updated_table += struct.pack("II", stored_task_id, block_number)

            # Write the updated index table back to Block 0
            disk.seek(0)
            disk.write(updated_table.ljust(self.block_size, b'\x00'))

        if task_found:
            print(f"[INFO] Task ID {task_id} successfully deleted.")
        else:
            print(f"[ERROR] Task ID {task_id} not found.")

        return task_found

    def clear_disk(self):
        """
        Clear all data in the virtual disk, including the index table.
        """
        with open(self.file_name, "wb") as disk:
            disk.write(b'\x00' * (self.block_size * self.num_blocks))
        print(f"[INFO] Virtual disk '{self.file_name}' has been cleared.")
