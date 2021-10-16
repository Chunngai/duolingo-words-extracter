import argparse
import datetime
from typing import List

import openpyxl


def get_words_in(sheet, only_just_now: bool = False) -> List[str]:
    words: List[str] = []

    for row in sheet.rows:
        word_cell = row[0]
        word = word_cell.value

        if not only_just_now:
            words.append(word)
        else:
            last_practice_cell = row[2]
            last_practice = last_practice_cell.value
            if last_practice == "Just now":
                words.append(word)

    return words


def main(args: argparse.Namespace):
    workbook = openpyxl.load_workbook(filename=args.logs)

    # The first sheet is the "Learnt" sheet
    # that stores all the words learnt
    # and their related info
    # in the form of (word, lesson, record time).
    learnt_sheet = workbook["Learnt"]
    learnt_words = get_words_in(learnt_sheet, only_just_now=False)

    # The newer sheet defaults to the last sheet.
    newer_sheet_index: int = -1
    # Newer sheet provided.
    if args.new_log is not None:
        try:
            newer_sheet_index = workbook.sheetnames.index(args.new_log)
        except ValueError:
            print(f"{args.n} is not a sheet name in the file.")
            exit(0)
    newer_sheet = workbook.worksheets[newer_sheet_index]
    newer_words = get_words_in(newer_sheet, only_just_now=False)
    newer_sheet_name = workbook.sheetnames[newer_sheet_index]

    older_sheet_index = newer_sheet_index - 1
    older_sheet = None
    try:
        older_sheet = workbook.worksheets[older_sheet_index]
    except IndexError:
        print("No older sheet exists.")
        exit(0)
    older_words = get_words_in(older_sheet, only_just_now=False)

    if len(workbook.sheetnames) == 1:
        # There are only two sheets: the "Learnt" sheet and the newer sheet.
        words_to_write = newer_words
    elif len(older_words) == len(newer_words):
        # There are no new words.
        # Collects words of the lastly reviewed lesson.
        lastly_reviewed_words = set(get_words_in(newer_sheet, only_just_now=True)) - set(learnt_words)
        words_to_write = sorted(list(lastly_reviewed_words - set(learnt_words)))
    else:
        # There are new words.
        new_words = set(newer_words) - set(older_words)
        words_to_write = sorted(list(new_words - set(learnt_words)))

    # Prints the words.
    if len(words_to_write) != 0:
        cur_time_repr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for word in words_to_write:
            print(word)
            learnt_sheet.append([word, newer_sheet_name, cur_time_repr])
        learnt_sheet.append([" "])
    # Save.
    workbook.save(args.logs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--new-log")
    parser.add_argument("--logs", default="duolingo_logs.xlsx")
    args = parser.parse_args()

    main(args)
