# Distributed Task Management System

This project is a **cloud-based simulation** that manages tasks across distributed virtual machines (VMs). It incorporates concepts of cloud computing, multithreading, and virtual disk storage to create a robust system for task management.

## Features
- Add, update, delete, and retrieve tasks for each VM.
- Persistent task storage using a simulated virtual disk.
- Dual-core CPU simulation for parallel task processing.
- Commands processed via a centralized cloud system.
- Retrieve processed tasks from both memory and virtual disk.

## Technologies Used
- **Python**: Programming language.
- **Object-Oriented Programming (OOP)**: For modular and scalable design.
- **Multithreading**: To simulate CPU cores.
- **File-based Storage**: To simulate virtual disk operations.

## How It Works
1. **Client Commands**: Commands are issued through the `client.py` script.
2. **Cloud Processing**: Commands are processed by the `cloud.py` module and routed to the appropriate VM.
3. **Task Storage**: Tasks are processed and stored in both memory and a virtual disk.

## Commands
- Add a Task:
  ```bash
  python client.py add-task <vm_id> <task_data> <task_id>

- List Tasks:
  ```bash
  python client.py list-tasks <vm_id>

- Delete a Task:
  ```bash
  python client.py delete-task <vm_id> <task_id>

- Update a Task:
  ```bash
  python client.py update-task <vm_id> <task_id> <new_data>

- Get Processed Tasks:
  ```bash
  python client.py get-processed-tasks <vm_id>

- List All Tasks (Stored on Disk):
  ```bash
  python client.py list-all-tasks <vm_id>

- Clear Disk:
  ```bash
  python client.py clear-disk <vm_id>

