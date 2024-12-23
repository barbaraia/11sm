import csv
import json
from datetime import datetime

class Task:
    def __init__(self, id, title, description, done=False, priority="Средний", due_date=None):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date or datetime.now().strftime("%d-%m-%Y")

    def load_tasks(self):
        try:
            with open('tasks.json', "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open('tasks.json', "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

    def __str__(self):
        return f"Title: {self.title}, Done: {self.done}, Priority: {self.priority}, Due: {self.due_date}"


    def add_task(self, title, description="", priority="Средний", due_date=None):
        task_id = max((task["id"] for task in self.tasks), default=0) + 1
        new_task = {
            "id": task_id,
            "title": title,
            "description": description,
            "done": False,
            "priority": priority,
            "due_date": due_date
        }
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def list_tasks(self):
        return self.tasks

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def mark_task_done(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task["done"] = True
            self.save_tasks()
            return task
        return None

    def edit_task(self, task_id, new_title=None, new_description=None, new_priority=None, new_due_date=None):
        task = self.get_task_by_id(task_id)
        if task:
            if new_title:
                task["title"] = new_title
            if new_description:
                task["description"] = new_description
            if new_priority:
                task["priority"] = new_priority
            if new_due_date:
                task["due_date"] = new_due_date
            self.save_tasks()
            return task
        return None

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()

    def export_to_csv(self, file_name):
        with open(file_name, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "title", "description", "done", "priority", "due_date"])
            for task in self.tasks:
                writer.writerow([task["id"], task["title"], task["description"], task["done"], task["priority"], task["due_date"]])

    def filter_tasks(self, status=None, priority=None, due_date=None):
        filtered_tasks = self.tasks
        if status is not None:
            filtered_tasks = [task for task in filtered_tasks if task["done"] == status]
        if priority:
            filtered_tasks = [task for task in filtered_tasks if task["priority"] == priority]
        if due_date:
            filtered_tasks = [task for task in filtered_tasks if task["due_date"] == due_date]
        return filtered_tasks