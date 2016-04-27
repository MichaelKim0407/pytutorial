import mklibpy

import options

__author__ = 'Michael'

clear_screen = mklibpy.terminal.clear_screen


class Scene(object):
    def __init__(self, name, *pages):
        self.name = name
        self.pages = list(pages)
        self.cur_page = 0

    def display(self, err_msg=""):
        clear_screen()
        if err_msg:
            print err_msg
        print "Page {}/{} in {}".format(self.cur_page + 1, len(self.pages), self.name)
        print ""
        print self.pages[self.cur_page]
        if options.DEBUG:
            print ""
            print repr(self.pages[self.cur_page])

    def page_change(self, n):
        changed = True
        if self.cur_page + n < 0:
            if self.cur_page == 0:
                changed = False
            self.cur_page = 0
            self.display("First page")
        elif self.cur_page + n >= len(self.pages):
            if self.cur_page == len(self.pages) - 1:
                changed = False
            self.cur_page = len(self.pages) - 1
            self.display("Last page")
        else:
            if n == 0:
                changed = False
            self.cur_page += n
            self.display()
        return changed

    def page(self, n):
        return self.page_change(n - self.cur_page)
