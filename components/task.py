from typing import Coroutine

from textual_datepicker import DatePicker, DateSelect

from components.side import Sidebar, SidebarItem
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

class TaskDialog(ModalScreen):
    BINDINGS = [("d", "datepick", "Date Picker"),
                ("escape", "dismiss", "Cancel")]
    
    def __init__(self, task_item: dl.Task, context = 'inbox', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = task_item
        self.title = task_item.title
        self.tags = f'#{task_item.tag},@{task_item.project}'
        self.description = task_item.description
        
    def action_datepick(self):
        DateSelect(
            picker_mount=self,            
        )

    def compose(self) -> ComposeResult:
        td = Grid(
            Label("Title:", classes="form-label"),
            Input(id="title-input", placeholder="Enter title...", value=self.title),
            
            Label("Tags:", classes="form-label"),
            Input(id="tags-input", placeholder="Enter tags (comma separated)...", value=self.tags),
            
            Label("Description:", classes="form-label"),
            TextArea(id="desc-input", classes="multiline", text=self.description),
            
            Container(
                Button("Save", variant="primary", id="save-button"),
                Button("Cancel", id="cancel-button"),
                id="button-container"),
            
            id="task-dialog"
        )
        td.border_title = "Task Details"
        yield td
        
    def on_button_pressed(self, event: Button.Pressed) -> None:        
        if event.button.label == "Save":
            title = self.query_one("#title-input").value
            tags = self.query_one("#tags-input").value
            parts = tags.split(',')
            tag, project = '', ''
            for part in parts:
                if part.startswith('#'):
                    tag = part[1:]
                elif part.startswith('@'):
                    project = part[1:]
            description = self.query_one("#desc-input").value

            self.item.title = title
            self.item.tag = tag
            self.item.project = project
            self.item.description = description
            dl.save_task(self.item)
            self.dismiss(True)
        else:
            self.dismiss(False)

class TaskItem(ListItem):
    
    def __init__(self, todo_task: dl.Task):
        super().__init__()
        self.todo_task = todo_task        

    def compose(self) -> ComposeResult:
        print(f"Composing TaskItem for {self.todo_task.title}")
        check_label = True if self.todo_task.done == 1 else False
        # check_label = True
        tag_label = f'#{self.todo_task.tag:20} @{self.todo_task.project}'
        yield Horizontal(
            Checkbox(value=check_label),
            Label(self.todo_task.title),            
            Label(tag_label, classes="task-item-tags"),
            classes="task-item"            
        )

class TaskList(ListView):

    def on_list_view_highlighted(self, event: ListView.Highlighted):
        logger_utils.info(f"TaskList Highlighted: {event.item} {self.index}")
        # State['focus'] = 'task-list'
        # State['index'] = self.index

    def on_mount(self):
        logger_utils.info("Mounting TaskList")
        # restore_focus(self.app)

class TaskScreen(Vertical):
    BINDINGS = [("n", "task_details_popup", "New Task"),
                ("space", "mark_complete", "Mark Complete")]

    tag = reactive('inbox', recompose=True)
    def on_mount(self):
        logger_utils.info(f"TaskScreen mounted: {self.tag}")

    def filter_tasks(self):
        todo_tasks = dl.get_all_tasks()
        if self.tag == 'inbox':
            tasks = [x for x in todo_tasks if x.done != 1]
        elif self.tag == 'finished':
            tasks = [x for x in todo_tasks if x.done == 1]
        else:
            tasks = todo_tasks
        logger_utils.info(f"Filtering tasks: {tasks}")
        return tasks

    def compose(self) -> ComposeResult:
        yield TaskList(
            *[
                TaskItem(task)
                for task in self.filter_tasks()
            ],
            id="task-list"
        )

    def on_list_view_selected(self, event: ListView.Selected):
        # print(f"Task selected: {event.item}")
        logger_utils.info(f"Task selected: {event.item}")
        # self.push_screen(TaskDialog(task = event.item.todo_task))
        # self.app.push_screen(TaskDialog(task_item = event.item.todo_task))
        self.task_details_popup(event.item.todo_task)

    def action_task_details_popup(self):
        self.task_details_popup()

    def action_mark_complete(self):
        active_task = self.query_one('#task-list').highlighted_child
        if active_task is not None:
            print(f"Active task: {active_task.todo_task.title}")
            active_task.todo_task.done = 1
            dl.save_task(active_task.todo_task)            
            self.todo_tasks = dl.get_all_tasks()
        # self.query_one('#task-list').focus()

    def task_details_popup(self, task_item: dl.Task = None):
        if task_item is None:
            task_item = dl.create_empty_task()
        self.app.push_screen(TaskDialog(task_item = task_item))