__author__ = 'Michael'


class TypeSyntaxError(Exception):
    pass


class InvalidCommand(Exception):
    def __init__(self, msg):
        self.msg = msg
