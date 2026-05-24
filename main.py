
import mysql.connector

# ---------------- DB ----------------
class DB:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "12345671"
        )

        cursor = self.mydb.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS todo_list")
        cursor.execute("USE todo_list")

# ---------------- SETUP ----------------
class SetUp:
    def __init__(self, db):
        cursor = db.mydb.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(111)
            )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            task_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            user_id INT, 
            status VARCHAR(30),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """)

        db.mydb.commit()
        cursor.close()

# ---------------- REPOSITORY ----------------
class TaskRepository:
    def __init__(self, db):
        self.db = db

    def create_user(self, name):
        cursor = self.db.mydb.cursor()

        cursor.execute("""
            INSERT INTO users (name )VALUES (%s)
        """, (name, ))
        self.db.mydb.commit()
        cursor.close()

    def read_user(self):
        cursor = self.db.mydb.cursor()

        cursor.execute("SELECT * FROM users")
        res = cursor.fetchall()
        cursor.close()
        return res

    def user_exists(self, user_id):
        cursor = self.db.mydb.cursor()

        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        res = cursor.fetchone()
        cursor.close()
        return res is not None

    def create_task(self, title, user_id):
        if not self.user_exists(user_id):
            return False

        cur = self.db.mydb.cursor()
        cur.execute(
            "INSERT INTO tasks (title, user_id, status) VALUES (%s, %s, %s)",
            (title, user_id, "In Progress")
        )
        self.db.mydb.commit()
        cur.close()
        return True

    def read_tasks(self, user_id):
        cursor = self.db.mydb.cursor()

        cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
        res = cursor.fetchall()
        cursor.close()
        return res

    def read_all(self):
        cursor = self.db.mydb.cursor()

        cursor.execute("""
        SELECT tasks.task_id,
               tasks.title,
               tasks.user_id,
               tasks.status,
               users.name
        FROM tasks
        JOIN users
        ON tasks.user_id = users.user_id
        """)
        res = cursor.fetchall()
        cursor.close()
        return res

    def delete_task(self, task_id):
        cursor = self.db.mydb.cursor()
        cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id, ))
        self.db.mydb.commit()
        cursor.close()

    def mark_done(self, task_id):
        cursor = self.db.mydb.cursor()

        cursor.execute("UPDATE tasks SET status = %s WHERE task_id = %s", ("DONE", task_id, ))
        self.db.mydb.commit()
        cursor.close()

# ---------------- CLEANUP ----------------
def on_exit_cleanup(db):
    cursor = db.mydb.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("DROP TABLE IF EXISTS tasks")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.mydb.commit()
    cursor.close()

# ---------------- MAIN ----------------
def main():
    db = DB()
    SetUp(db)
    rep = TaskRepository(db)

    print("\n" + "-" * 60)
    print("🚀 TO DO APP V2.0 🚀")
    print("-" * 60)

    while True:
        print("\n📌MENU")
        print("-" * 60)
        print("1. Create user")
        print("2. Create task")
        print("3. View users")
        print("4. View tasks by users")
        print("5. View all data")
        print("6. Delete task")
        print("7. Mark done")
        print("8. Exit")
        print("-" * 60)

        choice = input("👉 Choose:")

        # ---------------- CREATE USER ----------------
        if choice == "1":
            name = input("👤 User name: ")
            rep.create_user(name)
            print(f"✅ User '{name}' created")

        # ---------------- CREATE TASK ----------------
        elif choice == "2":
            title = input("📝 Task title: ")
            user_id = int(input("👤 User ID: "))

            if rep.create_task(title, user_id):
                print("✅ Task is created")

            else:
                print("❌ User not found")

        # ---------------- USERS ----------------
        elif choice == "3":
            print("\n" + "=" * 40)
            print("👤 Users")
            print("=" * 40)

            users = rep.read_user()

            print(f"{'ID':<5} {'NAME'}")
            print("-" * 40)

            for user in users:
                print(f"{user[0]:<5} {user[1]}")

            print("-" * 40)
            print(f"Total: {len(users)} users")

        # ---------------- TASKS BY USER ----------------
        elif choice == "4":
            user_id = input("👤Enter user ID: ")
            tasks = rep.read_tasks(user_id)

            print("\n" + "=" * 40)
            print(f"Tasks for user {user_id}")
            print("=" * 40)

            if not rep.user_exists(user_id):
                print("❌ No tasks found")

            else:
                print(f"{'ID':<5} {'TITLE'}")
                print("-" * 40)

                for task in tasks:
                    print(f"{task[0]:<5} {task[1]} {task[2]}")
                print("-" * 40)
                print(f"Total: {len(tasks)} tasks")

        # ---------------- ALL DATA ----------------
        elif choice == "5":
            rows = rep.read_all()
            print("\n" + "=" * 70)
            print("📊 ALL DATA")
            print("=" * 70)

            print(f"{'ID':<5} {'TITLE':<20} {'USER':<6} {'STATUS':<12} {'NAME'}")
            print("-" * 70)
            for r in rows:
                print(f"{r[0]:<5} {r[1]:<20} {r[2]:<6} {r[3]:<12} {r[4]}")
            print("-" * 70)
            print(f"Total: {len(rows)} records")

        # ---------------- DELETE ----------------
        elif choice == "6":
            task_id = int(input("Task ID: "))
            rep.delete_task(task_id)
            print(f"🗑 Task {task_id} deleted")

        # ---------------- DONE ----------------
        elif choice == "7":
            task_id = int(input("Task ID: "))
            rep.mark_done(task_id)
            print(f"✅ Task {task_id} marked DONE")

        # ---------------- EXIT ----------------
        elif choice == "8":
            on_exit_cleanup(db)
            print("\n👋 Bye! Database cleared.")
            break

        else:
            print("❌Invalid choice")


if __name__ == "__main__":
    main()





