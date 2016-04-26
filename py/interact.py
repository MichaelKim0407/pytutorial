import scene

__author__ = 'Michael'


class InteractiveConsole(object):
    class TypeSyntaxError(Exception):
        pass

    class InvalidCommand(Exception):
        def __init__(self, msg):
            self.msg = msg

    class ExitCommand(Exception):
        pass

    class NoSuchSceneError(Exception):
        def __init__(self, name):
            self.name = name

    def __init__(self):
        self.scenes = list(self.__class__.Scenes)
        self.commands = dict(self.__class__.Commands)
        self.cur_scene = self.find_scene("Main Menu")
        self.history = [(self.cur_scene, self.cur_scene.cur_page)]
        self.history_pointer = 0

    def refresh(self):
        self.cur_scene.display()

    def warn(self, err_msg):
        self.cur_scene.display(err_msg)

    def update_history(self):
        self.history_pointer += 1
        if self.history_pointer < len(self.history):
            self.history = self.history[:self.history_pointer]
        self.history.append((self.cur_scene, self.cur_scene.cur_page))

    def use_history(self):
        item = self.history[self.history_pointer]
        self.cur_scene = item[0]
        self.cur_scene.cur_page = item[1]

    def change_history(self, n):
        if self.history_pointer + n < 0:
            self.history_pointer = 0
            self.use_history()
            self.warn("No more history")
        elif self.history_pointer + n >= len(self.history):
            self.history_pointer = len(self.history) - 1
            self.use_history()
            self.warn("Latest history")
        else:
            self.history_pointer += n
            self.use_history()
            self.refresh()

    def set_scene(self, name, page=0):
        self.cur_scene = self.find_scene(name)
        self.cur_scene.cur_page = page
        self.update_history()
        self.refresh()

    def start(self):
        self.refresh()
        while True:
            usr_input = raw_input(":")
            split = usr_input.split()
            cmd, args = split[0], split[1:]
            if cmd not in self.commands:
                self.warn("No such command: \"{}\".".format(cmd))
            else:
                try:
                    self.commands[cmd][0](self, *args)
                except InteractiveConsole.InvalidCommand as e:
                    self.warn("Invalid command: \"{}\". {}".format(usr_input, e.msg))
                except InteractiveConsole.ExitCommand:
                    break

    Scenes = []

    @classmethod
    def add_scene_global(cls, name, *pages):
        cls.Scenes.append(scene.Scene(name, *pages))

    def add_scene(self, name, *pages):
        self.scenes.append(scene.Scene(name, *pages))

    def find_scene(self, name):
        for scene in self.scenes:
            if scene.name == name:
                return scene
        raise InteractiveConsole.NoSuchSceneError(name)

    Commands = dict()

    @staticmethod
    def _command(name, *types):
        # First check types is valid
        _def = False
        required = 0
        for t in types:
            if isinstance(t, tuple):
                _def = True
            elif _def:
                raise InteractiveConsole.TypeSyntaxError
            else:
                required += 1

        def decor(func):
            def new_func(self, *args):
                # Check number of arguments
                if len(args) < required:
                    raise InteractiveConsole.InvalidCommand(
                        "Command \"{}\" requires {} argument(s).".format(name, required))
                elif len(args) > len(types):
                    raise InteractiveConsole.InvalidCommand(
                        "Command \"{}\" takes at most {} argument(s).".format(name, len(types)))

                # Convert arguments to type
                args = list(args)
                for i in range(len(args)):
                    if i < required:
                        t = types[i]
                    else:
                        t = types[i][0]
                    if t == str:
                        continue
                    try:
                        args[i] = t(args[i])
                    except ValueError:
                        raise InteractiveConsole.InvalidCommand(
                            "Parameter {} must be of type {}.".format(i + 1, t.__name__))

                # Fill default values
                for i in range(len(args), len(types)):
                    args.append(types[i][1])

                # Call function
                return func(self, *args)

            return new_func

        return decor

    @classmethod
    def command_global(cls, name, help_info, simple, *types):
        _decor = InteractiveConsole._command(name, *types)

        def decor(func):
            new_func = _decor(func)
            cls.Commands[name] = (new_func, types, help_info, simple)
            return new_func

        return decor

    def command(self, name, help_info, simple, *types):
        _decor = InteractiveConsole._command(name, *types)

        def decor(func):
            new_func = _decor(func)
            self.commands[name] = (new_func, types, help_info, simple)
            return new_func

        return decor


@InteractiveConsole.command_global(
    "refresh",
    "Refreshes the current page.",
    False
)
def cmd_refresh(self):
    self.refresh()


@InteractiveConsole.command_global(
    "exit",
    "Exits the interactive tutorial.",
    True
)
def cmd_exit(self):
    raise InteractiveConsole.ExitCommand


@InteractiveConsole.command_global(
    "history",
    "Change to a page you recently viewed.",
    False,
    int
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
        raise InteractiveConsole.InvalidCommand("The first argument should be positive. Use \"forward\" instead.")
    self.change_history(-n)


@InteractiveConsole.command_global(
    "forward",
    "Change to a page you viewed after this page.",
    False,
    (int, 1)
)
def cmd_forward(self, n):
    if n <= 0:
        raise InteractiveConsole.InvalidCommand("The first argument should be positive. Use \"back\" instead.")
    self.change_history(n)


@InteractiveConsole.command_global(
    "page",
    "Turn to a different page in the current scene.",
    True,
    int
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
        raise InteractiveConsole.InvalidCommand("The first argument should be positive. Use \"next\" instead.")
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
        raise InteractiveConsole.InvalidCommand("The first argument should be positive. Use \"prev\" instead.")
    if self.cur_scene.page_change(n):
        self.update_history()


InteractiveConsole.add_scene_global(
    "Main Menu",
    """Welcome to Michael Kim's Interactive Python tutorial!

Enter start to start learning!
Enter help for usage tips.
"""
)


@InteractiveConsole.command_global(
    "main",
    "Go to the main menu.",
    True
)
def cmd_main(self):
    self.set_scene("Main Menu")


InteractiveConsole.add_scene_global(
    "Help",
    """A list of useful commands:
\tName\t\tNotes"""
)

InteractiveConsole.add_scene_global(
    "Help (Advanced)",
    """A list of available commands:
\tName\t\tNotes"""
)


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
            help_scene.pages.append("A list of available commands:\n\tName\t\tNotes\n")
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
