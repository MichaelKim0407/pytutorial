import code

from interact import InteractiveConsole
from scenes import HELP_TEXT, HELP_FULL_TEXT

__author__ = 'Michael'


@InteractiveConsole.command_global(
    "main",
    "Go to the main menu.",
    True
)
def cmd_main(self, *args):
    self.set_scene("Main Menu")


@InteractiveConsole.command_global(
    "help",
    "Open help menu. By default (--simple), only frequently used commands are listed. To view all commands, use -A/--all option",
    True,
    (str, "--simple")
)
def cmd_help(self, option):
    if option in ["-A", "--all"]:
        _all = True
    elif option == "--simple":
        _all = False
    else:
        raise InteractiveConsole.InvalidCommand("Invalid options: {}".format(option))

    if _all:
        help_scene = self.find_scene("Help (Advanced)")
    else:
        help_scene = self.find_scene("Help")

    help_scene.pages = []
    count = 10

    def append(s):
        help_scene.pages[-1] += s

    for name in sorted(self.commands.keys()):
        if count == 10:
            help_scene.pages.append(HELP_FULL_TEXT if _all else HELP_TEXT)
            count = 0
        func, types, help_info, simple = self.commands[name]
        if not (_all or simple):
            continue
        append("\t{}\t\tTakes {} argument(s). ".format(name, len(types)))
        if types:
            for t in types:
                if isinstance(t, tuple):
                    append("{}({}) ".format(t[0].__name__, t[1]))
                else:
                    append("{} ".format(t.__name__))
        append("\n")
        append("\t\t\t{}\n".format(help_info))

        count += 1

    if _all:
        self.set_scene("Help (Advanced)")
    else:
        self.set_scene("Help")


@InteractiveConsole.command_global(
    "python",
    "Start interactive Python console.",
    True
)
def cmd_python(self, *args):
    def exit_console():
        raise SystemExit

    try:
        code.interact(local={"exit": exit_console})
    except SystemExit:
        self.refresh()
