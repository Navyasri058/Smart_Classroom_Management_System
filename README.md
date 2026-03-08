# Smart_Classroom_Management_System
Smart Classroom Management System using Fron-end: HTML&CSS , Back-end: python using Flask and MongoDB for data storing

## Overview

The Smart Classroom Management System is a web-based application developed using **Python, Flask, and MongoDB**.
It helps manage classroom activities such as student records, attendance, and classroom monitoring efficiently.

## Features

* Student management
* Attendance tracking
* Classroom data monitoring
* Web-based interface
* Database storage using MongoDB

## Technologies Used

* Python
* Flask
* MongoDB
* HTML
* CSS

## Project Structure

```
project-folder/
│
├── app.py
├── templates/
├── static/
├── database/
└── README.md
```

## Installation

1. Clone the repository

```
git clone https://github.com/username/smart-classroom-management-system.git
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Run the project

```
python app.py
```

## Future Improvements

* IoT integration
* Real-time classroom monitoring
* Dashboard analytics

## MongoDB Database Setup

This project uses **MongoDB** as the database to store student records, attendance data, and academic results.

### Database Connection

The application connects to MongoDB using **PyMongo**.

Example connection used in the project:

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["student_management"]
collection = db["students"]
```

### Collection Used

The project uses **one main collection**:

**Collection Name:** `students`

This collection stores:

* Student personal details
* Attendance records
* Academic marks
* Final results

### Example Student Document

```json
{
  "ROLL NO": "21CS101",
  "NAME": "NAVYA",
  "BRANCH": "CSE",
  "PHONE NO": "9876543210",
  "PRESENT_COUNT": 10,
  "ABSENT_COUNT": 2,
  "DBMS": 85,
  "DLCO": 78,
  "P&S": 80,
  "ML": 90,
  "OT": 75,
  "TOTAL MARKS": 408,
  "PERCENTAGE": 81.6,
  "GRADE": "B",
  "RESULT": "Pass"
}
```

### Features Using MongoDB

The database is used for the following operations:

* Add new students
* Store student personal details
* Track attendance (Present / Absent count)
* Store academic marks
* Calculate percentage and grade
* Generate student reports
* Generate class reports

### MongoDB Installation

1. Download MongoDB Community Server
   https://www.mongodb.com/try/download/community

2. Install MongoDB

3. Start the MongoDB server

4. Run the Flask application

```bash
python app.py
```

The application will automatically create the database and collection when the first student is added.

FLOW CHART :

Teacher / Student
        ↓
     Flask App
        ↓
     MongoDB
        ↓
   students collection
        ↓
Student Info + Attendance + Academics


## Author

Navya Sri

