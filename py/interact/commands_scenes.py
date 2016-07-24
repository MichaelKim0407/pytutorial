from mklibpy.util.list import format_list

from error import InvalidCommand
from interact import InteractiveConsole
from scenes import HELP_TEXT, HELP_FULL_TEXT, HELP_ALIASES

__author__ = 'Michael'


@InteractiveConsole.command_global(
    "main",
    (),
    "Go to the main menu.",
    is_simple=True
)
def cmd_main(self):
    self.set_scene("Main Menu")


@InteractiveConsole.command_global(
    "help",
    ((str, "--simple"),),
    "Open help menu.",
    """By default (--simple), only frequently used commands are listed.
To view all commands, use -A/--all option.
To view help for a specific command, use command name as the argument.
To view aliases, use --aliases.""",
    is_simple=True
)
def cmd_help(self, option):
    help_scene = self.find_scene("Help")

    def append(s):
        help_scene.pages[-1] += s

    if option in ["-A", "--all", "--simple"]:
        _all = option in ["-A", "--all"]

        help_scene.pages = []
        count = 10

        for name in sorted(self.commands.keys()):
            if count == 10:
                help_scene.pages.append(HELP_FULL_TEXT if _all else HELP_TEXT)
                count = 0
            func, cmd_info = self.commands[name]
            if not (_all or cmd_info.is_simple):
                continue
            append(cmd_info.help_short(name) + "\n")

            count += 1
    elif option in ["--aliases"]:
        help_scene.pages = []
        count = 10

        for alias in sorted(self.aliases.keys()):
            if count == 10:
                help_scene.pages.append(HELP_ALIASES)
                count = 0
            replace = self.aliases[alias]
            append("\t{}\t\t{}\n".format(
                alias,
                format_list(replace, "", "", " ", False)
            ))
    elif option in self.commands:
        func, cmd_info = self.commands[option]
        help_scene.pages = ["Usage information for command {}:\n\n{}".format(option, cmd_info.help_long(option))]
    else:
        raise InvalidCommand("No such command: {}".format(option))

    self.set_scene("Help")
