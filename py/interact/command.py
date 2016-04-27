from error import TypeSyntaxError, InvalidCommand

__author__ = 'Michael'


class CommandArgDef(object):
    def __init__(self, type, default_value=None):
        self.type = type
        self.default_value = default_value

    def type_name(self):
        return self.type.__name__

    def cast(self, i, arg):
        if self.type == str:
            return arg
        else:
            try:
                return self.type(arg)
            except ValueError:
                raise InvalidCommand("Argument {} must be of type {}.".format(i, self.type_name()))

    def __str__(self):
        result = self.type_name()
        if self.default_value is not None:
            result += "({!r})".format(self.default_value)
        return result


class CommandArgsDef(list):
    def __init__(self, *types):
        list.__init__(self)
        _def = False
        self.required = 0
        for t in types:
            t = CommandArgDef(*t)
            self.append(t)
            if t.default_value is not None:
                _def = True
            elif _def:
                raise TypeSyntaxError
            else:
                self.required += 1

    def parse(self, cmd_name, *args):
        if len(args) < self.required:
            raise InvalidCommand("Command {} requires {} argument(s).".format(cmd_name, self.required))
        elif len(args) > len(self):
            raise InvalidCommand("Command {} takes at most {} argument(s).".format(cmd_name, len(self)))

        parsed_args = []
        for i in range(len(args)):
            parsed_args.append(self[i].cast(i, args[i]))
        for i in range(len(args), len(self)):
            parsed_args.append(self[i].default_value)
        return parsed_args

    def __str__(self):
        result = "Takes {} argument(s).".format(len(self))
        for t in self:
            result += " " + str(t)
        return result