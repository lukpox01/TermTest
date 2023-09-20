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
            self.border()
            self.show_logo("login")

            self.stdscr.addstr(
                self.Y // 2 + 3 - 1 + 3, self.X // 2 - 43 // 2 + 11, msg
            )  # TODO make it in center
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
                if not isvalidEmail(email):
                    msg = "Invalid email"
                    continue
                user_exists = self.database.find_user(name, password)
                if not user_exists:
                    msg = "No user exists"
                    continue
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
        self.stdscr.addstr(y + 2, x + 4, "Shift  \u2B61")
        self.stdscr.addstr(y + 1, x + 18, "Quit")
        self.stdscr.addstr(y + 2, x + 18, "Any  \u2514\u2500\u2518")
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

            self.stdscr.addstr(
                0, curses.COLS - len(msg) - 1, msg
            )  # TODO make it in center
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
                        self.database.add_user(name, password, email)
                    else:
                        msg = "User already exist"
                        continue
                else:
                    self.database.add_user(name, password, email)
            self.stdscr.refresh()

            return name, email, password
