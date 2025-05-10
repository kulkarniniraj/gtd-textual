from typing import Coroutine
from datetime import datetime, timedelta

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid, Horizontal, Vertical
from textual.events import Key
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.widgets import (Button, Checkbox, Footer, Header, Input, Label,
                             ListItem, ListView, Static, TextArea)

import dl
import logger.utils as logger_utils
from components.side import Sidebar, SidebarItem
from components.task import TaskDialog, TaskList, TaskItem, TaskScreen

State = {
    'focus': 'task-list',
    'index': 0
}

def restore_focus(app: App):
    print(f"Restoring focus: {State['focus']} {State['index']}")
    logger_utils.info(f"Restoring focus: {State['focus']} {State['index']}")
    if State['focus'] == 'task-list':        
        app.query_one('TaskList').index = State['index']
        app.query_one('TaskList').focus()
    elif State['focus'] == 'sidebar':
        app.query_one('Sidebar').index = State['index']
        app.query_one('Sidebar').focus()

def adjust_dates():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    tasks = dl.get_all_tasks()
    for task in tasks:
        if task.scheduled_at is not None:
            if task.scheduled_at < today:
                task.tag = 'next'
                task.scheduled_at = today
                dl.save_task(task)
            elif task.scheduled_at == today:
                task.tag = 'next'
                dl.save_task(task)

class MainWin(Horizontal):

    def on_mount(self):
        print("Mounting MainWin")
        logger_utils.info("Mounting MainWin")
        
    def compose(self) -> ComposeResult:
        sidebar = Vertical(
            Sidebar(
                SidebarItem("Inbox", "inbox"),
                SidebarItem("Next", "next"),
                SidebarItem("Scheduled", "scheduled"),
                SidebarItem("Maybe", "maybe"),
                SidebarItem("Waiting", "waiting"),
                SidebarItem("", "", disabled=True),
                SidebarItem("Projects", "projects", disabled=True, classes="disabled"),
                SidebarItem("Project 1", "project1"),
                SidebarItem("Project 2", "project2"),
                SidebarItem("Project 3", "project3"),
                SidebarItem("", "", disabled=True),
                SidebarItem("Finished Tasks", "finished"),
            ),
            id="sidebar"
        )
        sidebar.border_title = "Sidebar"
        yield sidebar

        main_view = TaskScreen(
            id="main-content"
        )
        main_view.border_title = "Inbox"
        yield main_view
# --- Main App ---
class GTDApp(App):
    title = "GTD App"
    CSS_PATH = "main.tcss"
    BINDINGS = [("q", "quit", "Quit"),
                ("escape", "quit", "Quit"),
                ("left", "focus_left", "Focus Sidebar"),
                ("right", "focus_right", "Focus Main")
                ]
    

    def on_mount(self):
        self.theme = "tokyo-night"
        # self.query_one('#main-content').focus()
        
    def compose(self) -> ComposeResult:
        yield MainWin()
        yield Footer()

    def action_request_quit(self):
        self.action_quit()
    
    def action_focus_left(self):
        logger_utils.info("Focusing Sidebar")
        self.query_one('Sidebar').focus()

    def action_focus_right(self):
        logger_utils.info("Focusing Main")
        self.query_one('TaskList').focus()

if __name__ == "__main__":
    adjust_dates()
    app = GTDApp()
    app.run()
