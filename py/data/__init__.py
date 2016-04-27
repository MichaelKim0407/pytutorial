import scene

from tag import *
from item import *
from section import *

__author__ = 'Michael'


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
