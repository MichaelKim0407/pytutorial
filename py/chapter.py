import scene

__author__ = 'Michael'


class Tag(object):
    def __init__(self, tag, args, content):
        self.tag = tag
        self.args = args
        self.content = content

    def __repr__(self):
        return "tag: {!r}, args: {!r}, content: {!r}".format(self.tag, self.args, self.content)


class TagSyntaxError(Exception):
    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return "No ending bracket found for tag {}".format(self.tag)


class ParseError(Exception):
    pass


class Item(object):
    Start = "* "
    Bracket = "------"

    def __init__(self, type, id, text):
        self.type = type
        self.id = id
        self.text = text
        if not text.endswith("\n"):
            self.text += "\n"

    def __repr__(self):
        return self.type + " " + self.id

    def __str__(self):
        return Item.Start + self.__repr__() + "\n" \
               + Item.Bracket + "\n" + self.text + Item.Bracket + "\n"


class SectionText(object):
    def __init__(self, text=""):
        self.items = [text]

    def __iadd__(self, other):
        if isinstance(other, str) or isinstance(other, unicode):
            self.items[-1] += other
        elif isinstance(other, Item):
            self.items.append(other)
            self.items.append("")
        else:
            raise TypeError(other)
        return self

    def __str__(self):
        result = ""
        for item in self.items:
            result += str(item)
        return result

    def __repr__(self):
        return repr(self.__str__())

    def __nonzero__(self):
        for item in self.items:
            if not isinstance(item, str):
                return True
            elif item.strip():
                return True
        return False


class Section(object):
    def __init__(self, id, title, text=""):
        self.id = id
        self.title = title
        self.text = SectionText(text)
        self.sections = []

    def __eq__(self, other):
        if isinstance(other, Section):
            return self.id == other.id
        else:
            return self.id == other

    def __hash__(self):
        return self.id.__hash__()

    def __repr__(self):
        return self.id + " " + self.title

    def __str__(self):
        result = self.__repr__() + "\n" + str(self.text)
        for section in self.sections:
            result += str(section)
        return result

    def __format__(self, spec):
        if spec == "":
            return self.__str__()
        elif spec == "list":
            result = self.__repr__() + "\n" + str(self.text)
            for sect in self.sections:
                result += "\n" + repr(sect)
            return result
        elif spec == "tree":
            result = self.__repr__()
            for sect in self.sections:
                result += "\n{:tree}".format(sect).replace("\n", "\n  ")
            return result
        else:
            return self.__repr__()

    def sort(self):
        cur_id = 1
        while cur_id < len(self.sections):
            sect = self.sections[cur_id]
            last = self.sections[cur_id - 1]
            if sect.id.startswith(last.id + "."):
                last.sections.append(sect)
                self.sections.pop(cur_id)
            else:
                cur_id += 1
        for sect in self.sections:
            sect.sort()

    def __iter__(self):
        yield self, []
        for sect in self.sections:
            for leaf, hierarchy in sect:
                yield leaf, [sect] + hierarchy


class Chapter(object):
    def __init__(self, encoding, chap_id, chap_title):
        self.encoding = encoding
        self.chap_id = chap_id
        self.base_section = Section("", chap_title)
        self.items = []

    def __repr__(self):
        return "Chapter {} {}".format(self.chap_id, self.base_section.title)

    def __str__(self):
        return "Chapter {}{}".format(self.chap_id, self.base_section)

    def __format__(self, spec):
        if spec == "":
            return self.__str__()
        elif spec == "tree":
            return "Chapter {}{:tree}".format(self.chap_id, self.base_section)

    def gen_scene(self):
        scene_name = "Chapter {}".format(self.chap_id)
        pages = ["Contents in this chapter\n\n{:tree}\n".format(self)]
        for sect, hier in self.base_section:
            if not sect.text:
                continue
            page = ""
            for p in hier:
                page += repr(p) + "\n"
            page += "\n"
            page += str(sect.text)
            pages.append(page)
        return scene.Scene(scene_name, *pages)
