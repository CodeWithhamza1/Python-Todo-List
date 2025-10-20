# todo_pyside_advanced.py
import sys
import json
import qtawesome as qta
from datetime import date, datetime, timedelta
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QCheckBox, QMessageBox, QSizePolicy,
    QSpacerItem, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGraphicsOpacityEffect

TODOS_FILE = r"C:\Users\Muhammad Hamza\todos.json"

def load_todos():
    try:
        with open(TODOS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_todos(todos):
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f, indent=4)

# ---------- DAILY QUOTES ----------
QUOTES = [
    "Small steps every day — big changes over time.",
    "Do something today that your future self will thank you for.",
    "Focus on progress, not perfection.",
    "Clear tasks, clear mind. One thing at a time.",
    "Consistency beats intensity — show up.",
    "Make it simple. Start small. Finish strong."
]

def get_quote_of_day():
    idx = (date.today().toordinal() % len(QUOTES))
    return QUOTES[idx]


# ---------- CUSTOM CHECKBOX WITH STRIKETHROUGH ----------
class TaskCheckBox(QWidget):
    checked_changed = Signal(bool)

    def __init__(self, text, dark_mode, parent=None):
        super().__init__(parent)
        self.dark_mode = dark_mode
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.checkbox = QCheckBox()
        self.checkbox.setText("")
        self.checkbox.setFixedSize(24, 24)

        self.label = QLabel(text)
        self.label.setWordWrap(False)

        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.label, stretch=1)

        self.checkbox.stateChanged.connect(self.on_state_changed)
        self.update_styles()

    def on_state_changed(self, state):
        self.update_styles()
        self.checked_changed.emit(bool(state))

    def update_styles(self):
        if self.checkbox.isChecked():
            if self.dark_mode:
                self.label.setStyleSheet("color: #64748b; text-decoration: line-through; font-size: 14px; font-weight: 500;")
                self.checkbox.setStyleSheet("""
                    QCheckBox::indicator {
                        width: 20px;
                        height: 20px;
                        border-radius: 6px;
                        border: 2px solid #10b981;
                        background-color: #10b981;
                    }
                """)
            else:
                self.label.setStyleSheet("color: #94a3b8; text-decoration: line-through; font-size: 14px; font-weight: 500;")
                self.checkbox.setStyleSheet("""
                    QCheckBox::indicator {
                        width: 20px;
                        height: 20px;
                        border-radius: 6px;
                        border: 2px solid #10b981;
                        background-color: #10b981;
                    }
                """)
        else:
            if self.dark_mode:
                self.label.setStyleSheet("color: #e2e8f0; font-size: 14px; font-weight: 500;")
                self.checkbox.setStyleSheet("""
                    QCheckBox::indicator {
                        width: 20px;
                        height: 20px;
                        border-radius: 6px;
                        border: 2px solid #475569;
                        background-color: #1e293b;
                    }
                    QCheckBox::indicator:hover {
                        border-color: #10b981;
                        background-color: #334155;
                    }
                """)
            else:
                self.label.setStyleSheet("color: #0f172a; font-size: 14px; font-weight: 500;")
                self.checkbox.setStyleSheet("""
                    QCheckBox::indicator {
                        width: 20px;
                        height: 20px;
                        border-radius: 6px;
                        border: 2px solid #cbd5e1;
                        background-color: #ffffff;
                    }
                    QCheckBox::indicator:hover {
                        border-color: #10b981;
                        background-color: #f1f5f9;
                    }
                """)

    def isChecked(self):
        return self.checkbox.isChecked()

    def setChecked(self, checked):
        self.checkbox.setChecked(checked)


