import curses
import os
import re

logo = [
    "▄▄▄█████▓  ▓█████  ██▀███    ███▄ ▄███▓ ▄▄▄█████▓  ▓█████   ██████  ▄▄▄█████▓",
    "▓  ██▒ ▓▒  ▓█   ▀ ▓██ ▒ ██▒ ▓██▒▀█▀ ██▒ ▓  ██▒ ▓▒  ▓█   ▀▒ ██    ▒  ▓  ██▒ ▓▒",
    "▒ ▓██░ ▒░  ▒███   ▓██ ░▄█ ▒ ▓██    ▓██░ ▒ ▓██░ ▒░  ▒███  ░  ▓██▄    ▒ ▓██░ ▒░",
    "░ ▓██▓ ░   ▒▓█  ▄ ▒██▀▀█▄   ▒██    ▒██  ░ ▓██▓ ░   ▒▓█  ▄   ▒   ██▒ ░ ▓██▓ ░ ",
    "  ▒██▒ ░  ▒░▒████ ░██▓ ▒██▒ ▒██▒   ░██▒   ▒██▒ ░  ▒░▒████▒ ██████▒▒   ▒██▒ ░ ",
    "  ▒ ░░    ░░░ ▒░  ░ ▒▓ ░▒▓░ ░ ▒░   ░  ░   ▒ ░░    ░░░ ▒░ ▒  ▒▓▒ ▒ ░   ▒ ░░   ",
    "    ░     ░ ░ ░     ░▒ ░ ▒  ░  ░      ░     ░     ░ ░ ░  ░  ░▒  ░ ░     ░    ",
    "  ░ ░         ░     ░░   ░  ░      ░      ░ ░         ░  ░   ░  ░     ░      ",
    "          ░   ░      ░             ░              ░   ░         ░            ",
]


class Menu:
    def __init__(self, menu_options, stdscr, last_option):
        self.menu_options = menu_options
        self.stdscr = stdscr
        self.selected = 0
        self._previously_selected = None
        self.last_option = last_option

        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)  # Hide cursor
        self.stdscr.keypad(1)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.hilite_color = curses.color_pair(1)
        self.normal_color = curses.A_NORMAL

    def prompt_select(self):
        option_count = len(self.menu_options)
        longest_option = len(max(self.menu_options, key=len))
        input_key = None

        ENTER_KEY = ord("\n")
        while input_key != ENTER_KEY:
            max_y, max_x = self.stdscr.getmaxyx()
            if self.selected != self._previously_selected:
                self._previously_selected = self.selected

            for option in range(option_count):
                if self.selected == option:
                    self._draw_option(option, self.hilite_color, max_x, longest_option)
                else:
                    self._draw_option(option, self.normal_color, max_x, longest_option)

            if self.selected == option_count:
                self.stdscr.addstr(
                    20 + option_count,
                    max_x // 2 - (longest_option + 5) // 2,
                    "{:2} - {}".format(option_count + 1, self.last_option),
                    self.hilite_color,
                )
            else:
                self.stdscr.addstr(
                    20 + option_count,
                    max_x // 2 - (longest_option + 5) // 2,
                    "{:2} - {}".format(option_count + 1, self.last_option),
                    self.normal_color,
                )

            self.stdscr.refresh()

            input_key = self.stdscr.getch()
            down_keys = [curses.KEY_DOWN, ord("j")]
            up_keys = [curses.KEY_UP, ord("k")]
            exit_keys = [ord("q")]

            if input_key in down_keys:
                if self.selected < option_count:
                    self.selected += 1
                else:
                    self.selected = 0

            if input_key in up_keys:
                if self.selected > 0:
                    self.selected -= 1
                else:
                    self.selected = option_count

            if input_key in exit_keys:
                self.selected = option_count  # auto select exit and return
                break

        return self.selected

    def _draw_option(self, option_number, style, max_x, longest_option):
        self.stdscr.addstr(
            20 + option_number,
            max_x // 2 - (longest_option + 5) // 2,
            "{:2} - {}".format(option_number + 1, self.menu_options[option_number][0]),
            style,
        )

    def display(self):
        selected_option = self.prompt_select()
        if selected_option < len(self.menu_options):
            selected_opt = self.menu_options[selected_option]
            return selected_opt
        else:
            return self.last_option, 0


class Site:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.box()
        self.Y, self.X = self.stdscr.getmaxyx()

    def end_app(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def show_logo(self):
        for i, line in enumerate(logo):
            self.stdscr.addstr(i + 2, self.X // 2 - len(line) // 2, line)


def to_str(s: str) -> str:
    return str(s)[2:-1]


def isvalidEmail(email: str) -> bool:
    pattern = "^\S+@\S+\.\S+$"
    objs = re.search(pattern, email)
    try:
        if objs.string == email:
            return True
    except:
        return False
