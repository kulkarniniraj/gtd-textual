from typing import Coroutine

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid, Horizontal, Vertical
from textual.events import Key
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.widgets import (Button, Checkbox, Footer, Header, Input, Label,
                             ListItem, ListView, Static, TextArea)

import logger.utils as logger_utils

class Sidebar(ListView):

    def on_list_view_highlighted(self, event: ListView.Highlighted):
        print(f"Sidebar Highlighted: {event.item} {self.index}")
        logger_utils.info(f"Sidebar Highlighted: {event.item} idx: {self.highlighted_child}")
        # State['focus'] = 'sidebar'
        # State['index'] = self.index
        # logger_utils.info(f"Sidebar saved index: {State['index']}")
        
        task_screen = self.app.query_one('#main-content')
        task_screen.tag = event.item.tag        

    def on_focus(self, event):
        print(f"Sidebar Focused: {event} {self.index}")
        logger_utils.info(f"Sidebar Focused: {event} idx: {self.index}")
        
    def on_blur(self, event):
        print(f"Sidebar Blurred: {event} {self.index}")
        logger_utils.info(f"Sidebar Blurred: {event} idx: {self.index}")

class SidebarItem(ListItem):
    def __init__(self, label: str, tag: str):
        super().__init__()
        self.label = label
        self.tag = tag

    def __str__(self):
        return f"{self.label} : ({self.tag})"

    def compose(self) -> ComposeResult:
        yield Label(self.label)
