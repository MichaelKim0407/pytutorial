from item import Item

__author__ = 'Michael'


class TextPause(object):
    def __str__(self):
        return "----- Pause -----\n"


class SectionText(object):
    def __init__(self, text="", items=None):
        if items is None:
            self.items = [text]
        else:
            self.items = items

    def __iadd__(self, other):
        if isinstance(other, str) or isinstance(other, unicode):
            self.items[-1] += other
        elif isinstance(other, Item) or isinstance(other, TextPause):
            self.items.append(other)
            self.items.append("")
        else:
            raise TypeError(other)
        return self

    def strip(self):
        def is_empty(item):
            if not isinstance(item, str):
                return False
            elif item.strip():
                return False
            return True

        items = list(self.items)
        while items and is_empty(items[0]):
            items.pop(0)
        while items and is_empty(items[-1]):
            items.pop()
        return str(SectionText(items=items)).strip("\n")

    def __str__(self):
        result = ""
        for item in self.items:
            result += str(item)
        return result

    def __repr__(self):
        return repr(self.__str__())

    def split(self):
        def __split():
            items = []
            for item in self.items:
                if isinstance(item, TextPause):
                    yield SectionText(items=items)
                    items = []
                else:
                    items.append(item)
            yield SectionText(items=items)

        return list(__split())


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
