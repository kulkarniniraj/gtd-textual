from typing import Coroutine

from textual_datepicker import DatePicker, DateSelect

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
                SidebarItem("Projects", "projects"),
                SidebarItem("Project 1", "project1"),
                SidebarItem("Project 2", "project2"),
                SidebarItem("Project 3", "project3"),
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
                ("escape", "quit", "Quit")]
    

    def on_mount(self):
        self.theme = "tokyo-night"
        # self.query_one('#main-content').focus()
        
    def compose(self) -> ComposeResult:
        yield MainWin()
        yield Footer()

    def action_request_quit(self):
        self.action_quit()
    


if __name__ == "__main__":
    app = GTDApp()
    app.run()
