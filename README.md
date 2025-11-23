# Student To-Do List System - README

<br>

## Project Overview

This Python program helps students track tasks such as homework, assignments, and exam preparation. It provides a centralized task management system with a clear table display, enabling users to add, complete, edit, delete, and view tasks conveniently.

Key features:
Tasks are displayed in a clear table format.
Newly added, completed, or edited tasks are immediately saved and displayed.
Supports input validation and retry for invalid IDs or dates.
Automatic tasks.json file creation and persistence.

<br>

## Requirements

Python 3.6.5 or above
Standard Python modules: json, os, datetime
Runs on Windows, macOS, or Linux terminals

<br>

## How to Run

1. Save the program as student_todo_list.py.
2. Make sure tasks.json is in the same folder (it will be created automatically if missing).
3. Open a terminal/command prompt.
4. Navigate to the folder containing student_todo_list.py.
5. Run the program: python student_todo_list.py
6. On start, the program shows the most recent task (highest ID) in a table.
7. Main menu options:

---

任務待辦清單選單：
1. 新增 - 新增任務與截止日期
2. 標記完成 - 將任務標記為已完成
3. 編輯/刪除 - 修改名稱、截止日期或刪除任務
4. 查看所有任務 - 顯示所有任務表格
5. 退出 - 離開程式

---

Enter your choice (1-5).
Tables are displayed for all task lists.
Invalid inputs prompt retry until valid or cancel with Enter.

<br>

## Test Cases

### 1. Add Task
Input: 1 → COMP8080SEF Final Project → 2025-11-29
<br>
Output: Table displaying the newly added task.

### 2. View All Tasks
Input: 4
<br>
Output: Table of all tasks, sorted by ID.

### 3. Complete Task
Input: 2 → select task ID (e.g., 002)
<br>
Output: Table showing task marked as completed.

### 4. Edit Task Name
Input: 3 → task ID (e.g., 002) → 1 → new name
<br>
Output: Table showing updated task name.

### 5. Edit Task Deadline
Input: 3 → task ID → 2 → new date
<br>
Output: Table showing updated deadline.

### 6. Delete Task
Input: 3 → task ID → 3 → confirm y
<br>
Output: Table confirming deletion.

### 7. Cancel Edit
Input: 3 → task ID → 4 or Enter
<br>
Output: Returns to main menu.

### 8. Exit Program
Input: 5
<br>
Output: Program terminates.

<br>

## Invalid Test Cases

### Invalid Deadline Format
Input: 1 → task name → 2025-13-18
<br>
Output: 日期格式錯誤！請使用 YYYY-MM-DD 格式

### Invalid Task ID
Input: 2 or 3 → invalid ID (e.g., abc or nonexistent)
<br>
Output: 找不到該任務或已完成，請重新輸入！ (loops until valid or Enter)

### Invalid Menu Choice
Input: invalid number in main menu (e.g., 6) or edit menu (e.g., 5)
<br>
Output: 請輸入 1-5 的數字！ 或 請輸入 1-4 的數字

<br>

## Notes

Task IDs are 3-digit numbers starting from 001.
Tasks are stored in tasks.json and persist between program runs.
Main menu and edit menu have input validation and table display.
Clearing the screen on each menu ensures a clean interface.
Users can retry entering task IDs if invalid.
All updates (add, complete, edit, delete) are immediately saved and displayed in table format.

<br>

### Last Updated: November 23, 2025