# 學生任務待辦清單
# 作者：Leung Kam Chung Peter
# 版本：1.0
# 功能：新增、標記完成、編輯/刪除、查看任務
# 日期：2025 年 11 月 29 日


import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

# ================ 清屏 ================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ================ 表格 ================
def display_tasks_table(tasks, title="任務列表"):
    if not tasks:
        print("\n沒有任務。\n")
        return
    
    print(f"\n====== {title} ======\n")
    print(" 任務編號 │ 任務名稱                                           │ 狀態       │ 截止日期")
    print("─" * 90)

    for t in tasks:
        print(f" {t['id']:<6}   │ {t['task']:<50} │ {t['status']:<6}  │ {t['deadline']}")

    print("═" * 90 + "\n")

# ================ 取得下一個任務編號 ===============
def get_next_id(tasks):
    if not tasks:                     # 沒有任務時回傳 001
        return "001"
    
    max_id = 0
    for t in tasks:
        current_id = int(t["id"])     # 把字串轉成整數
        if current_id > max_id:
            max_id = current_id
    next_id = max_id + 1
    return f"{next_id:03d}"           # 補零成三位數，例如 001、012

# ================ 主程式 ================
clear()
print("═" * 58)
print("    學生任務待辦清單    ".center(50, "█"))
print("═" * 58)

# 載入任務
if os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        tasks = json.load(f)
else:
    tasks = []

# 開頭顯示最近一次任務
if not tasks:
    print("清單中沒有任務")
else:
    latest_task = tasks[0]
    for t in tasks:
        if int(t["id"]) > int(latest_task["id"]):
            latest_task = t
    display_tasks_table([latest_task], "最近一次任務")

# ================ 主選單 ================
while True:
    input("\n按 Enter 返回主選單…")
    clear()

    print("任務待辦清單選單：(請輸入數字(1-5)操作)")
    print("1. 新增任務")
    print("2. 標記完成")
    print("3. 編輯/刪除任務")
    print("4. 查看所有任務")
    print("5. 退出")
    choice = input("\n請選擇 (1-5): ").strip()

    # 1. 新增任務
    if choice == "1":
        clear()
        print("1. 新增任務 （直接按 Enter 即可取消）\n")

        name = input("輸入任務名稱：").strip()
        if name == "":
            clear()
            print("已取消新增")
            continue

        while True:
            deadline = input("輸入截止日期 (YYYY-MM-DD)：").strip()
            if deadline == "":
                print("已取消新增\n")
                break

            try:
                datetime.strptime(deadline, "%Y-%m-%d")
                new_id = get_next_id(tasks)

                new_task = {
                    "id": new_id,
                    "task": name,
                    "deadline": deadline,
                    "status": "未完成"
                }
                tasks.append(new_task)

                with open(TASKS_FILE, "w", encoding="utf-8") as f:
                    json.dump(tasks, f, ensure_ascii=False, indent=4)

                print("\n任務新增成功！已新增以下任務：")
                display_tasks_table([new_task])
                break

            except ValueError:
                print("日期格式錯誤！請使用 YYYY-MM-DD 格式")

    # 2. 標記完成
    elif choice == "2":
        clear()
        pending = []
        for t in tasks:
            if t["status"] == "未完成":
                pending.append(t)

        if not pending:
            print("沒有未完成的任務！")
            continue

        while True:
            display_tasks_table(pending, "未完成任務")
            tid = input("輸入要完成的任務編號（按 Enter 取消）：").strip()
            if tid == "":
                print("已取消操作\n")
                break  # 取消就跳出

            # 嘗試找到任務
            found_task = None
            for task in pending:
                if task["id"] == tid:
                    task["status"] = "已完成"
                    found_task = task
                    break

            if found_task:
                with open(TASKS_FILE, "w", encoding="utf-8") as f:
                    json.dump(tasks, f, ensure_ascii=False, indent=4)
                print(f"\n任務 {tid} 已標記為完成！\n")
                display_tasks_table([found_task], "已更新任務")
                break
            else:
                clear()
                print("找不到該任務或已完成，請重新輸入！")

    # 3. 編輯或刪除
    elif choice == "3":
        clear()
        if not tasks:
            print("目前沒有任務可編輯")
            continue

        while True:
            display_tasks_table(tasks, "所有任務")
            tid = input("輸入要編輯/刪除的任務編號（按 Enter 取消）：").strip()
            if tid == "":
                print("已取消操作\n")
                break

            # 嘗試找任務
            target_task = None
            for task in tasks:
                if task["id"] == tid:
                    target_task = task
                    break

            if target_task:
                # 找到任務就進入編輯選單
                print("\n編輯選單：")
                print("1. 修改任務名稱")
                print("2. 修改截止日期")
                print("3. 刪除此任務")
                print("4. 取消")
                edit_opt = input("選擇 (1-4)：").strip()

                if edit_opt == "1":
                    new_name = input("輸入新名稱（留空取消）：").strip()
                    if new_name:
                        target_task["task"] = new_name
                        print("名稱已更新")
                    else:
                        print("未修改名稱")

                elif edit_opt == "2":
                    while True:
                        new_date = input("輸入新截止日期 (YYYY-MM-DD)（留空取消）：").strip()
                        if new_date == "":
                            print("未修改日期")
                            break
                        try:
                            datetime.strptime(new_date, "%Y-%m-%d")
                            target_task["deadline"] = new_date
                            print("日期已更新")
                            break
                        except:
                            print("日期格式錯誤，請重新輸入")

                elif edit_opt == "3":
                    confirm = input("確定要刪除？(y/n)：").strip().lower()
                    if confirm in ["y", "yes"]:
                        new_tasks = []
                        for t in tasks:
                            if t["id"] != tid:
                                new_tasks.append(t)
                        tasks = new_tasks
                        print("任務已刪除")
                    else:
                        print("已取消刪除")

                elif edit_opt in ["4", ""]:
                    print("已取消編輯")

                else:
                    print("選項錯誤")

                # 儲存檔案
                with open(TASKS_FILE, "w", encoding="utf-8") as f:
                    json.dump(tasks, f, ensure_ascii=False, indent=4)
                break

            else:
                clear()
                print("找不到該任務，請重新輸入！")

    # 4. 查看所有任務
    elif choice == "4":
        clear()
        if not tasks:
            print("清單中沒有任務")
        else:
            # 編號排序
            sorted_tasks = tasks[:]  # 複製一份
            n = len(sorted_tasks)
            for i in range(n):
                for j in range(0, n-i-1):
                    if int(sorted_tasks[j]["id"]) > int(sorted_tasks[j+1]["id"]):
                        sorted_tasks[j], sorted_tasks[j+1] = sorted_tasks[j+1], sorted_tasks[j]
            display_tasks_table(sorted_tasks, "所有任務（按編號排序）")

    # 5. 退出
    elif choice == "5":
        clear()
        print("謝謝使用！再見！")
        break

    else:
        print("請輸入 1-5 的數字！")
