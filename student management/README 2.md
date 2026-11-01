# Student Management System

A command-line Python app to manage student records with persistent file-based storage (JSON).

## Features
- Add, view, search (by ID or name), update and delete students
- Data saved automatically to `students.json`, so it persists between runs
- Input validation (no empty fields, valid age and grade ranges, unique IDs)
- Statistics: number of students, average grade, top student
- Clean OOP design with a `StudentManager` class

## Requirements
Python 3.8+ (no external libraries).

## Run
```bash
python student_management.py
```

## Data format
```json
[
  {"id": "1", "name": "Ali", "age": 20, "major": "CS", "grade": 15.5}
]
```

## What I learned
File handling with JSON, CRUD operations, object-oriented design, and defensive input handling.

## Author
Built as part of the Python Development track at Horizon Intern.
