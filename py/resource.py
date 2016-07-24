import os

from mklibpy.util.path import CD
from mklibpy.util.list import format_dict_multiline, format_list

__author__ = 'Michael'


class Resource(object):
    def __init__(self, type, name, content):
        self.type = type
        self.name = name
        self.content = content


class ResourceDict(dict):
    def __init__(self):
        dict.__init__(self)

    def add(self, res):
        if res.type not in self:
            self[res.type] = dict()
        self[res.type][res.name] = res

    def list_types(self):
        return sorted(self.keys())

    def list_resources(self, type):
        return sorted(self[type].keys())

    def __repr__(self):
        out = {
            type: format_list(
                sorted(self[type].keys()),
                "\t\t",
                "",
                "",
                False
            )
            for type in self
        }
        return format_dict_multiline(out, 16)


class ResourceLoader(object):
    def __init__(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)

    def load(self, type, name):
        with CD(os.path.join(self.root_dir, type)):
            with open(name) as f:
                return Resource(type, name, f.read())

    def load_all(self):
        result = ResourceDict()
        with CD(self.root_dir):
            for type in os.listdir("."):
                with CD(type):
                    for name in os.listdir("."):
                        result.add(self.load(type, name))
        return result
