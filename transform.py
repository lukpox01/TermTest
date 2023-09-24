import sys

import dill

from utils import Test, Question


def txt_check(val, max_length, min_length, type_, line_num):
    if val == "":
        sys.exit(f"Empty {type_} on line {line_num}")
    elif len(val) > max_length:
        sys.exit(f"Too long {type_} on line {line_num} (<{max_length})")
    elif len(val) < min_length:
        sys.exit(f"Too short {type_} on line {line_num} (>{min_length})")


# TODO implement description
def textfile(file):
    lines = file.readlines()
    t = {
        "autor": None,
        "title": None,
        "questions": [],
        "time_to_complete": None,
        "description": "",
    }
    q = {"question": None, "options": [], "correct": None, "done": False}
    options_count = 0
    for index, line in enumerate(lines):
        if line.startswith("@autor"):
            autor = line.split(":", 1)[1].strip()
            txt_check(autor, 32, 3, "autor", index + 1)
            t["autor"] = autor

        elif line.startswith("@title"):
            title = line.split(":", 1)[1].strip()
            txt_check(title, 64, 3, "title", index + 1)
            t["title"] = title

        elif line.startswith("@description"):
            description = line.split(":", 1)[1].strip()
            txt_check(description, 200, 0, "description", index + 1)
            t["description"] = description

        elif line.startswith("@time"):
            time = line.split(":", 1)[1].split(" ")[0].strip()
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
                t["questions"].append(Question(**q))
                q = {"question": None, "options": [], "correct": None, "done": False}
            elif options_count > 5:
                sys.exit(f"Too many options in {q['question']}")
            elif options_count != 0 and options_count <= 1:
                sys.exit(f"Not enough options in {q['question']}")

            question = line.split("#")[1].strip()
            txt_check(question, 256, 3, "question", index + 1)

            options_count = 0
            q["question"] = line.split("#")[1].strip()

        elif line.startswith(">"):
            option = line.split(">", 1)[1].replace("+", "").strip()
            txt_check(option, 128, 1, "option", index + 1)

            options_count += 1
            if line.strip().endswith("+"):
                q["correct"] = options_count
            q["options"].append(option)

    if options_count != 0 and options_count != 1:
        t["questions"].append(Question(**q))
    elif options_count > 5:
        sys.exit(f"Too many options in {q['question']}")
    elif options_count != 0 and options_count <= 1:
        sys.exit(f"Not enough options in {q['question']}")

    test = Test(**t)
    with open(
        f"{file.name[:-4]}.ttf", "wb"  # [:-4] strip out the .txt extension
    ) as ttf:
        dill.dump(test, ttf)


def ttf(file):
    test = dill.load(file)
    with open(
        file.name[:-4] + ".txt", "w"
    ) as txt:  # [:-4] strip out the .ttf extension
        txt.write("@autor:" + test.autor + "\n")
        txt.write("@title:" + test.title + "\n")
        txt.write("@time:" + test.time_to_complete + "\n\n")
        for question in test.questions:
            txt.write("# " + question.question + "\n")
            for i, option in enumerate(question.options):
                if i + 1 == question.correct:
                    txt.write("> " + option + " +" + "\n")
                else:
                    txt.write("> " + option + "\n")
            txt.write("\n")


def template(filename):
    with open(filename, "w") as txt:
        txt.write("@autor:<autor>" + "\n")
        txt.write("@title:<title>" + "\n")
        txt.write("@time:<time in minutes>" + "\n\n")
        for i in range(2):
            txt.write(f"# <question{i+1}>" + "\n")
            for j in range(3):
                if j == 0:
                    txt.write(
                        f"> <option{j+1} for question{i+1}> <'+' for correct answer>"
                        + "\n"
                    )
                else:
                    txt.write(f"> <option{j+1} for question{i+1}>" + "\n")
            txt.write("\n")


def main(argv):
    # file = argv[-1]
    file = "test.txt"
    if file.split(".")[-1] == "ttf":
        with open(file, "rb") as f:
            ttf(f)
    elif file.split(".")[-1] == "txt":
        with open(file, "r") as f:
            textfile(f)
    else:
        template("template.txt")


if __name__ == "__main__":
    main(sys.argv)
