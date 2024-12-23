import json
import csv
from datetime import datetime
from FinanceRecord import FinanceRecord
from Calculator import Calculator
from Contact import Contact
from Note import Note
from Task import Task


class PersonalAssistant:
    def __init__(self):
        self.notes = []
        self.tasks = []
        self.contacts = []
        self.finance_records = []
        self.load_data()

    def load_data(self):
        try:
            with open("notes.json", "r") as file:
                self.notes = json.load(file)
        except FileNotFoundError:
            self.notes = []

        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

        try:
            with open("contacts.json", "r") as file:
                self.contacts = json.load(file)
        except FileNotFoundError:
            self.contacts = []

        try:
            with open("finance.json", "r") as file:
                self.finance_records = json.load(file)
        except FileNotFoundError:
            self.finance_records = []

    def save_data(self):
        with open("notes.json", "w") as file:
            json.dump(self.notes, file)

        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

        with open("contacts.json", "w") as file:
            json.dump(self.contacts, file)

        with open("finance.json", "w") as file:
            json.dump(self.finance_records, file)

    def manage_notes(self):
        while True:
            print("\n1. Создать новую заметку")
            print("2. Просмотр всех заметок")
            print("3. Редактировать заметку")
            print("4. Удалить заметку")
            print("5. Экспортировать заметки в CSV")
            print("6. Назад")

            choice = input("Выберите действие: ")

            if choice == "1":
                title = input("Введите заголовок заметки: ")
                content = input("Введите содержимое заметки: ")
                note_id = len(self.notes) + 1
                note = Note(note_id, title, content)
                self.notes.append(note.__dict__)
                self.save_data()
                print("Заметка добавлена.")

            elif choice == "2":
                for note in self.notes:
                    print(f"{note['id']}. {note['title']} ({note['timestamp']})")

            elif choice == "3":
                note_id = int(input("Введите ID заметки для редактирования: "))
                note = next((note for note in self.notes if note["id"] == note_id), None)
                if note:
                    note["title"] = input(f"Новый заголовок ({note['title']}): ")
                    note["content"] = input(f"Новое содержимое ({note['content']}): ")
                    note["timestamp"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    self.save_data()
                    print("Заметка обновлена.")
                else:
                    print("Заметка не найдена.")

            elif choice == "4":
                note_id = int(input("Введите ID заметки для удаления: "))
                self.notes = [note for note in self.notes if note["id"] != note_id]
                self.save_data()
                print("Заметка удалена.")

            elif choice == "5":
                with open("notes.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["id", "title", "content", "timestamp"])
                    writer.writeheader()
                    for note in self.notes:
                        writer.writerow(note)
                print("Заметки экспортированы в notes.csv.")

            elif choice == "6":
                break

    def manage_tasks(self):
        while True:
            print("\n1. Создать новую задачу")
            print("2. Просмотр всех задач")
            print("3. Отметить задачу как выполненную")
            print("4. Редактировать задачу")
            print("5. Удалить задачу")
            print("6. Экспортировать задачи в CSV")
            print("7. Назад")

            choice = input("Выберите действие: ")

            if choice == "1":
                title = input("Введите название задачи: ")
                description = input("Введите описание задачи: ")
                priority = input("Введите приоритет (Высокий, Средний, Низкий): ")
                due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")
                task_id = len(self.tasks) + 1
                task = Task(task_id, title, description, priority=priority, due_date=due_date)
                self.tasks.append(task.__dict__)
                self.save_data()
                print("Задача добавлена.")

            elif choice == "2":
                for task in self.tasks:
                    print(f"{task['id']}. {task['title']} - {task['done']}")

            elif choice == "3":
                task_id = int(input("Введите ID задачи для отметки как выполненной: "))
                task = next((task for task in self.tasks if task["id"] == task_id), None)
                if task:
                    task["done"] = True
                    self.save_data()
                    print("Задача отмечена как выполненная.")
                else:
                    print("Задача не найдена.")

            elif choice == "4":
                task_id = int(input("Введите ID задачи для редактирования: "))
                task = next((task for task in self.tasks if task["id"] == task_id), None)
                if task:
                    task["title"] = input(f"Новый заголовок ({task['title']}): ")
                    task["description"] = input(f"Новое описание ({task['description']}): ")
                    task["priority"] = input(f"Новый приоритет ({task['priority']}): ")
                    task["due_date"] = input(f"Новый срок выполнения ({task['due_date']}): ")
                    self.save_data()
                    print("Задача обновлена.")
                else:
                    print("Задача не найдена.")

            elif choice == "5":
                task_id = int(input("Введите ID задачи для удаления: "))
                self.tasks = [task for task in self.tasks if task["id"] != task_id]
                self.save_data()
                print("Задача удалена.")

            elif choice == "6":
                with open("tasks.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["id", "title", "description", "done", "priority", "due_date"])
                    writer.writeheader()
                    for task in self.tasks:
                        writer.writerow(task)
                print("Задачи экспортированы в tasks.csv.")

            elif choice == "7":
                break

    def manage_contacts(self):
        while True:
            print("\n1. Добавить новый контакт")
            print("2. Просмотр всех контактов")
            print("3. Редактировать контакт")
            print("4. Удалить контакт")
            print("5. Экспортировать контакты в CSV")
            print("6. Назад")

            choice = input("Выберите действие: ")

            if choice == "1":
                name = input("Введите имя контакта: ")
                phone = input("Введите номер телефона: ")
                email = input("Введите email: ")
                contact_id = len(self.contacts) + 1
                contact = Contact(contact_id, name, phone, email)
                self.contacts.append(contact.__dict__)
                self.save_data()
                print("Контакт добавлен.")

            elif choice == "2":
                for contact in self.contacts:
                    print(f"{contact['id']}. {contact['name']} ({contact['phone']}, {contact['email']})")

            elif choice == "3":
                contact_id = int(input("Введите ID контакта для редактирования: "))
                contact = next((contact for contact in self.contacts if contact["id"] == contact_id), None)
                if contact:
                    contact["name"] = input(f"Новое имя ({contact['name']}): ")
                    contact["phone"] = input(f"Новый телефон ({contact['phone']}): ")
                    contact["email"] = input(f"Новый email ({contact['email']}): ")
                    self.save_data()
                    print("Контакт обновлен.")
                else:
                    print("Контакт не найден.")

            elif choice == "4":
                contact_id = int(input("Введите ID контакта для удаления: "))
                self.contacts = [contact for contact in self.contacts if contact["id"] != contact_id]
                self.save_data()
                print("Контакт удалён.")

            elif choice == "5":
                with open("contacts.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["id", "name", "phone", "email"])
                    writer.writeheader()
                    for contact in self.contacts:
                        writer.writerow(contact)
                print("Контакты экспортированы в contacts.csv.")

            elif choice == "6":
                break

    def manage_finances(self):
        while True:
            print("\n1. Добавить финансовую запись")
            print("2. Просмотр всех записей")
            print("3. Экспортировать записи в CSV")
            print("4. Назад")

            choice = input("Выберите действие: ")

            if choice == "1":
                amount = float(input("Введите сумму операции: "))
                category = input("Введите категорию операции: ")
                date = input("Введите дату операции (ДД-ММ-ГГГГ): ")
                description = input("Введите описание операции: ")
                record_id = len(self.finance_records) + 1
                finance_record = FinanceRecord(record_id, amount, category, date, description)
                self.finance_records.append(finance_record.__dict__)
                self.save_data()
                print("Финансовая запись добавлена.")

            elif choice == "2":
                for record in self.finance_records:
                    print(
                        f"{record['id']}. {record['amount']} {record['category']} {record['date']} {record['description']}")

            elif choice == "3":
                with open("finance.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["id", "amount", "category", "date", "description"])
                    writer.writeheader()
                    for record in self.finance_records:
                        writer.writerow(record)
                print("Финансовые записи экспортированы в finance.csv.")

            elif choice == "4":
                break

    def calculator(self):
        while True:
            print("\n1. Сложение")
            print("2. Вычитание")
            print("3. Умножение")
            print("4. Деление")
            print("5. Назад")

            choice = input("Выберите действие: ")

            if choice == "1":
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))
                print(f"Результат: {num1 + num2}")

            elif choice == "2":
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))
                print(f"Результат: {num1 - num2}")

            elif choice == "3":
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))
                print(f"Результат: {num1 * num2}")

            elif choice == "4":
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))
                if num2 != 0:
                    print(f"Результат: {num1 / num2}")
                else:
                    print("Ошибка: деление на ноль.")

            elif choice == "5":
                break

    def main_menu(self):
        while True:
            print("\nДобро пожаловать в Персональный помощник!")
            print("Выберите действие:")
            print("1. Управление заметками")
            print("2. Управление задачами")
            print("3. Управление контактами")
            print("4. Управление финансовыми записями")
            print("5. Калькулятор")
            print("6. Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.manage_notes()
            elif choice == "2":
                self.manage_tasks()
            elif choice == "3":
                self.manage_contacts()
            elif choice == "4":
                self.manage_finances()
            elif choice == "5":
                self.calculator()
            elif choice == "6":
                print("Выход из программы.")
                break
            else:
                print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    app = PersonalAssistant()
    app.main_menu()