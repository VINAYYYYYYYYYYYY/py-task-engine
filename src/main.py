import sqlite3
import argparse
import sys
from datetime import datetime

class TaskManager:
    def __init__(self, db_path='tasks.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def add_task(self, title):
        with self.conn:
            self.conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
            print(f"Task '{title}' added.")

    def list_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title, status FROM tasks')
        for row in cursor.fetchall():
            print(f"[{row[0]}] {row[1]} - {row[2]}")

    def complete_task(self, task_id):
        with self.conn:
            self.conn.execute('UPDATE tasks SET status = "completed" WHERE id = ?', (task_id,))
            print(f"Task {task_id} marked as completed.")

def main():
    parser = argparse.ArgumentParser(description="Advanced Python Task Engine")
    parser.add_argument('action', choices=['add', 'list', 'done'])
    parser.add_argument('--title', help="Task title")
    parser.add_argument('--id', type=int, help="Task ID")

    args = parser.parse_args()
    tm = TaskManager()

    if args.action == 'add' and args.title:
        tm.add_task(args.title)
    elif args.action == 'list':
        tm.list_tasks()
    elif args.action == 'done' and args.id:
        tm.complete_task(args.id)

if __name__ == "__main__":
    main()
