from typing import Coroutine
import time

from components.side import Sidebar, SidebarItem
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid, Horizontal, Vertical
from textual.events import Key
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.widgets import (Button, Checkbox, Footer, Header, Input, Label,
                             ListItem, ListView, Static, TextArea, Select)

import dl
import logger.utils as logger_utils

class TaskDialog(ModalScreen[bool]):
    BINDINGS = [("d", "datepick", "Date Picker"),
                ("escape", "dismiss", "Cancel"),
                ("ctrl+s", "save", "Save")]
    
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

    def action_save(self):
        self.save_task()

    def compose(self) -> ComposeResult:
        tag_list = [('Inbox', 'inbox'), ('Next', 'next'), ('Scheduled', 'scheduled'), ('Maybe', 'maybe'), ('Waiting', 'waiting')]
        project_list = [('Default', 'default'), ('Project 1', 'project1'), ('Project 2', 'project2'), ('Project 3', 'project3')]
        td = Grid(
            Label("Title:", classes="form-label"),
            Input(id="title-input", placeholder="Enter title...", value=self.title),
            
            # Label("Tags:", classes="form-label"),
            # Input(id="tags-input", placeholder="Enter tags (comma separated)...", value=self.tags),
            Label("Tag:", classes="form-label"),
            Select(tag_list, id="tag-input", value=self.item.tag),
            Label("Project:", classes="form-label"),
            Select(project_list, id="project-input", value=self.item.project),
                
            
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
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:        
        logger_utils.info(f"Button pressed: {event.button.label} {event.button.id} {event.button.id == 'save-button'}")
        if event.button.id == "save-button":
            self.save_task()            
        else:
            self.dismiss(False)

    def save_task(self):
        title = self.query_one("#title-input").value            
        tag = self.query_one("#tag-input").value
        project = self.query_one("#project-input").value
        description = self.query_one("#desc-input").text
        self.item.title = title
        self.item.tag = tag
        self.item.project = project
        self.item.description = description
        logger_utils.info(f"Saving task: {self.item}")
        dl.save_task(self.item)
        self.dismiss(True)

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
        logger_utils.info(f"Mounting TaskList {time.time()}")
        # restore_focus(self.app)

class TaskScreen(Vertical):
    BINDINGS = [("n", "task_details_popup", "New Task"),
                ("space", "mark_complete", "Mark Complete")]

    tag = reactive('inbox', recompose=True)
    task_list = reactive([], recompose=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_task_list()
        
    def update_task_list(self):
        self.task_list = dl.get_all_tasks()

    def on_mount(self):
        logger_utils.info(f"TaskScreen mounted: {self.tag} {time.time()}")

    def filter_tasks(self):
        todo_tasks = self.task_list
        if self.tag == 'finished':
            tasks = [x for x in todo_tasks if x.done == 1]
        else:
            tasks = [x for x in todo_tasks if x.done != 1]
            if self.tag == 'inbox':
                tasks = [x for x in todo_tasks if x.tag == 'inbox']
            elif self.tag == 'next':
                tasks = [x for x in todo_tasks if x.tag == 'next']
            elif self.tag == 'scheduled':
                tasks = [x for x in todo_tasks if x.tag == 'scheduled']
            elif self.tag == 'maybe':
                tasks = [x for x in todo_tasks if x.tag == 'maybe']
            elif self.tag == 'waiting':
                tasks = [x for x in todo_tasks if x.tag == 'waiting']
            else:
                tasks = todo_tasks
        logger_utils.info(f"Filtering tasks: {tasks}")
        return tasks

    def compose(self) -> ComposeResult:
        logger_utils.info(f"Composing TaskScreen {time.time()}")
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
            logger_utils.info(f"Active task: {active_task.todo_task.title}")
            if active_task.todo_task.done == 0 or active_task.todo_task.done == None:
                active_task.todo_task.done = 1
            else:
                active_task.todo_task.done = 0
            dl.save_task(active_task.todo_task)  
            self.update_task_list()
            self.refresh(recompose=True)
        # self.query_one('#task-list').focus()

    def task_details_popup(self, task_item: dl.Task = None):
        if task_item is None:
            task_item = dl.create_empty_task()
        self.app.push_screen(TaskDialog(task_item = task_item), 
                             lambda x: (self.update_task_list() or self.refresh(recompose=True)) if x is True else None )