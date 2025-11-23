# 學生任務待辦清單
# 作者：Leung Kam Chung Peter

import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

# ================ 主程式開始 ================

print("學生任務待辦清單")
print("輸入數字選擇操作")
print("日期格式示例：2025-12-31\n")

# 載入任務
if os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        tasks = json.load(f)
else:
    tasks = []

# 開頭顯示目前任務
if len(tasks) == 0:
    print("清單中沒有任務")
else:
    for task in tasks:
        print(f"{task['id']}. {task['task']}：{task['status']} (截止日期: {task['deadline']})")

# ================ 主選單 ================
while True:
    print("\n" + "="*40)
    print("任務待辦清單選單：")
    print("1. 新增任務")
    print("2. 標記完成")
    print("3. 編輯/刪除任務")
    print("4. 查看所有任務")
    print("5. 退出")
    choice = input("\n請選擇 (1-5): ").strip()

    # ────── 1. 新增任務 ──────
    if choice == "1":
        print("\n=== 新增任務 === （直接按 Enter 即可取消）")
        
        name = input("輸入任務名稱：").strip()
        if name == "":                     # 留空就取消
            print("已取消新增\n")
            continue

        while True:
            deadline = input("輸入截止日期 (YYYY-MM-DD)：").strip()
            if deadline == "":             # 留空就取消
                print("已取消新增\n")
                break

            try:
                datetime.strptime(deadline, "%Y-%m-%d")
                if tasks:
                    last_id = max(int(t["id"]) for t in tasks)
                    new_id = f"{last_id + 1:03d}"
                else:
                    new_id = "001"

                tasks.append({
                    "id": new_id,
                    "task": name,
                    "deadline": deadline,
                    "status": "未完成"
                })

                with open(TASKS_FILE, "w", encoding="utf-8") as f:
                    json.dump(tasks, f, ensure_ascii=False, indent=4)

                print(f"\n任務新增成功！")
                print(f"編號：{new_id}｜名稱：{name}｜截止：{deadline}\n")
                break

            except ValueError:
                print("日期格式錯誤！請使用 YYYY-MM-DD 格式")

    # 2. 標記完成
    elif choice == "2":
        pending = [t for t in tasks if t["status"] == "未完成"]
        if not pending:
            print("沒有未完成的任務！")
            continue

        print("\n未完成任務：")
        for t in pending:
            print(f"{t['id']}. {t['task']} (截止: {t['deadline']})")

        tid = input("\n輸入要完成的任務編號（直接按 Enter 取消）：").strip()
        if tid == "":                      # 留空就取消
            print("已取消操作\n")
            continue

        found = False
        for task in tasks:
            if task["id"] == tid and task["status"] == "未完成":
                task["status"] = "已完成"
                found = True
                break

        if found:
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump(tasks, f, ensure_ascii=False, indent=4)
            print(f"任務 {tid} 已標記為完成！")
        else:
            print("找不到該任務或已完成")

    # 3. 編輯或刪除
    elif choice == "3":
        if not tasks:
            print("目前沒有任務可編輯")
            continue

        for task in tasks:
            print(f"{task['id']}. {task['task']}：{task['status']} (截止日期: {task['deadline']})")

        tid = input("\n輸入要編輯的任務編號（直接按 Enter 取消）：").strip()
        if tid == "":                      # 留空就取消
            print("已取消操作\n")
            continue

        target_task = None
        for task in tasks:
            if task["id"] == tid:
                target_task = task
                break

        if target_task is None:
            print("找不到該編號的任務！")
            continue

        print("\n編輯選單：")
        print("1. 修改任務名稱")
        print("2. 修改截止日期")
        print("3. 刪除此任務")
        print("4. 取消")
        edit_opt = input("選擇 (1-4): ").strip()
        if edit_opt == "":                 # 留空也視為取消
            edit_opt = "4"

        if edit_opt == "1":
            new_name = input("輸入新名稱：").strip()
            if new_name == "":             # 留空就取消修改
                print("未修改名稱")
            else:
                target_task["task"] = new_name
                print("名稱已更新")

        elif edit_opt == "2":
            while True:
                new_date = input("輸入新截止日期 (YYYY-MM-DD)（留空取消）：").strip()
                if new_date == "":         # 留空就取消
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
            confirm = input("確定要刪除？(y/n): ").strip().lower()
            if confirm == "y" or confirm == "yes":
                tasks = [t for t in tasks if t["id"] != tid]
                print("任務已刪除")
            else:
                print("已取消刪除")

        elif edit_opt == "4" or edit_opt == "":
            print("已取消編輯")
        else:
            print("選項錯誤")

        if edit_opt in ["1", "2", "3"] and edit_opt != "4":
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump(tasks, f, ensure_ascii=False, indent=4)

    # 4. 查看所有任務
    elif choice == "4":
        if not tasks:
            print("清單中沒有任務")
        else:
            print("\n目前所有任務：")
            for task in tasks:
                print(f"{task['id']}. {task['task']}：{task['status']} (截止日期: {task['deadline']})")

    # 5. 退出
    elif choice == "5":
        print("謝謝使用！再見！")
        break

    else:
        print("請輸入 1-5 的數字！")