# ---------- MAIN APP WINDOW ----------
class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Productive To-Do")
        self.resize(750, 650)
        self.filter_mode = "all"
        self.search_text = ""
        self.dark_mode = True

        self.setup_styles()
        self.init_ui()
        self.load_tasks(animated=True)

    def setup_styles(self):
        dark_stylesheet = """
            QWidget {
                font-family: "Segoe UI", "SF Pro Display", Arial;
                font-size: 14px;
                color: #e2e8f0;
                background-color: #0f172a;
            }
            QLabel#title {
                font-size: 32px;
                font-weight: 700;
                color: white;
                background: transparent;
            }
            QLabel#quote {
                font-size: 14px;
                color: rgba(255, 255, 255, 0.8);
                font-style: italic;
                background: transparent;
            }
            QLineEdit {
                border: 2px solid #334155;
                border-radius: 12px;
                padding: 12px 16px;
                background-color: #1e293b;
                color: #e2e8f0;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
                background-color: #1e293b;
            }
            QPushButton {
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton#addBtn { 
                background-color: #10b981;
                color: white;
            }
            QPushButton#addBtn:hover { 
                background-color: #059669;
            }
            QPushButton#addBtn:pressed {
                background-color: #047857;
            }
            QPushButton#themeBtn { 
                background-color: #3b82f6;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton#themeBtn:hover {
                background-color: #2563eb;
            }
            QPushButton[filterSelected="true"] { 
                background-color: #3b82f6;
                color: white;
            }
            QPushButton[filterSelected="false"] { 
                background-color: transparent;
                color: #94a3b8;
            }
            QPushButton[filterSelected="false"]:hover {
                background-color: #1e293b;
                color: #e2e8f0;
            }
            QPushButton#actionBtn {
                background-color: #1e293b;
                color: #94a3b8;
                padding: 10px 16px;
            }
            QPushButton#actionBtn:hover {
                background-color: #334155;
                color: #e2e8f0;
            }
            QPushButton#editBtn {
                background-color: rgba(59, 130, 246, 0.1);
                border: 1px solid rgba(59, 130, 246, 0.3);
            }
            QPushButton#editBtn:hover {
                background-color: rgba(59, 130, 246, 0.2);
                border: 1px solid rgba(59, 130, 246, 0.5);
            }
            QPushButton#deleteBtn {
                background-color: rgba(239, 68, 68, 0.1);
                border: 1px solid rgba(239, 68, 68, 0.3);
            }
            QPushButton#deleteBtn:hover {
                background-color: rgba(239, 68, 68, 0.2);
                border: 1px solid rgba(239, 68, 68, 0.5);
            }
            QFrame#taskFrame {
                background-color: #1e293b;
                border-radius: 14px;
                border: 1px solid #334155;
            }
            QFrame#taskFrame:hover {
                background-color: #263548;
                border-color: #3b82f6;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #1e293b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #64748b;
            }
        """
        
        light_stylesheet = """
            QWidget { 
                background-color: #f8fafc;
                color: #0f172a;
                font-family: "Segoe UI", "SF Pro Display", Arial;
            }
            QLabel#title {
                color: #0f172a;
                background: transparent;
            }
            QLabel#quote {
                color: rgba(15, 23, 42, 0.7);
                background: transparent;
            }
            QLineEdit { 
                background-color: #ffffff;
                color: #0f172a;
                border: 2px solid #e2e8f0;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
            QPushButton#addBtn { 
                background-color: #10b981;
                color: white;
            }
            QPushButton#addBtn:hover { 
                background-color: #059669;
            }
            QPushButton#themeBtn { 
                background-color: #3b82f6;
                color: white;
            }
            QPushButton#themeBtn:hover {
                background-color: #2563eb;
            }
            QPushButton[filterSelected="true"] { 
                background-color: #3b82f6;
                color: white;
            }
            QPushButton[filterSelected="false"] { 
                background-color: transparent;
                color: #64748b;
            }
            QPushButton[filterSelected="false"]:hover {
                background-color: #e2e8f0;
                color: #0f172a;
            }
            QPushButton#actionBtn {
                background-color: #e2e8f0;
                color: #475569;
            }
            QPushButton#actionBtn:hover {
                background-color: #cbd5e1;
                color: #0f172a;
            }
            QPushButton#editBtn {
                background-color: rgba(59, 130, 246, 0.1);
                border: 1px solid rgba(59, 130, 246, 0.3);
            }
            QPushButton#editBtn:hover {
                background-color: rgba(59, 130, 246, 0.15);
            }
            QPushButton#deleteBtn {
                background-color: rgba(239, 68, 68, 0.1);
                border: 1px solid rgba(239, 68, 68, 0.3);
            }
            QPushButton#deleteBtn:hover {
                background-color: rgba(239, 68, 68, 0.15);
            }
            QFrame#taskFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
            }
            QFrame#taskFrame:hover {
                border-color: #3b82f6;
                background-color: #f8fafc;
            }
            QScrollBar:vertical {
                background-color: #e2e8f0;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """
        
        self.dark_stylesheet = dark_stylesheet
        self.light_stylesheet = light_stylesheet
        self.setStyleSheet(dark_stylesheet)

    def init_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(24, 24, 24, 24)
        main.setSpacing(20)

        # HEADER - Simple and Clean
        header = QVBoxLayout()
        header.setSpacing(8)
        
        top_row = QHBoxLayout()
        title = QLabel("📝 Productive To-Do")
        title.setObjectName("title")
        title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        top_row.addWidget(title)
        
        top_row.addStretch()
        
        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.setIcon(qta.icon("fa5s.sun", color='white'))
        self.theme_btn.setIconSize(QSize(20, 20))
        self.theme_btn.setFixedSize(44, 44)
        self.theme_btn.setToolTip("Toggle Theme")
        self.theme_btn.clicked.connect(self.toggle_theme)
        top_row.addWidget(self.theme_btn)
        
        header.addLayout(top_row)
        
        self.quote_label = QLabel(get_quote_of_day())
        self.quote_label.setObjectName("quote")
        self.quote_label.setFont(QFont("Segoe UI", 14))
        header.addWidget(self.quote_label)
        
        main.addLayout(header)

        # Input row
        input_row = QHBoxLayout()
        input_row.setSpacing(12)
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("What needs to be done?")
        self.task_input.setMinimumHeight(48)
        self.task_input.returnPressed.connect(self.add_task)
        input_row.addWidget(self.task_input)

        add_btn = QPushButton("Add Task")
        add_btn.setObjectName("addBtn")
        add_btn.setMinimumHeight(48)
        add_btn.setMinimumWidth(120)
        add_btn.clicked.connect(self.add_task)
        input_row.addWidget(add_btn)

        main.addLayout(input_row)

        # Filters + Search
        control_row = QHBoxLayout()
        control_row.setSpacing(8)
        
        self.btn_all = QPushButton("All")
        self.btn_all.setProperty("filterSelected", True)
        self.btn_all.setMinimumWidth(80)
        self.btn_all.clicked.connect(lambda: self.change_filter("all"))
        control_row.addWidget(self.btn_all)

        self.btn_pending = QPushButton("Pending")
        self.btn_pending.setProperty("filterSelected", False)
        self.btn_pending.setMinimumWidth(80)
        self.btn_pending.clicked.connect(lambda: self.change_filter("pending"))
        control_row.addWidget(self.btn_pending)

        self.btn_completed = QPushButton("Completed")
        self.btn_completed.setProperty("filterSelected", False)
        self.btn_completed.setMinimumWidth(80)
        self.btn_completed.clicked.connect(lambda: self.change_filter("completed"))
        control_row.addWidget(self.btn_completed)

        control_row.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search tasks...")
        self.search_input.setMinimumHeight(42)
        self.search_input.textChanged.connect(self.on_search)
        self.search_input.setFixedWidth(250)
        control_row.addWidget(self.search_input)

        main.addLayout(control_row)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_content = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(12)
        self.scroll_area.setWidget(self.scroll_content)
        main.addWidget(self.scroll_area)

        # Footer
        footer = QHBoxLayout()
        footer.setSpacing(12)
        
        clear_btn = QPushButton("Clear Completed")
        clear_btn.setObjectName("actionBtn")
        clear_btn.clicked.connect(self.clear_completed)
        footer.addWidget(clear_btn)

        cleanup_btn = QPushButton("Auto-clean (30+ days)")
        cleanup_btn.setObjectName("actionBtn")
        cleanup_btn.clicked.connect(lambda: self.auto_cleanup(days=30))
        footer.addWidget(cleanup_btn)

        footer.addStretch()
        main.addLayout(footer)

        self.task_input.setFocus()

    def load_tasks(self, animated=False):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            widget = child.widget()
            if widget:
                widget.deleteLater()

        todos = load_todos()
        filtered = todos[:]
        
        if self.filter_mode == "pending":
            filtered = [t for t in filtered if not t["completed"]]
        elif self.filter_mode == "completed":
            filtered = [t for t in filtered if t["completed"]]
            
        if self.search_text:
            filtered = [t for t in filtered if self.search_text.lower() in t["task"].lower()]
        
        filtered.sort(key=lambda t: t["id"], reverse=True)
        
        if not filtered:
            empty = QLabel("No tasks yet. Add one above!")
            color = "#64748b" if self.dark_mode else "#475569"
            empty.setStyleSheet(f"color: {color}; font-style: italic; padding: 40px; font-size: 16px;")
            empty.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(empty)
            return

        for t in filtered:
            w = self._create_task_widget(t["id"], t["task"], t["completed"])
            self.scroll_layout.addWidget(w)
            if animated:
                self._animate_fade_in(w)

        self.scroll_layout.addStretch()

    def add_task(self):
        task = self.task_input.text().strip()
        if not task:
            return
            
        todos = load_todos()
        next_id = max([t["id"] for t in todos], default=0) + 1
        new_task = {
            "id": next_id,
            "task": task,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        todos.append(new_task)
        save_todos(todos)
        self.task_input.clear()
        self.load_tasks(animated=True)
        self.task_input.setFocus()

    def delete_task(self, task_id):
        reply = QMessageBox.question(
            self, 
            "Delete Task", 
            "Are you sure you want to delete this task?", 
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
            
        todos = load_todos()
        todos = [t for t in todos if t["id"] != task_id]
        save_todos(todos)
        self.load_tasks(animated=True)

    def update_completed(self, task_id, checked):
        todos = load_todos()
        for t in todos:
            if t["id"] == task_id:
                t["completed"] = checked
                break
        save_todos(todos)
        self.load_tasks(animated=True)  # Reload to update visuals if needed

    def clear_completed(self):
        reply = QMessageBox.question(
            self,
            "Clear Completed",
            "Delete all completed tasks?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
            
        todos = load_todos()
        old_count = len(todos)
        todos = [t for t in todos if not t["completed"]]
        save_todos(todos)
        if len(todos) < old_count:
            self.load_tasks(animated=True)

    def auto_cleanup(self, days=30):
        todos = load_todos()
        old_count = len(todos)
        now = datetime.now()
        cutoff = now - timedelta(days=days)
        todos = [t for t in todos if not (t["completed"] and datetime.fromisoformat(t["created_at"]) < cutoff)]
        save_todos(todos)
        affected = old_count - len(todos)
        QMessageBox.information(
            self, 
            "Auto-cleanup", 
            f"Removed {affected} completed task(s) older than {days} days."
        )
        if affected > 0:
            self.load_tasks(animated=True)

    def _create_task_widget(self, task_id, text, completed):
        task_frame = QFrame()
        task_frame.setObjectName("taskFrame")
        layout = QHBoxLayout(task_frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        checkbox = TaskCheckBox(text, self.dark_mode)
        checkbox.setChecked(completed)
        checkbox.checked_changed.connect(
            lambda checked: self.update_completed(task_id, checked)
        )
        layout.addWidget(checkbox, stretch=1)

        # Edit button with proper icon color
        edit_btn = QPushButton()
        edit_btn.setObjectName("editBtn")
        icon_color = '#3b82f6' if self.dark_mode else '#2563eb'
        edit_btn.setIcon(qta.icon("fa5s.edit", color=icon_color))
        edit_btn.setFixedSize(40, 40)
        edit_btn.setIconSize(QSize(16, 16))
        edit_btn.setToolTip("Edit task")
        edit_btn.clicked.connect(lambda: self._edit_task_popup(task_id, text))
        layout.addWidget(edit_btn)

        # Delete button with proper icon color
        delete_btn = QPushButton()
        delete_btn.setObjectName("deleteBtn")
        icon_color = '#ef4444' if self.dark_mode else '#dc2626'
        delete_btn.setIcon(qta.icon("fa5s.trash-alt", color=icon_color))
        delete_btn.setFixedSize(40, 40)
        delete_btn.setIconSize(QSize(16, 16))
        delete_btn.setToolTip("Delete task")
        delete_btn.clicked.connect(lambda: self.delete_task(task_id))
        layout.addWidget(delete_btn)

        effect = QGraphicsOpacityEffect(task_frame)
        effect.setOpacity(1.0)
        task_frame.setGraphicsEffect(effect)
        
        return task_frame

    def _edit_task_popup(self, task_id, old_text):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Task")
        dialog.setModal(True)
        dialog.setFixedSize(500, 160)
        
        dlg_layout = QVBoxLayout(dialog)
        dlg_layout.setContentsMargins(24, 24, 24, 24)
        dlg_layout.setSpacing(16)
        
        edit_input = QLineEdit()
        edit_input.setText(old_text)
        edit_input.setMinimumHeight(48)
        dlg_layout.addWidget(edit_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self._save_edit(task_id, edit_input.text(), dialog))
        buttons.rejected.connect(dialog.reject)
        dlg_layout.addWidget(buttons)
        
        edit_input.selectAll()
        edit_input.setFocus()
        dialog.exec()

    def _save_edit(self, task_id, new_text, dialog):
        new_text = new_text.strip()
        if not new_text:
            QMessageBox.warning(self, "Empty Task", "Task cannot be empty.")
            return
            
        todos = load_todos()
        for t in todos:
            if t["id"] == task_id:
                t["task"] = new_text
                break
        save_todos(todos)
        dialog.accept()
        self.load_tasks(animated=True)

    def _animate_fade_in(self, widget, duration=300):
        effect = widget.graphicsEffect()
        if not effect or not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
            
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setDuration(duration)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        
        if not hasattr(widget, '_animations'):
            widget._animations = []
        widget._animations.append(anim)
        
        anim.finished.connect(
            lambda: widget._animations.remove(anim) 
            if hasattr(widget, '_animations') and anim in widget._animations 
            else None
        )

    def change_filter(self, mode):
        self.filter_mode = mode
        self.btn_all.setProperty("filterSelected", mode == "all")
        self.btn_pending.setProperty("filterSelected", mode == "pending")
        self.btn_completed.setProperty("filterSelected", mode == "completed")
        
        for btn in (self.btn_all, self.btn_pending, self.btn_completed):
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            
        self.load_tasks(animated=True)

    def on_search(self, text):
        self.search_text = text.strip()
        self.load_tasks(animated=True)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            self.setStyleSheet(self.dark_stylesheet)
            self.theme_btn.setIcon(qta.icon("fa5s.sun", color='white'))
        else:
            self.setStyleSheet(self.light_stylesheet)
            self.theme_btn.setIcon(qta.icon("fa5s.moon", color='white'))
        
        # Reload tasks to update icon colors and checkbox styles
        self.load_tasks()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = TodoApp()
    window.show()
    sys.exit(app.exec())