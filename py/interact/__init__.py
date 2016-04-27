import scene
from command import CommandInfo
from error import InvalidCommand

__author__ = 'Michael'


class InteractiveConsole(object):
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
                except InvalidCommand as e:
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
    def _command(name, args_def):
        def decor(func):
            def new_func(self, *args):
                args = args_def.parse(name, *args)
                return func(self, *args)

            return new_func

        return decor

    @classmethod
    def command_global(cls, name, *args):
        cmd_info = CommandInfo(*args)
        _decor = InteractiveConsole._command(name, cmd_info.args_def)

        def decor(func):
            new_func = _decor(func)
            cls.Commands[name] = (new_func, cmd_info)
            return new_func

        return decor

    def command(self, name, *args):
        cmd_info = CommandInfo(*args)
        _decor = InteractiveConsole._command(name, cmd_info.args_def)

        def decor(func):
            new_func = _decor(func)
            self.commands[name] = (new_func, cmd_info)
            return new_func

        return decor


import commands_basic
import scenes
import commands_scenes
