import data

__author__ = 'Michael'


class Parser(object):
    def __init__(self, resources):
        self.encoding = "UTF-8"
        self.chapters = []
        self.cur_chap = None
        self.cur_sect = None
        self.resources = resources

    @staticmethod
    def parse_tag(lines):
        args = []
        content = ""
        _tag, _rem = lines[0].split("(", 1)
        tag = _tag.strip().lstrip("@")
        _args, _rem = _rem.split(")", 1)
        for _arg in _args.split(","):
            args.append(_arg.strip())
        _rem = _rem.strip()
        if not _rem:
            content = ""
        elif _rem != ":":
            content = _rem
        else:
            while lines and len(lines) > 1:
                lines.pop(0)
                if lines[0] == "{":
                    continue
                elif lines[0] == "}":
                    break
                else:
                    content += lines[0] + "\n"
            else:
                raise data.TagSyntaxError(tag)
        return data.Tag(tag, args, content)

    def run_tag(self, tag):
        if tag.tag in ["encode", "encoding"]:
            self.encoding = tag.args[0] or tag.content
        elif tag.tag == "chapter":
            self.cur_chap = data.Chapter(self.encoding, tag.args[0], tag.content)
            self.chapters.append(self.cur_chap)
            self.cur_sect = self.cur_chap.base_section
        elif tag.tag == "section":
            self.cur_sect = data.Section(tag.args[0], tag.content)
            self.cur_chap.base_section.sections.append(self.cur_sect)
        elif tag.tag in ["eg", "example", "usage", "syntax"]:
            if tag.tag == "example":
                tag.tag = "eg"
            item = data.Item(tag.tag, tag.args[0], tag.content)
            self.cur_chap.items.append(item)
            self.cur_sect.text += item
        elif tag.tag in ["script"]:
            try:
                # First, check if the item has already been created from requested resource
                item = self.cur_chap.find_item(tag.tag, tag.args[0])
            except ValueError:
                # Create a new item
                def __script_name(tag):
                    return "m{}_{}.py".format(self.cur_chap.chap_id, tag.args[0])

                resource_name = {
                    "script": __script_name
                }
                item = data.Item(
                    tag.tag,
                    tag.args[0],
                    self.resources[tag.tag][
                        resource_name[tag.tag](tag)
                    ].content
                )
                self.cur_chap.items.append(item)
            self.cur_sect.text += item
        elif tag.tag == "pause":
            self.cur_sect.text += data.TextPause()

    def load_file(self, file):
        lines = file.split("\n")
        self.cur_chap = None
        while lines:
            if lines[0].startswith("@"):
                tag = Parser.parse_tag(lines)
                self.run_tag(tag)
                if not lines:
                    break
            else:
                self.cur_sect.text += lines[0] + "\n"
            lines.pop(0)
        for chap in self.chapters:
            chap.base_section.sort()
        return self.chapters
