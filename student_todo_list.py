"""Student Task To-Do List System.

Simple command-line to-do list for students with deadlines.

Features:
- Add tasks with a YYYY-MM-DD deadline
- Mark tasks as completed
- Edit task name / deadline or delete tasks
- Persist tasks in a JSON file between runs

Usage (interactive): run the script and follow the menu prompts.
This file is intentionally small and easy to read so students can extend it.

作者: Leung Kam Chung Peter
"""

import json
import os
from datetime import datetime, date

# File to store tasks (created in the current working directory)
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file if it exists.

    Returns a list of task dicts. Each task is expected to have keys:
    - id: string id (three digits, e.g. '001')
    - task: task description
    - deadline: string in YYYY-MM-DD
    - status: status string (e.g. '未完成' or '已完成')
    """
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    """Save tasks to JSON file using UTF-8 encoding.

    This ensures non-ASCII characters (e.g., Chinese) are preserved.
    """
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def add_task(task_name, deadline):
    """Add a new task with a deadline.

    ID generation: pick max existing numeric id and add 1. This avoids
    duplicate IDs when tasks are deleted.
    """
    tasks = load_tasks()
    # compute next numeric id
    max_id = 0
    for t in tasks:
        try:
            n = int(t.get("id", "0"))
            if n > max_id:
                max_id = n
        except ValueError:
            continue
    next_id = max_id + 1
    task = {
        "id": "{:03d}".format(next_id),  # three-digit ID
        "task": task_name,
        "deadline": deadline,
        "status": "未完成"
    }
    tasks.append(task)
    save_tasks(tasks)
    print("\n任務已新增：{} (編號: {}, 截止日期: {})".format(task_name, task["id"], deadline))

def complete_task(task_id):
    """Mark a task as completed by ID."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "已完成"
            save_tasks(tasks)
            print("\n任務 {} 已標記為完成：{}".format(task_id, task["task"]))
            return
    print("錯誤：找不到該任務")

def edit_task(task_id, new_name, new_deadline, delete=False):
    """Edit a task's name or deadline by ID."""
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            if delete:
                tasks.pop(i)
                save_tasks(tasks)
                print("\n任務 {} 已刪除：{}".format(task_id, task["task"]))
                return
            if new_name.strip():
                task["task"] = new_name
            if new_deadline and validate_deadline(new_deadline):
                task["deadline"] = new_deadline
            save_tasks(tasks)
            print("\n任務 {} 已更新：{} (截止日期: {})".format(task_id, task["task"], task["deadline"]))
            return
    print("錯誤：找不到該任務")

def view_tasks():
    """Display all tasks with deadlines and statuses."""
    tasks = load_tasks()
    if not tasks:
        print("清單中沒有任務")
        return
    for task in tasks:
        print("{}. {}：{} (截止日期: {})".format(task["id"], task["task"], task["status"], task["deadline"]))

def view_pending_tasks():
    """Display only pending tasks for completion selection."""
    tasks = load_tasks()
    pending_tasks = [task for task in tasks if task["status"] == "未完成"]
    if not pending_tasks:
        print("沒有未完成任務可完成")
        return False
    print("\n未完成任務：")
    for task in pending_tasks:
        print("{}. {} (截止日期: {})".format(task["id"], task["task"], task["deadline"]))
    return True

def validate_deadline(deadline):
    """Return True if deadline is a valid date in YYYY-MM-DD format.

    Uses datetime.strptime to validate exact date values (e.g., rejects 2023-02-30).
    """
    try:
        datetime.strptime(deadline, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False

def main():
    """Main program loop with menu."""
    # Welcome and quick usage info
    print("學生任務待辦清單 (互動模式)")
    print("輸入數字選擇操作。日期格式示例：2025-12-31")
    print("當前任務：")
    view_tasks()
    
    while True:
        print("\n任務待辦清單選單：")
        print("1. 新增 - 新增任務和截止日期")
        print("2. 完成 - 標記任務為已完成")
        print("3. 編輯 - 修改任務名稱或截止日期")
        print("4. 查看 - 查看所有任務")
        print("5. 退出 - 退出程式")
        choice = input("輸入您的選擇 (1-5)：").strip()
        
        if choice == "1":
            task_name = input("輸入任務名稱：")
            if not task_name.strip():
                print("錯誤：任務名稱不能為空")
                continue
            deadline = input("輸入截止日期 (YYYY-MM-DD)：")
            if validate_deadline(deadline):
                add_task(task_name, deadline)
            else:
                print("錯誤：截止日期格式無效，請使用 YYYY-MM-DD")
                
        elif choice == "2":
            if view_pending_tasks():  # Show pending tasks
                try:
                    task_id = input("輸入要編輯的任務編號：").strip()
                    complete_task(task_id)
                except ValueError:
                    print("錯誤：請輸入有效的數字")
                
        elif choice == "3":
            view_tasks()  # Show all tasks for editing
            task_id = input("輸入要編輯的任務編號（或輸入 'exit' 返回主選單）：").strip()
            if task_id.lower() == "exit":
                print("返回任務待辦清單選單")
                continue
            """Check if the ID is valid"""
            tasks = load_tasks()
            if not any(task["id"] == task_id for task in tasks):
                print("\n錯誤：請輸入有效的任務編號或輸入 'exit' 返回主選單")
                continue
            if task_id:
                print("\n編輯選項：")
                print("1. 修改任務名稱")
                print("2. 修改截止日期")
                print("3. 刪除任務")
                print("4. 退出")
                edit_choice = input("輸入您的選擇 (1-4)：").strip()
                
                if edit_choice == "1":
                    new_name = input("輸入新任務名稱：")
                    if not new_name.strip():
                        print("錯誤：任務名稱不能為空")
                    else:
                        edit_task(task_id, new_name, "")
                elif edit_choice == "2":
                    new_deadline = input("輸入新截止日期 (YYYY-MM-DD)：")
                    if validate_deadline(new_deadline):
                        edit_task(task_id, "", new_deadline)
                    else:
                        print("錯誤：截止日期格式無效，請使用 YYYY-MM-DD")
                elif edit_choice == "3":
                    edit_task(task_id, "", "", delete=True)
                elif edit_choice == "4":
                    print("取消編輯")
                else:
                    print("\n錯誤：請輸入 1-4 的數字")
            else:
                print("錯誤：請輸入有效的任務編號")
                
        elif choice == "4":
            view_tasks()
            
        elif choice == "5":
            break
            
        else:
            print("\n錯誤：請輸入 1-5 的數字")

if __name__ == "__main__":
    main()