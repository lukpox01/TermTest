import curses
import sys
from curses.textpad import rectangle

from utils import Site, to_str, isvalidEmail
from utils.database import Database

# TODO: do a little cleanup with math
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
            self.border()
            self.show_logo("login")

            self.stdscr.addstr(self.Y // 2 + 3 - 1 + 3, self.X // 2 - 43 // 2 + 11, msg)
            self.stdscr.addstr(self.Y // 2 - 3, self.X // 2 - 43 // 2, "Name     : ")
            self.stdscr.addstr(self.Y // 2, self.X // 2 - 43 // 2, "Password : ")
            # X//2 center of screen,
            # 43 is lenght of longest field email,
            # 43//2 is half that i substract to get curs
            rectangle(
                self.stdscr,
                self.Y // 2 - 3 - 1,
                self.X // 2 - 43 // 2 + 11,
                self.Y // 2 - 3 + 1,
                self.X // 2 - 43 // 2 + 12 + 15,
            )
            rectangle(
                self.stdscr,
                self.Y // 2 - 1,
                self.X // 2 - 43 // 2 + 11,
                self.Y // 2 + 1,
                self.X // 2 - 43 // 2 + 12 + 15,
            )

            name: str = to_str(
                self.stdscr.getstr(self.Y // 2 - 3, self.X // 2 - 43 // 2 + 12, 15)
            ).replace("\\x16", "@")
            rectangle(
                self.stdscr,
                self.Y // 2 - 3 - 1,
                self.X // 2 - 43 // 2 + 11,
                self.Y // 2 - 3 + 1,
                self.X // 2 - 43 // 2 + 12 + 15,
            )

            password: str = to_str(
                self.stdscr.getstr(self.Y // 2, self.X // 2 - 43 // 2 + 12, 15)
            )
            rectangle(
                self.stdscr,
                self.Y // 2 - 1,
                self.X // 2 - 43 // 2 + 11,
                self.Y // 2 + 1,
                self.X // 2 - 43 // 2 + 12 + 15,
            )

            self.buttons()
            key: int = self.stdscr.getch()

            if key == 32:  # spacebar
                continue
            elif key == 10:  # enter
                user_exists = self.database.find_user(
                    name, password
                )  # TODO add more corrections
                if not user_exists:
                    msg = "No user exists"
                    continue
            else:
                print(key)
                self.end_app()
                sys.exit()

            self.stdscr.refresh()
            return name, password

    def buttons(self):
        x = self.X // 2 - 43 // 2 + 11
        y = self.Y // 2 + 3 + 4
        self.stdscr.addstr(y + 1, x - 10, "Confirm")
        self.stdscr.addstr(y + 2, x - 10, "Enter  \u21B0")
        self.stdscr.addstr(y + 1, x + 4, "Edit")
        self.stdscr.addstr(y + 2, x + 4, "Space  \u2514\u2500\u2518")
        self.stdscr.addstr(y + 1, x + 18, "Quit")
        self.stdscr.addstr(y + 2, x + 18, "Any  *")
        rectangle(self.stdscr, y, x - 11, y + 3, x + 2)
        rectangle(self.stdscr, y, x + 3, y + 3, x + 16)
        rectangle(self.stdscr, y, x + 17, y + 3, x + 30)


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
            self.border()
            self.show_logo("signup")

            self.stdscr.addstr(self.Y // 2 + 3 - 1 + 3, self.X // 2 - 43 // 2 + 11, msg)
            self.stdscr.addstr(self.Y // 2 - 3, self.X // 2 - 43 // 2, "Name     : ")
            self.stdscr.addstr(self.Y // 2, self.X // 2 - 43 // 2, "Email    : ")
            self.stdscr.addstr(self.Y // 2 + 3, self.X // 2 - 43 // 2, "Password : ")
            # X//2 center of screen,
            # 43 is lenght of longest field email,
            # 43//2 is half that i substract to get curs
            rectangle(
                self.stdscr,
                self.Y // 2 - 3 - 1,
                self.X // 2 - 43 // 2 + 11,
                self.Y // 2 - 3 + 1,
                self.X // 2 - 43 // 2 + 12 + 15,
            )
            rectangle(
                self.stdscr,
                self.Y // 2 - 1,
                self.X // 2 - 43 // 2 + 11,
                self.Y // 2 + 1,
                self.X // 2 - 43 // 2 + 12 + 30,
            )
            rectangle(
                self.stdscr,
                self.Y // 2 + 3 - 1,
                self.X // 2 - 43 // 2 + 11,
                self.Y // 2 + 3 + 1,
                self.X // 2 - 43 // 2 + 12 + 15,
            )

            name: str = to_str(
                self.stdscr.getstr(self.Y // 2 - 3, self.X // 2 - 43 // 2 + 12, 15)
            )
            rectangle(
                self.stdscr,
                self.Y // 2 - 3 - 1,
                self.X // 2 - 43 // 2 + 11,
                self.Y // 2 - 3 + 1,
                self.X // 2 - 43 // 2 + 12 + 15,
            )

            email: str = to_str(
                self.stdscr.getstr(self.Y // 2, self.X // 2 - 43 // 2 + 12, 30)
            ).replace("\\x16", "@")
            rectangle(
                self.stdscr,
                self.Y // 2 - 1,
                self.X // 2 - 43 // 2 + 11,
                self.Y // 2 + 1,
                self.X // 2 - 43 // 2 + 12 + 30,
            )

            password: str = to_str(
                self.stdscr.getstr(self.Y // 2 + 3, self.X // 2 - 43 // 2 + 12, 15)
            )
            rectangle(
                self.stdscr,
                self.Y // 2 + 3 - 1,
                self.X // 2 - 43 // 2 + 11,
                self.Y // 2 + 3 + 1,
                self.X // 2 - 43 // 2 + 12 + 15,
            )

            self.buttons()
            key: int = self.stdscr.getch()

            if key == 32:  # spacebar
                continue
            elif key == 10:  # enter
                if not isvalidEmail(
                    email
                ):  # TODO add more corrections password maybe re-password
                    msg = "Invalid email"
                    continue

                if not self.database.is_empty():
                    if self.database.name_exists(name):
                        msg = "Name already used"
                        continue
                    usr = self.database.find_user(name, password)
                    if not usr:
                        self.database.add_user(name, password, email)
                    else:
                        msg = "User already exist"
                        continue
                else:
                    self.database.add_user(name, password, email)

            else:
                print(key)
                self.end_app()
                sys.exit()

            self.stdscr.refresh()
            return name, email, password

    def buttons(self):
        x = self.X // 2 - 43 // 2 + 11
        y = self.Y // 2 + 3 + 4
        self.stdscr.addstr(y + 1, x - 10, "Confirm")
        self.stdscr.addstr(y + 2, x - 10, "Enter  \u21B0")
        self.stdscr.addstr(y + 1, x + 4, "Edit")
        self.stdscr.addstr(y + 2, x + 4, "Space  \u2514\u2500\u2518")
        self.stdscr.addstr(y + 1, x + 18, "Quit")
        self.stdscr.addstr(y + 2, x + 18, "Any  *")
        rectangle(self.stdscr, y, x - 11, y + 3, x + 2)
        rectangle(self.stdscr, y, x + 3, y + 3, x + 16)
        rectangle(self.stdscr, y, x + 17, y + 3, x + 30)
