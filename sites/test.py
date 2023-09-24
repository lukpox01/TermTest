import curses

from utils import Site, Menu


class Test(Site):
    def __init__(self):
        super().__init__()

    def show_bar(self, test):
        num_questions = len(test.questions)
        bar = ""
        done_symbol = "\u2B24"
        notdone_symbol = "\u25CB"
        for i in range(num_questions):
            if i == num_questions - 1:
                bar += done_symbol
            else:
                bar += notdone_symbol + "\u2576"  # -
        self.stdscr.addstr(2, self.X // 2 - num_questions - 1, bar)


class TEST(Test):
    def __init__(self, test):
        super().__init__()
        self.test = test
        self.selected = {}
        self.border()

    def show_test(self):
        self.show_bar(self.test)
        self.stdscr.addstr(
            7, self.X // 2 - len(self.test.title) // 2, self.test.title, curses.A_BOLD
        )
        if len(self.test.description) // 60 > 1:
            for i in range(len(self.test.description) // 60):
                self.stdscr.addstr(
                    10 + i,
                    self.X // 2 - 60 // 2,
                    self.test.description[60 * i : 60 * (i + 1)],
                )
        else:
            self.stdscr.addstr(
                10, self.X // 2 - len(self.test.description) // 2, self.test.description
            )

        menu = Menu([("START", 1)], self.stdscr, "BACK")
        menu_o = menu.display()

        if menu_o[1] == 1:  # START
            q = 1
            question = Question(self.test, q)  # TODO manage questions
            s = question.show_question()
            self.selected[
                self.test.questions[q - 1]
            ] = s  # stored selected options in form of testmodel question, option
        self.stdscr.getch()

    def manage_questions(self):
        pass


class Question(Test):
    def __init__(self, test, question, selected=None):
        super().__init__()
        self.test = test
        self.question = test.questions[question - 1]
        self.selected = selected
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def show_question(self):
        self.show_bar(self.test)
        self.stdscr.addstr(4, 10, self.question.question)
        self.stdscr.hline(5, 10, "-", 60)
        while True:
            for i, o in enumerate(self.question.options):
                if self.selected == i:
                    self.stdscr.addstr(
                        7 + i, 10, chr(97 + i) + ". " + o, curses.color_pair(1)
                    )
                else:
                    self.stdscr.addstr(
                        7 + i, 10, chr(97 + i) + ". " + o, curses.A_NORMAL
                    )
            option_ch = self.stdscr.getch()
            if option_ch == 10 and self.selected is not None:
                self.question.done = True
                return self.selected
            elif len(self.question.options) - option_ch - 96 <= 0:
                self.selected = option_ch - 97
            else:
                continue
