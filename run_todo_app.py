#!/usr/bin/env python3
"""
Todo Application Runner
This script demonstrates the todo functionality similar to the original console application
but now connects to the full backend API that was implemented.
"""

import requests
import json
import os
from typing import List, Dict, Optional

class TodoApp:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.username = None

    def signup(self, email: str, username: str, password: str) -> bool:
        """Sign up a new user"""
        url = f"{self.base_url}/api/auth/signup"
        data = {
            "email": email,
            "username": username,
            "password": password
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                user_data = response.json()
                print(f"✓ Successfully created user: {user_data['username']}")
                return True
            else:
                print(f"✗ Signup failed: {response.json().get('detail', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False

    def signin(self, email: str, password: str) -> bool:
        """Sign in an existing user"""
        url = f"{self.base_url}/api/auth/signin"
        data = {
            "email": email,
            "password": password
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                auth_data = response.json()
                self.token = auth_data['access_token']
                self.user_id = auth_data['user']['id']
                self.username = auth_data['user']['username']
                print(f"✓ Successfully signed in as: {self.username}")
                return True
            else:
                print(f"✗ Signin failed: {response.json().get('detail', 'Invalid credentials')}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False

    def signout(self):
        """Sign out the current user"""
        if not self.token:
            print("✗ Not signed in")
            return False

        url = f"{self.base_url}/api/auth/signout"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                print("✓ Successfully signed out")
                self.token = None
                self.user_id = None
                self.username = None
                return True
            else:
                print("✗ Signout failed")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False

    def get_todos(self) -> List[Dict]:
        """Get all todos for the current user"""
        if not self.token:
            print("✗ Not signed in")
            return []

        url = f"{self.base_url}/api/todos"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"✗ Failed to get todos: {response.json().get('detail', 'Error')}")
                return []
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return []

    def add_todo(self, title: str, description: str = "") -> bool:
        """Add a new todo"""
        if not self.token:
            print("✗ Not signed in")
            return False

        url = f"{self.base_url}/api/todos"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        data = {
            "title": title,
            "description": description,
            "completed": False
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                todo = response.json()
                print(f"✓ Added todo: {todo['title']}")
                return True
            else:
                print(f"✗ Failed to add todo: {response.json().get('detail', 'Error')}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False

    def update_todo(self, todo_id: str, title: str = None, description: str = None, completed: bool = None) -> bool:
        """Update an existing todo"""
        if not self.token:
            print("✗ Not signed in")
            return False

        url = f"{self.base_url}/api/todos/{todo_id}"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if completed is not None:
            data["completed"] = completed

        try:
            response = requests.put(url, headers=headers, json=data)
            if response.status_code == 200:
                todo = response.json()
                print(f"✓ Updated todo: {todo['title']}")
                return True
            else:
                print(f"✗ Failed to update todo: {response.json().get('detail', 'Error')}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False

    def toggle_todo(self, todo_id: str) -> bool:
        """Toggle the completion status of a todo"""
        if not self.token:
            print("✗ Not signed in")
            return False

        url = f"{self.base_url}/api/todos/{todo_id}/toggle-complete"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.patch(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                status = "completed" if result['completed'] else "not completed"
                print(f"✓ Todo marked as {status}")
                return True
            else:
                print(f"✗ Failed to toggle todo: {response.json().get('detail', 'Error')}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False

    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo"""
        if not self.token:
            print("✗ Not signed in")
            return False

        url = f"{self.base_url}/api/todos/{todo_id}"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                print("✓ Deleted todo")
                return True
            else:
                print(f"✗ Failed to delete todo: {response.json().get('detail', 'Error')}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False

    def print_todos(self):
        """Print all todos for the current user"""
        todos = self.get_todos()
        if not todos:
            print("No todos found.")
            return

        print(f"\nYour todos ({len(todos)}):")
        print("-" * 50)
        for i, todo in enumerate(todos, 1):
            status = "✓" if todo['completed'] else "○"
            print(f"{i}. [{status}] {todo['title']}")
            if todo['description']:
                print(f"    Description: {todo['description']}")
            print(f"    ID: {todo['id']}")
            print()

def main():
    print("=== Todo Application ===")
    print("Backend server should be running on http://localhost:8001")
    print("Frontend will be available on http://localhost:3000 when started\n")

    app = TodoApp()

    while True:
        print("\nOptions:")
        print("1. Sign up")
        print("2. Sign in")
        print("3. Sign out")
        print("4. List todos")
        print("5. Add todo")
        print("6. Toggle todo")
        print("7. Delete todo")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            email = input("Email: ")
            username = input("Username: ")
            password = input("Password: ")
            app.signup(email, username, password)

        elif choice == "2":
            email = input("Email: ")
            password = input("Password: ")
            app.signin(email, password)

        elif choice == "3":
            app.signout()

        elif choice == "4":
            if app.token:
                app.print_todos()
            else:
                print("Please sign in first.")

        elif choice == "5":
            if app.token:
                title = input("Todo title: ")
                description = input("Description (optional): ")
                app.add_todo(title, description if description else "")
            else:
                print("Please sign in first.")

        elif choice == "6":
            if app.token:
                app.print_todos()
                todos = app.get_todos()
                if todos:
                    try:
                        idx = int(input("Enter todo number to toggle: ")) - 1
                        if 0 <= idx < len(todos):
                            app.toggle_todo(todos[idx]['id'])
                        else:
                            print("Invalid todo number.")
                    except ValueError:
                        print("Please enter a valid number.")
            else:
                print("Please sign in first.")

        elif choice == "7":
            if app.token:
                app.print_todos()
                todos = app.get_todos()
                if todos:
                    try:
                        idx = int(input("Enter todo number to delete: ")) - 1
                        if 0 <= idx < len(todos):
                            app.delete_todo(todos[idx]['id'])
                        else:
                            print("Invalid todo number.")
                    except ValueError:
                        print("Please enter a valid number.")
            else:
                print("Please sign in first.")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()