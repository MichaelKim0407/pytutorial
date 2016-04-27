__author__ = 'Michael'


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
