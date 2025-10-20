# 📝 Productive To-Do (PySide6)

A modern, elegant, and productivity-focused **To-Do application** built using **Python (PySide6)** and **QtAwesome** icons.  
It helps you manage your daily tasks efficiently with a clean interface, smooth animations, light/dark themes, and persistent storage via JSON.

---

## 🚀 Features

### ✅ Core Functionalities
- **Add New Tasks:** Quickly add tasks by pressing **Enter** or clicking the **Add Task** button.  
- **Mark as Completed:** Check off tasks as you complete them (with strikethrough text and style updates).  
- **Edit Tasks:** Update task names anytime using the edit (✏️) button.  
- **Delete Tasks:** Remove tasks individually using the trash (🗑) button.  
- **Persistent Storage:** All tasks are automatically saved in a JSON file and reloaded on app startup.

### 🔍 Task Filtering & Search
- **All / Pending / Completed Filters:** Easily view specific categories of your tasks.
- **Search Bar:** Instantly find any task by typing part of its name.

### 🧹 Productivity Tools
- **Clear Completed:** Remove all completed tasks at once.
- **Auto-Cleanup:** Automatically delete completed tasks older than 30 days.
- **Motivational Daily Quote:** A random quote that changes daily to keep you inspired.

### 🎨 Themes & Design
- **Light and Dark Modes:** Toggle between dark and light UI themes using the sun/moon icon.
- **Smooth Fade Animations:** Tasks fade in with subtle transitions for a premium feel.
- **Clean, Minimal UI:** Built with modern typography, rounded cards, and soft hover effects.

---

## 📁 File Structure

- `todo_pyside_advanced.py` # Main application file
- `todos.json` # JSON file used to store your tasks (auto-created)

> By default, the todos file path is set to:
> ```
> C:\Users\Muhammad Hamza\todos.json
> ```
> You can modify this path in the code by editing the line:
> ```python
> TODOS_FILE = r"C:\Users\Muhammad Hamza\todos.json"
> ```

---

## 🛠 Installation & Setup

### 1. Install Python
Make sure Python **3.8 or higher** is installed on your system.  
You can verify this by running:
```bash
python --version
```

### 2. Install Required Packages
Run the following commands in your terminal:
```bash
pip install PySide6 qtawesome
```

### 3. (Optional) Create a Virtual Environment
It’s recommended to use a virtual environment to isolate dependencies:
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On macOS/Linux
```

### ▶️ Running the Application
Navigate to the folder where `todo_pyside_advanced.py` is saved.

Run the script with:
```bash
python todo_pyside_advanced.py
```

The main window titled “Productive To-Do” will appear.

---

## 💡 How to Use

### ➕ Add a Task
Type your task in the input field and press Enter or click Add Task.

The task will appear instantly in your list.

### 🗂 Filter Tasks
Use the buttons:
- **All** – View every task
- **Pending** – View only incomplete tasks
- **Completed** – View finished tasks

### ✏️ Edit a Task
Click the edit icon (✏️) beside any task, modify the text, and press Save.

### 🗑 Delete a Task
Click the trash icon (🗑) beside a task to delete it after confirmation.

### 🌗 Toggle Theme
Click the sun/moon icon in the top-right corner to switch between dark and light modes.

### 🔄 Auto-Cleanup
Click the **Auto-clean (30+ days)** button to automatically remove old completed tasks.

### 🧠 Data Persistence
All your tasks are stored in a simple JSON file (`todos.json`) located at:
```
C:\Users\Muhammad Hamza\todos.json
```

Each task entry is saved in the following structure:
```json
{
  "id": 1,
  "task": "Buy groceries",
  "completed": false,
  "created_at": "2025-10-20T10:45:12.345678"
}
```
This ensures that your data is automatically reloaded the next time you launch the app.

---

## ⚙️ Technical Overview
- **Framework:** PySide6 (Qt for Python)
- **Icons:** QtAwesome (Font Awesome 5)
- **Data Storage:** JSON file
- **Animation:** QPropertyAnimation for fade-in effects
- **UI Design:** Dynamic QSS (Qt Stylesheets) for light/dark themes

---

## 🧩 Customization
You can easily:
- Change color schemes or fonts by editing the stylesheet strings inside `setup_styles()` method.
- Modify quotes in the `QUOTES` list.
- Change cleanup duration by editing:
  ```python
  cleanup_btn.clicked.connect(lambda: self.auto_cleanup(days=30))
  ```

---

## 💬 Example Screenshots (optional)
You can include screenshots of dark and light modes here once captured.

---

## 👨‍💻 Author
**Muhammad Hamza Yousaf**  
💬 Passionate about coding, productivity tools, and creative app development.

---

## 🪪 License
This project is open-source and free to use for educational and personal purposes.  
Feel free to modify and enhance it as you wish.
