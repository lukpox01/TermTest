from utils import Test, Question
import sys


def txt_check(val, max_length, min_length, type_, line_num):
    if val == "":
        sys.exit(f"Empty {type_} on line {line_num}")
    elif len(val) > max_length:
        sys.exit(f"Too long {type_} on line {line_num} (<{max_length})")
    elif len(val) < min_length:
        sys.exit(f"Too short {type_} on line {line_num} (>{min_length})")


def textfile(lines):
    t = {"autor": None, "title": None, "questions": [], "time_to_complete": None}
    q = {"question": None, "options": [], "correct": None}
    options_count = 0
    for index, line in enumerate(lines):
        if line.startswith("@autor"):

            autor = line.split(':', 1)[1].strip()
            txt_check(autor, 32, 3, "autor", index + 1)
            t["autor"] = autor

        elif line.startswith("@title"):

            title = line.split(':', 1)[1].strip()
            txt_check(title, 64, 3, "title", index + 1)
            t["title"] = title

        elif line.startswith("@time"):

            time = line.split(' ', 1)[1].strip()
            try:
                if int(time) < 5:
                    sys.exit(f"Time is too short on line {index + 1} (>5)")
                elif int(time) > 1440:
                    sys.exit(f"Time is too long on line {index + 1} (<1440)")
            except:
                sys.exit(f"Invalid time on line {index + 1}")

            t["time_to_complete"] = time
        elif line.startswith("#"):

            if options_count != 0 and options_count != 1:
                print(2)
                t["questions"].append(Question(**q))
            elif options_count > 5:
                sys.exit(f"Too many options in {q['question']}")
            elif options_count != 0 and options_count <= 1:
                sys.exit(f"Not enough options in {q['question']}")

            question = line.split('#')[1].strip()
            txt_check(question, 256, 3, "question", index + 1)

            options_count = 0
            q["question"] = line.split('#')[1].strip()

        elif line.startswith(">"):

            option = line.split('>', 1)[1].replace('+', '').strip()
            txt_check(option, 128, 1, "option", index + 1)

            options_count += 1
            if line.strip().endswith('+'):
                q["correct"] = options_count
            q["options"].append(option)

    if options_count != 0 and options_count != 1:
        print(2)
        t["questions"].append(Question(**q))
    elif options_count > 5:
        sys.exit(f"Too many options in {q['question']}")
    elif options_count != 0 and options_count <= 1:
        sys.exit(f"Not enough options in {q['question']}")
    test = Test(**t)
    print(test)


def main(argv):
    # file = argv[-1]
    file = "test.txt"
    if file.split('.')[-1] == 'ttf':
        pass
    elif file.split('.')[-1] == 'txt':
        print(1)
        with open(file) as f:
            textfile(f.readlines())


if __name__ == '__main__':
    main(sys.argv)

