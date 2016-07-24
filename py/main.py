import interact
import loader
import resource

__author__ = 'Michael'


class Main(object):
    def __init__(self):
        self.resources = None
        self.chapters = []

    def load_resources(self, resource_root_dir):
        res_loader = resource.ResourceLoader(resource_root_dir)
        self.resources = res_loader.load_all()

    def find_chapter(self, chap_id):
        for chap in self.chapters:
            if chap.chap_id == chap_id:
                return chap
        raise ValueError(chap_id)

    def load_file(self, filename):
        parser = loader.Parser(self.resources)
        file = self.resources["tutorial"][filename].content
        self.chapters.extend(parser.load_file(file))

    def load_dir(self, dir, match):
        for filename in self.resources.list_resources("tutorial"):
            if not match(filename):
                continue
            self.load_file(filename)

    def chapter_scenes(self, console):
        l_chapters = "Use \"chapter X\" command to view a chapter.\n\n"
        for chap in self.chapters:
            l_chapters += repr(chap) + "\n"
            console.scenes.append(chap.gen_scene())
        console.add_scene("Contents", l_chapters)

        @console.command(
            "start",
            (),
            "View contents in this tutorial.",
            is_simple=True
        )
        def cmd_start(_self):
            _self.set_scene("Contents")

        @console.command(
            "chapter",
            ((int,),),
            "Open a chapter of the tutorial.",
            is_simple=True
        )
        def cmd_chapter(_self, n):
            try:
                _self.set_scene("Chapter {}".format(n))
            except interact.InteractiveConsole.NoSuchSceneError:
                _self.warn("There is no chapter {}.".format(n))

        @console.command(
            "eg",
            ((str,), (str,)),
            "View an example in the tutorial.",
            """The first argument is the chapter id and the second one is the example id."""
        )
        def cmd_eg(_self, chap_id, eg_id):
            try:
                print str(self.find_chapter(chap_id).find_item("eg", eg_id))
            except ValueError:
                print "No found!"

        @console.command(
            "usage",
            ((str,), (str,)),
            "View an usage in the tutorial.",
            """The first argument is the chapter id and the second one is the usage id."""
        )
        def cmd_usage(_self, chap_id, usage_id):
            try:
                print str(self.find_chapter(chap_id).find_item("usage", usage_id))
            except ValueError:
                print "Not found!"

        @console.command(
            "syntax",
            ((str,), (str,)),
            "View a syntax definition in the tutorial."
            """The first argument is the chapter id and the second one is the syntax id."""
        )
        def cmd_syntax(_self, chap_id, syntax_id):
            try:
                print str(self.find_chapter(chap_id).find_item("syntax", syntax_id))
            except ValueError:
                print "Not found!"

        @console.command(
            "script",
            ((str,), (str,)),
            "View a script",
            """The first argument is the chapter id and the second one is the script id."""
        )
        def cmd_script(_self, chap_id, script_id):
            try:
                print str(self.find_chapter(chap_id).find_item("script", script_id))
            except ValueError:
                print "Not found!"

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
    main.load_resources("resource")
    main.load_dir("data", lambda n: n.startswith("python_") and n.endswith(".txt"))
    main.start_interactive()
