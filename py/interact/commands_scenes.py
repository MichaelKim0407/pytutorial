from error import InvalidCommand
from interact import InteractiveConsole
from scenes import HELP_TEXT, HELP_FULL_TEXT

__author__ = 'Michael'


@InteractiveConsole.command_global(
    "main",
    "Go to the main menu.",
    True
)
def cmd_main(self):
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
        raise InvalidCommand("Invalid options: {}".format(option))

    help_scene = self.find_scene("Help")

    help_scene.pages = []
    count = 10

    def append(s):
        help_scene.pages[-1] += s

    for name in sorted(self.commands.keys()):
        if count == 10:
            help_scene.pages.append(HELP_FULL_TEXT if _all else HELP_TEXT)
            count = 0
        func, args_def, help_info, simple = self.commands[name]
        if not (_all or simple):
            continue
        append("\t{}\t\t{}\n".format(name, args_def))
        append("\t\t\t{}\n".format(help_info))

        count += 1

    self.set_scene("Help")
