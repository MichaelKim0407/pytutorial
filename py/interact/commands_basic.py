import subprocess

from mklibpy.util.path import CD

from error import InvalidCommand
from interact import InteractiveConsole

__author__ = 'Michael'


@InteractiveConsole.command_global(
    "refresh",
    (),
    "Refresh the current page."
)
def cmd_refresh(self):
    self.refresh()


@InteractiveConsole.command_global(
    "exit",
    (),
    "Exit the interactive tutorial.",
    is_simple=True
)
def cmd_exit(self):
    raise InteractiveConsole.ExitCommand


InteractiveConsole.alias_global("q", "exit")


@InteractiveConsole.command_global(
    "history",
    ((int,),),
    "Change to a page you recently viewed.",
)
def cmd_history(self, n):
    self.change_history(n)


@InteractiveConsole.command_global(
    "back",
    ((int, 1),),
    "Change to a page you viewed before this page."
)
def cmd_back(self, n):
    if n <= 0:
        raise InvalidCommand("The first argument should be positive. Use \"forward\" instead.")
    self.change_history(-n)


InteractiveConsole.alias_global("<", "back")


@InteractiveConsole.command_global(
    "forward",
    ((int, 1),),
    "Change to a page you viewed after this page."
)
def cmd_forward(self, n):
    if n <= 0:
        raise InvalidCommand("The first argument should be positive. Use \"back\" instead.")
    self.change_history(n)


InteractiveConsole.alias_global(">", "forward")


@InteractiveConsole.command_global(
    "page",
    ((int,),),
    "Turn to a different page in the current scene.",
    is_simple=True
)
def cmd_page(self, n):
    if self.cur_scene.page(n - 1):
        self.update_history()


@InteractiveConsole.command_global(
    "prev",
    ((int, 1),),
    "Turn to a previous page in the current scene.",
    is_simple=True
)
def cmd_prev(self, n):
    if n <= 0:
        raise InvalidCommand("The first argument should be positive. Use \"next\" instead.")
    if self.cur_scene.page_change(-n):
        self.update_history()


InteractiveConsole.alias_global(",", "prev")


@InteractiveConsole.command_global(
    "next",
    ((int, 1),),
    "Turn to a later page in the current scene.",
    is_simple=True
)
def cmd_next(self, n):
    if n <= 0:
        raise InvalidCommand("The first argument should be positive. Use \"prev\" instead.")
    if self.cur_scene.page_change(n):
        self.update_history()


InteractiveConsole.alias_global(".", "next")


@InteractiveConsole.command_global(
    "python",
    (None,),
    "Start interactive Python console, or run a Python script.",
    is_simple=True
)
def cmd_python(self, *args):
    with CD("resource/script"):
        subprocess.call(["python"] + list(args))
