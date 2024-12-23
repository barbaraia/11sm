import json
import csv
from datetime import datetime


class Note:
    def __init__(self, id, title, content, timestamp=None):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def __str__(self):
        return f"{self.title} ({self.timestamp})\n{self.content}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data):
        return Note(
            data["id"],
            data["title"],
            data["content"],
            data["timestamp"]
        )

    def load_notes(self):
        try:
            with open('notes.json', "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Note.from_dict(note) for note in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_notes(self):
        with open('notes.json', "w", encoding="utf-8") as f:
            json.dump([note.to_dict() for note in self.load_notes()], f, indent=4, ensure_ascii=False)

    def edit_note(self, note_id, new_title=None, new_content=None):
        note = self.get_note_by_id(note_id)
        if note:
            if new_title:
                note.title = new_title
            if new_content:
                note.content = new_content
            note.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_notes()
            return note
        return None

    def delete_note(self, note_id):
        self.load_notes = [note for note in self.load_notes if note.id != note_id]
        self.save_notes()

    def export_to_csv(self, file_name):
        with open(file_name, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "title", "content", "timestamp"])
            for note in self.load_notes:
                writer.writerow([note.id, note.title, note.content, note.timestamp])

    def import_from_csv(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.create_note(
                    title=row["title"],
                    content=row["content"]
                )

    def list_notes(self):
        return self.load_notes

    def get_note_by_id(self, note_id):
        for note in self.load_notes:
            if note.id == note_id:
                return note
        return None

    def create_note(self, title, content):
        note_id = max((note.id for note in self.load_notes), default=0) + 1
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        new_note = Note(note_id, title, content, timestamp)
        self.load_notes.append(new_note)
        self.save_notes()
        return new_note
