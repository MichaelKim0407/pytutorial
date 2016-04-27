__author__ = 'Michael'


class Item(object):
    Start = "\033[34;1m*\033[0m "
    Brace = "\033[34;1m------\033[0m"

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
               + Item.Brace + "\n" + self.text + Item.Brace + "\n"
