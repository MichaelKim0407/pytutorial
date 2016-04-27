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
