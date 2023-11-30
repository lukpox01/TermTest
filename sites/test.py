import curses
from curses.textpad import rectangle

from utils import Site, Menu, count_percents




# TODO math cleanup


class Test(Site):
    def __init__(self):
        super().__init__()
        self.selected = {}
        self.percents = None

    def show_bar(self, test):
        num_questions = len(test.questions)
        bar = ""
        done_symbol = "\u2B24"
        notdone_symbol = "\u25CB"
        for i in range(num_questions):
            symbol = notdone_symbol if not test.questions[i].done else done_symbol
            if i == num_questions - 1:
                bar += symbol
            else:
                bar += symbol + "\u2576"  # -
        self.stdscr.addstr(2, self.X // 2 - num_questions - 1, bar)


class Reluslt(Test):
    def __init__(self, test, percents):
        super().__init__()
        self.border()
        self.test = test
        self.percents = percents

    def show_results(self):
        self.show_bar(self.test)
        self.stdscr.addstr(self.Y//2, int(self.X // 2 - len(str(self.percents))), f"{self.percents}%")


class TEST(Test):
    def __init__(self, test):
        super().__init__()
        self.test = test


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
            done = self.manage_questions()
            if not done:
                return
            elif done:
                # sort
                keys = list(self.selected.keys())
                keys.sort()
                sorted_answers = [self.selected[key] for key in keys]
                correct_answers = [
                    self.test.questions[int(key)].correct for key in keys
                ]
                self.percents = count_percents(correct_answers, sorted_answers)
                result = Reluslt(self.test, self.percents)
                result.show_results()
                self.stdscr.getch()

    def manage_questions(self):
        q_index = 0
        while True:
            question = Question(self.test, q_index)
            s = question.show_question()
            question.end_app()
            if s[0]:
                self.selected[q_index] = s[
                    1
                ]  # stored selected options in form of question idx, option
                if q_index == len(self.test.questions) - 1:
                    return True

                q_index += 1
                continue
            else:
                if s[1] == 0:  # BACK
                    return False
                q_index += s[1]
                continue


class Question(Test):
    def __init__(self, test, question, selected=None):
        super().__init__()
        self.test = test
        self.q_num = question
        self.question = test.questions[question]
        self.selected = selected
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def show_question(self):
        self.show_bar(self.test)
        self.stdscr.addstr(4, 10, self.question.question)
        self.stdscr.hline(5, 10, "-", 60)
        questions_idx = len(self.test.questions) - 1
        if self.q_num != 0:
            self.stdscr.addstr(self.Y - 5, self.X - 26, "Previous")
            self.stdscr.addstr(self.Y - 4, self.X - 26, "\u2B60 / J")
        if self.q_num == 0:
            self.stdscr.addstr(self.Y - 5, self.X - 26, "BACK")
            self.stdscr.addstr(self.Y - 4, self.X - 26, "\u2B60 / J")
        if self.q_num != questions_idx:
            self.stdscr.addstr(self.Y - 5, self.X - 13, "Next")
            self.stdscr.addstr(self.Y - 4, self.X - 13, "\u2B62 / K")
        if self.q_num == questions_idx:
            self.stdscr.addstr(self.Y - 5, self.X - 13, "SAVE")
            self.stdscr.addstr(self.Y - 4, self.X - 13, "ENTER")
        rectangle(self.stdscr, self.Y - 6, self.X - 14, self.Y - 3, self.X - 3)
        rectangle(self.stdscr, self.Y - 6, self.X - 27, self.Y - 3, self.X - 16)
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
                return True, self.selected + 1

            elif option_ch == 107 or option_ch == 261:  # next
                if self.q_num == questions_idx:
                    continue
                return False, 1
            elif option_ch == 106 or option_ch == 260:  # previous
                if self.q_num == 0:
                    return False, 0  # back
                return False, -1
            elif len(self.question.options) - option_ch - 96 <= 0:
                self.selected = option_ch - 97
            else:
                continue


# 107 K 106 J 261 ra 260 la
