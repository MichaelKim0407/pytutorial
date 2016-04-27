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
            if not split:
                continue
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


import commands_basic
import scenes
import commands_scenes
