import json
import csv
import os
from datetime import datetime

class FinanceRecord:
    def __init__(self, id, amount, category, date, description, storage_file="finance.json"):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
        self.storage_file = storage_file
        self.records = self._load_records()

    def __str__(self):
        return f"Amount: {self.amount}, Category: {self.category}, Date: {self.date}, Description: {self.description}"

    def _load_records(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as file:
                return {record['id']: FinanceData(**record) for record in json.load(file)}
        return {}

    def _save_records(self):
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([record.to_dict() for record in self.records.values()], file, indent=4)

    def add_record(self, amount, category, date, description):
        record_id = max(self.records.keys(), default=0) + 1
        new_record = FinanceData(record_id, amount, category, date, description)
        self.records[record_id] = new_record
        self._save_records()
        return new_record

    def get_all_records(self):
        return list(self.records.values())

    def get_filtered_records(self, date=None, category=None):
        filtered_records = []
        for record in self.records.values():
            if date and record.date != date:
                continue
            if category and record.category != category:
                continue
            filtered_records.append(record)
        return filtered_records

    def generate_report(self, start_date, end_date):
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
        report = []
        for record in self.records.values():
            record_date = datetime.strptime(record.date, "%d-%m-%Y")
            if start <= record_date <= end:
                report.append(record)
        return report

    def export_to_csv(self, filename="finance_records.csv"):
        with open(filename, mode='w', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "amount", "category", "date", "description"])
            writer.writeheader()
            for record in self.records.values():
                writer.writerow(record.to_dict())

    def import_from_csv(self, filename="finance_records.csv"):
        with open(filename, mode='r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_record(float(row["amount"]), row["category"], row["date"], row["description"])

    def calculate_balance(self):
        return sum(record.amount for record in self.records.values())

    def group_by_category(self):
        grouped = {}
        for record in self.records.values():
            if record.category not in grouped:
                grouped[record.category] = []
            grouped[record.category].append(record)
        return grouped

class FinanceData:
    def __init__(self, id, amount, category, date, description):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

