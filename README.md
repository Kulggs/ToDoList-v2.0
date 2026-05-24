📝 ToDo List App (MySQL + Python)

A simple command-line To-Do List application built with Python and MySQL. The project demonstrates basic CRUD operations, relational database design, and user/task management.

🚀 Features

Create users, create tasks for users, view users, view tasks by user, view all data with JOIN, delete tasks, mark tasks as DONE. The database is created automatically and uses foreign keys between users and tasks.

🛠️ Tech Stack

Python 3, MySQL, mysql-connector-python.

🗄️ Database Structure

Users table: user_id (PK, AUTO_INCREMENT), name (VARCHAR)
Tasks table: task_id (PK, AUTO_INCREMENT), title (VARCHAR), user_id (FK → users.user_id), status (VARCHAR)

▶️ How to Run
Install dependency: pip install mysql-connector-python
Make sure MySQL is running with:
host="localhost", user="root", password="12345671"
Run project: python main.py
📌 Example Usage
Create user
Create task
View users
View tasks by user
View all data
Delete task
Mark done
Exit
