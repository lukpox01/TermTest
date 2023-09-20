# from curses import wrapper
import curses
from utils import Menu, Site
from sites import LOGIN, SIGNUP
import sys


class MainPage(Site):
    def __init__(self):
        super().__init__()

    def main(self):
        curses.curs_set(0)

        self.show_logo()
        self.stdscr.refresh()

        menu = Menu([("LOGIN", 1), ("SIGNUP", 2)], self.stdscr, "EXIT")
        auth = menu.display()
        self.end_app()

        if auth[1] == 1:  # LOGIN
            login = LOGIN()
            info = login.get_info()
        elif auth[1] == 2:  # SIGNUP
            signup = SIGNUP()
            info = signup.get_info()
        else:
            sys.exit()

        print(info)


m = MainPage()
m.main()
