import os

import interact
import loader

__author__ = 'Michael'


class Main(object):
    def __init__(self):
        self.loaded_files = []
        self.chapters = []

    def load_file(self, filename):
        if filename in self.loaded_files:
            return
        self.loaded_files.append(filename)
        parser = loader.Parser()
        self.chapters.extend(parser.load_file(filename))

    def load_dir(self, dir, match):
        for filename in sorted(os.listdir(dir)):
            if not match(filename):
                continue
            self.load_file(os.path.join(dir, filename))

    def chapter_scenes(self, console):
        l_chapters = "Use \"chapter X\" command to view a chapter.\n\n"
        for chap in self.chapters:
            l_chapters += repr(chap) + "\n"
            console.scenes.append(chap.gen_scene())
        console.add_scene("Contents", l_chapters)

        @console.command(
            "start",
            "View contents in this tutorial.",
            True
        )
        def cmd_start(_self):
            _self.set_scene("Contents")

        @console.command(
            "chapter",
            "Open a chapter of the tutorial.",
            True,
            int
        )
        def cmd_chapter(_self, n):
            try:
                _self.set_scene("Chapter {}".format(n))
            except interact.InteractiveConsole.NoSuchSceneError:
                _self.warn("There is no chapter {}.".format(n))

    def start_interactive(self):
        console = interact.InteractiveConsole()
        self.chapter_scenes(console)
        console.start()


if __name__ == "__main__":
    from sys import argv

    if len(argv) > 1 and argv[1] == "-d":
        import options

        options.DEBUG = True
    main = Main()
    main.load_dir("data", lambda n: n.startswith("python_") and n.endswith(".txt"))
    main.start_interactive()
