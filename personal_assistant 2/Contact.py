import json
import csv
import os

class Contact:
    def __init__(self, id, name, phone, email, storage_file="contacts.json"):
            self.id = id
            self.name = name
            self.phone = phone
            self.email = email
            self.storage_file = storage_file
            self.contacts = self._load_contacts()

    def __str__(self):
            return f"{self.name} ({self.phone}, {self.email})"

    def _load_contacts(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as file:
                return {contact['id']: ContactData(**contact) for contact in json.load(file)}
        return {}

    def _save_contacts(self):
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([contact.to_dict() for contact in self.contacts.values()], file, indent=4)

    def add_contact(self, name, phone, email):
        contact_id = max(self.contacts.keys(), default=0) + 1
        new_contact = ContactData(contact_id, name, phone, email)
        self.contacts[contact_id] = new_contact
        self._save_contacts()
        return new_contact

    def edit_contact(self, contact_id, name=None, phone=None, email=None):
        contact = self.contacts.get(contact_id)
        if contact:
            contact.name = name or contact.name
            contact.phone = phone or contact.phone
            contact.email = email or contact.email
            self._save_contacts()
            return contact
        return None

    def delete_contact(self, contact_id):
        if contact_id in self.contacts:
            del self.contacts[contact_id]
            self._save_contacts()
            return True
        return False

    def find_contact(self, search_term):
        found_contacts = []
        for contact in self.contacts.values():
            if search_term.lower() in contact.name.lower() or search_term in contact.phone:
                found_contacts.append(contact)
        return found_contacts

    def export_to_csv(self, filename="contacts.csv"):
        with open(filename, mode='w', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name", "phone", "email"])
            writer.writeheader()
            for contact in self.contacts.values():
                writer.writerow(contact.to_dict())

    def import_from_csv(self, filename="contacts.csv"):
        with open(filename, mode='r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_contact(row["name"], row["phone"], row["email"])

    def list_contacts(self):
        return list(self.contacts.values())

class ContactData:
    def __init__(self, id, name, phone, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }
