import curses
import sys
from curses.textpad import rectangle
from utils import Site, to_str, isvalidEmail
from utils.database import Database

class LOGIN(Site):
    def __init__(self):
        super().__init__()
        self.name = None
        self.password = None
        self.email = None
        curses.curs_set(1)
        curses.echo()
        self.database = Database()

    def get_info(self, msg=""):
        while True:
            self.stdscr.clear()

            self.stdscr.addstr(0, curses.COLS - len(msg) - 1, msg)  # TODO make it in center
            self.stdscr.addstr(1, 1, "Name     : ")
            self.stdscr.addstr(4, 1, "Email    : ")
            self.stdscr.addstr(7, 1, "Password : ")

            rectangle(self.stdscr, 0, 11, 2, 27)
            rectangle(self.stdscr, 3, 11, 5, 42)
            rectangle(self.stdscr, 6, 11, 8, 27)

            name: str = to_str(self.stdscr.getstr(1, 12, 15))
            rectangle(self.stdscr, 0, 11, 2, 27)

            email: str = to_str(self.stdscr.getstr(4, 12, 30)).replace("\\x16", "@")
            rectangle(self.stdscr, 3, 11, 5, 42)

            password: str = to_str(self.stdscr.getstr(7, 12, 15))
            rectangle(self.stdscr, 6, 11, 8, 27)

            self.stdscr.addstr(15, 5, "if you want to continue then press | Any")
            self.stdscr.addstr(16, 5, "if you want to correct then press  | r")
            self.stdscr.addstr(17, 5, "if you want to quit then press     | q")
            self.stdscr.addstr(19, 5, "if you forget your password contact me :)")
            key: str = self.stdscr.getkey()

            if key == "r":
                continue
            elif key == "q":
                self.end_app()
                sys.exit()
            else:
                if not isvalidEmail(email):
                    msg = "Invalid email"
                    continue
                user_exists = self.database.find_user(name, password)
                if not user_exists:
                    msg = "No user exists"
                    continue

            self.stdscr.refresh()
            return name, email, password


class SIGNUP(Site):
    def __init__(self):
        super().__init__()
        self.name = None
        self.password = None
        self.email = None
        curses.curs_set(1)
        curses.echo()
        self.database = Database()

    def get_info(self, msg=""):
        while True:
            self.stdscr.clear()

            self.stdscr.addstr(0, curses.COLS - len(msg) - 1, msg)  # TODO make it in center
            self.stdscr.addstr(1, 1, "Name     : ")
            self.stdscr.addstr(4, 1, "Email    : ")
            self.stdscr.addstr(7, 1, "Password : ")
            self.stdscr.addstr(10, 1, "re-Password : ")

            rectangle(self.stdscr, 0, 11, 2, 27)
            rectangle(self.stdscr, 3, 11, 5, 42)
            rectangle(self.stdscr, 6, 11, 8, 27)
            rectangle(self.stdscr, 9, 14, 11, 30)

            name: str = to_str(self.stdscr.getstr(1, 12, 15))
            rectangle(self.stdscr, 0, 11, 2, 27)

            email: str = to_str(self.stdscr.getstr(4, 12, 30)).replace("\\x16", "@")
            rectangle(self.stdscr, 3, 11, 5, 42)

            password: str = to_str(self.stdscr.getstr(7, 12, 15))
            rectangle(self.stdscr, 6, 11, 8, 27)

            password2: str = to_str(self.stdscr.getstr(10, 15, 15))
            rectangle(self.stdscr, 9, 14, 11, 30)

            self.stdscr.addstr(15, 5, "if you want to continue then press | Any")
            self.stdscr.addstr(16, 5, "if you want to correct then press  | r")
            self.stdscr.addstr(17, 5, "if you want to quit then press     | q")

            key: str = self.stdscr.getkey()

            if key == "r":
                continue
            elif key == "q":
                self.end_app()
                sys.exit()
            else:
                if not isvalidEmail(email):
                    msg = "Invalid email syntax"
                    continue
                if password != password2:
                    msg = "Password mismatch"
                    continue
                if not self.database.is_empty():
                    if self.database.name_exists(name):
                        msg = "Name already used"
                        continue
                    usr = self.database.find_user(name, password)
                    if not usr:
                        self.database.add_user(name, email, password)
                    else:
                        msg = "User already exist"
                        continue
                else:
                    self.database.add_user(name, email, password)
            self.stdscr.refresh()

            return name, email, password
