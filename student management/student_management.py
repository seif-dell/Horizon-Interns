"""Student Management System with file-based storage (JSON)."""

import json
import os

DATA_FILE = "students.json"


class StudentManager:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.students = self.load()

    # ---------- storage ----------
    def load(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print("! Could not read data file, starting with an empty list.")
            return []

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.students, f, indent=2, ensure_ascii=False)

    # ---------- helpers ----------
    def find(self, student_id):
        for s in self.students:
            if s["id"] == student_id:
                return s
        return None

    # ---------- operations ----------
    def add(self, student_id, name, age, major, grade):
        if self.find(student_id):
            return False
        self.students.append(
            {"id": student_id, "name": name, "age": age,
             "major": major, "grade": grade}
        )
        self.save()
        return True

    def search(self, term):
        term = term.lower()
        return [s for s in self.students
                if term == s["id"].lower() or term in s["name"].lower()]

    def update(self, student_id, **changes):
        student = self.find(student_id)
        if not student:
            return False
        student.update({k: v for k, v in changes.items() if v is not None})
        self.save()
        return True

    def delete(self, student_id):
        student = self.find(student_id)
        if not student:
            return False
        self.students.remove(student)
        self.save()
        return True

    def statistics(self):
        if not self.students:
            return None
        grades = [s["grade"] for s in self.students]
        best = max(self.students, key=lambda s: s["grade"])
        return {"count": len(grades), "average": sum(grades) / len(grades),
                "highest": best}


# ---------- input helpers ----------
def ask_text(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("  ! This field cannot be empty.")


def ask_number(prompt, cast, low, high, allow_empty=False):
    while True:
        raw = input(prompt).strip()
        if raw == "" and allow_empty:
            return None
        try:
            value = cast(raw)
            if low <= value <= high:
                return value
            print(f"  ! Enter a value between {low} and {high}.")
        except ValueError:
            print("  ! Invalid number.")


def print_table(students):
    if not students:
        print("  (no students found)")
        return
    print(f"\n{'ID':<8}{'Name':<22}{'Age':<6}{'Major':<18}{'Grade':<6}")
    print("-" * 60)
    for s in students:
        print(f"{s['id']:<8}{s['name']:<22}{s['age']:<6}"
              f"{s['major']:<18}{s['grade']:<6}")


MENU = """
===== STUDENT MANAGEMENT SYSTEM =====
 1. Add student
 2. View all students
 3. Search student (ID or name)
 4. Update student
 5. Delete student
 6. Statistics
 0. Exit
=====================================
"""


def main():
    manager = StudentManager()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            sid = ask_text("  ID: ")
            if manager.find(sid):
                print("  ! A student with this ID already exists.")
                continue
            name = ask_text("  Name: ")
            age = ask_number("  Age (15-100): ", int, 15, 100)
            major = ask_text("  Major: ")
            grade = ask_number("  Grade (0-20): ", float, 0, 20)
            manager.add(sid, name, age, major, grade)
            print("  Student added.")

        elif choice == "2":
            print_table(manager.students)

        elif choice == "3":
            print_table(manager.search(ask_text("  Search term: ")))

        elif choice == "4":
            sid = ask_text("  ID of student to update: ")
            if not manager.find(sid):
                print("  ! Student not found.")
                continue
            print("  Leave a field empty to keep its current value.")
            name = ask_text("  New name: ", allow_empty=True) or None
            age = ask_number("  New age: ", int, 15, 100, allow_empty=True)
            major = ask_text("  New major: ", allow_empty=True) or None
            grade = ask_number("  New grade: ", float, 0, 20, allow_empty=True)
            manager.update(sid, name=name, age=age, major=major, grade=grade)
            print("  Student updated.")

        elif choice == "5":
            sid = ask_text("  ID of student to delete: ")
            if manager.find(sid):
                confirm = input("  Are you sure? (y/n): ").strip().lower()
                if confirm == "y":
                    manager.delete(sid)
                    print("  Student deleted.")
            else:
                print("  ! Student not found.")

        elif choice == "6":
            stats = manager.statistics()
            if stats is None:
                print("  (no data yet)")
            else:
                print(f"  Students : {stats['count']}")
                print(f"  Average  : {stats['average']:.2f}")
                top = stats["highest"]
                print(f"  Top grade: {top['name']} ({top['grade']})")

        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("  ! Invalid option.")


if __name__ == "__main__":
    main()
