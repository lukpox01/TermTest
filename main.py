# from curses import wrapper
import sys

import dill

from sites import TEST, LOGIN, SIGNUP
from utils import Menu, Site, find_all


class MainPage(Site):
    def main(self):
        self.show_logo()

        menu = Menu([("DEV", 3), ("LOGIN", 1), ("SIGNUP", 2)], self.stdscr, "EXIT")
        auth = menu.display()

        if auth[1] == 1:  # LOGIN
            login = LOGIN()
            info = login.get_info()

        elif auth[1] == 2:  # SIGNUP
            signup = SIGNUP()
            info = signup.get_info()

        elif auth[1] == 3:  # dev
            info

        else:
            sys.exit()

        while True:
            self.stdscr.clear()
            self.border()
            self.show_logo()
            menu = Menu([("LOAD TEST", 1)], self.stdscr, "EXIT")
            menu_o = menu.display()

            if menu_o[1] == 1:  # LOAD TEST
                files = find_all("*.ttf", "tests")
                self.stdscr.clear()
                self.border()
                self.show_logo()
                explorer = Menu(
                    [(file, i + 1) for i, file in enumerate(files)], self.stdscr, "BACK"
                )
                file = explorer.display()
                with open(file[0], "rb") as f:
                    test = TEST(dill.load(f))
                    test.show_test()
            else:
                break
        self.end_app()


m = MainPage()
m.main()
