from error import InvalidCommand
from interact import InteractiveConsole

__author__ = 'Michael'


@InteractiveConsole.command_global(
    "refresh",
    "Refresh the current page.",
    False
)
def cmd_refresh(self):
    self.refresh()


@InteractiveConsole.command_global(
    "exit",
    "Exit the interactive tutorial.",
    True
)
def cmd_exit(self):
    raise InteractiveConsole.ExitCommand


@InteractiveConsole.command_global(
    "history",
    "Change to a page you recently viewed.",
    False,
    (int,)
)
def cmd_history(self, n):
    self.change_history(n)


@InteractiveConsole.command_global(
    "back",
    "Change to a page you viewed before this page.",
    False,
    (int, 1)
)
def cmd_back(self, n):
    if n <= 0:
        raise InvalidCommand("The first argument should be positive. Use \"forward\" instead.")
    self.change_history(-n)


@InteractiveConsole.command_global(
    "forward",
    "Change to a page you viewed after this page.",
    False,
    (int, 1)
)
def cmd_forward(self, n):
    if n <= 0:
        raise InvalidCommand("The first argument should be positive. Use \"back\" instead.")
    self.change_history(n)


@InteractiveConsole.command_global(
    "page",
    "Turn to a different page in the current scene.",
    True,
    (int,)
)
def cmd_page(self, n):
    if self.cur_scene.page(n - 1):
        self.update_history()


@InteractiveConsole.command_global(
    "prev",
    "Turn to a previous page in the current scene.",
    True,
    (int, 1)
)
def cmd_prev(self, n):
    if n <= 0:
        raise InvalidCommand("The first argument should be positive. Use \"next\" instead.")
    if self.cur_scene.page_change(-n):
        self.update_history()


@InteractiveConsole.command_global(
    "next",
    "Turn to a later page in the current scene.",
    True,
    (int, 1)
)
def cmd_next(self, n):
    if n <= 0:
        raise InvalidCommand("The first argument should be positive. Use \"prev\" instead.")
    if self.cur_scene.page_change(n):
        self.update_history()
