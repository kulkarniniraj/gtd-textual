from typing import Coroutine
from textual.app import App, ComposeResult
from textual.events import Key
from textual.widgets import (
    Header,
    Footer,
    ListView,
    ListItem,
    Static,
    Label,
    Input,
    TextArea,
    Button,
    Checkbox,
)
from textual.containers import Vertical, Horizontal, Grid, Container
from textual.screen import Screen, ModalScreen
from textual.binding import Binding
from textual_datepicker import DateSelect, DatePicker

import logger.utils as logger_utils
import dl

todo_tasks = [
    ("Buy Groceries", [], "Purchase fruits, vegetables, and dairy products from the supermarket."),
    ("Morning Exercise", [], "Complete a 30-minute workout session, including stretching and cardio."),
    ("Read a Book", [], "Read at least 20 pages of 'The Great Gatsby' for leisure and learning."),
    ("Meeting with Team", [], "Attend the weekly project meeting to discuss progress and blockers."),
    ("Send Emails", [], "Respond to urgent emails and follow up on pending client queries."),
    ("Pay Bills", [], "Complete the payment for electricity, water, and internet services."),
    ("Clean Workspace", [], "Organize the desk, file important documents, and declutter."),
    ("Plan Weekend Trip", [], "Research and finalize the itinerary for the upcoming weekend getaway."),
    ("Backup Files", [], "Ensure all important documents and photos are backed up to the cloud."),
    ("Practice Coding", [], "Work on a Python project to improve problem-solving skills.")
]
# --- Task Data Structure (Basic) ---
class Task:
    def __init__(self, title, tags, description, completed=False):
        self.title = title
        self.tags = tags
        self.description = description
        self.completed = completed


class TaskDialog(ModalScreen):
    BINDINGS = [("d", "datepick", "Date Picker"),
                ("escape", "dismiss", "Cancel")]
    
    def __init__(self, context = 'inbox', task_item = ('', [], ''), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context
        self.title = task_item[0]
        self.tags = task_item[1]
        self.description = task_item[2]
        
    def action_datepick(self):
        DateSelect(
            picker_mount=self,            
        )

    def compose(self) -> ComposeResult:
        td = Grid(
            Label("Title:", classes="form-label"),
            Input(id="title-input", placeholder="Enter title..."),
            
            Label("Tags:", classes="form-label"),
            Input(id="tags-input", placeholder="Enter tags (comma separated)..."),
            
            Label("Description:", classes="form-label"),
            TextArea(id="desc-input", classes="multiline"),
            
            Container(
                Button("Save", variant="primary", id="save-button"),
                Button("Cancel", id="cancel-button"),
                id="button-container"),
            
            id="task-dialog"
        )
        td.border_title = "Task Details"
        yield td
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(True)
        # if event.button.label == "Save":
        #     title = self.query_one(Input).value
        #     tags = self.query_one(Input, nth=2).value
        #     description = self.query_one(TextArea).value

        #     # Access the TaskListScreen to add task. You'll need to pass the parent screen or app
        #     # in a more robust way in a full application.
        #     # For this example, let's assume the previous screen is available as 'self.app.screen_stack[-1]'
        #     if isinstance(self.app.screen_stack[-1], TaskListScreen):
        #         self.app.screen_stack[-1].tasks.append(Task(title, tags, description))
        #         self.app.screen_stack[-1].refresh()
        #     self.app.pop_screen()
        # else:
        #     self.app.pop_screen()

class TaskItem(ListItem):
    def __init__(self, todo_task: tuple):
        self.todo_task = todo_task
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Checkbox(value=False),
            Label(self.todo_task[0]),
            Label('default', classes="task-item-tags"),
            classes="task-item"            
        )

class MainWin(Horizontal):
    BINDINGS = [("n", "task_details_popup", "Task Details")]
    def on_mount(self):
        self.query_one('#task-list').focus()
        # self.fo

    def compose(self) -> ComposeResult:
        sidebar = Vertical(
            ListView(
                ListItem(Label("Inbox")),
                ListItem(Label("Next")),
                ListItem(Label("Scheduled")),
                ListItem(Label("Maybe")),
                ListItem(Label("Waiting")),
                ListItem(Label("")),
                ListItem(Static("Projects"), id="projects-header"),
                ListItem(Label("   Project 1")),
                ListItem(Label("   Project 2")),
                ListItem(Label("")),
                ListItem(Label("Finished Tasks")),
            ),
            id="sidebar"
        )
        sidebar.border_title = "Sidebar"
        yield sidebar

        main_view = Vertical(
            ListView(
                *[
                    TaskItem(task)
                    for task in todo_tasks
                ],
                id="task-list"
            ),
            id="main-content"
        )
        main_view.border_title = "Inbox"
        yield main_view

    def on_list_view_selected(self, event: ListView.Selected):
        # print(f"Task selected: {event.item}")
        logger_utils.info(f"Task selected: {event.item}")
        # self.push_screen(TaskDialog(task = event.item.todo_task))
        # self.app.push_screen(TaskDialog(task_item = event.item.todo_task))
        self.task_details_popup(event.item.todo_task)

    def action_task_details_popup(self):
        self.task_details_popup()

    def task_details_popup(self, task_item: dl.Task = None):
        if task_item is None:
            task_item = dl.create_empty_task()
        self.app.push_screen(TaskDialog(task_item = task_item))

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
    # def action_request_quit(self) -> None:
    #     """Action to display the quit dialog."""
    #     self.push_screen(QuitScreen())


    # def on_list_view_selected(self, event: ListView.Selected):
    #     # Handle sidebar selection
    #     label = event.item.query_one(Label)
    #     if label.text == "Inbox":
    #         self.tasks = [
    #             Task("Check Emails", "work", "Process unread emails"),
    #             Task("Buy Groceries", "home", "Milk, eggs, bread"),
    #         ]
    #         self.push_screen(TaskListScreen("Inbox", self.tasks))
    #     elif label.text == "Next":
    #         self.tasks = [
    #             Task("Call John", "personal", "About the project"),
    #             Task("Write Report", "work", "Weekly progress"),
    #         ]
    #         self.push_screen(TaskListScreen("Next", self.tasks))

    #     # Add more conditions for other sidebar options

    # def on_mount(self) -> None:
    #     self.set_focus(self.query_one(ListView))


if __name__ == "__main__":
    app = GTDApp()
    app.run()
