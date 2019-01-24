#!/usr/bin/env python3
"""
Triumvirate Code Challenge from #########
Program to find the most common three word sequences within inputted text.

Created 11/2018
"""

import argparse
import re
import select
import sys
from collections import defaultdict


class Triumvirate:

    READ_SIZE = 1
    RESULT_SIZE = 100
    LETTER_MATCH = r"([a-zA-Z])"        # letters only

    def __init__(self, args):

        self.args = args
        self.combo_dict = defaultdict(int)
        self.new_word = []  # char list
        self.first_word = ""
        self.second_word = ""
        self.third_word = ""
        self.output_string = ""

    def execute(self):

        self.process_stdin()
        self.process_filename_args()
        ordered_list_of_tuples = self.sort_and_order_dict()
        self.format_final_list(ordered_list_of_tuples)

        print("finished!")

    def process_filename_args(self):

        for target in self.args.file:
            with open(target.name) as file_pointer:

                while 1:
                    character = file_pointer.read(self.READ_SIZE)
                    self.process_character(character)
                    if not character:
                        break  # end of file

    def process_stdin(self):

        """not pretty way to see if stdin has data"""
        if select.select([sys.stdin, ], [], [], 0.0)[0]:

            while 1:
                character = sys.stdin.read(self.READ_SIZE)
                self.process_character(character)
                if not character:
                    break  # end of file

    def process_character(self, character):
        was_added_to_word = self.add_char_to_word(character)  # true or false
        complete_word = self.is_new_word(was_added_to_word)
        if complete_word:
            self.update_words()
            self.push_to_dict()

    def add_char_to_word(self, character):

        return_value = False
        if re.match(self.LETTER_MATCH, character):  # if it is a character
            self.new_word.append(character.lower())
            return_value = True
        return return_value

    def is_new_word(self, was_added_to_word):

        return_value = False
        if not was_added_to_word and len(self.new_word) != 0:
            return_value = True
        return return_value

    def update_words(self):

        word = "".join(self.new_word)
        self.first_word = self.second_word
        self.second_word = self.third_word
        self.third_word = word
        self.new_word = []

    def push_to_dict(self):

        if self.first_word:
            three_word_string = "{0} {1} {2}".format(
                self.first_word, self.second_word, self.third_word)
            self.combo_dict[three_word_string] += 1

    def sort_and_order_dict(self):
        return sorted(self.combo_dict.items(), key=lambda kv: kv[1], reverse=True)

    def format_final_list(self, ordered_list_of_tuples):

        output_list = []

        for index, value in enumerate(ordered_list_of_tuples):

            if index < self.RESULT_SIZE:

                if (index + 1) == len(ordered_list_of_tuples) or (index + 1) == self.RESULT_SIZE:
                    output_list.append("{0} - {1}".format(value[1], value[0]))
                else:
                    output_list.append("{0} - {1}, ".format(value[1], value[0]))
            else:
                break

        self.output_string = ''.join(output_list)
        print(self.output_string)
        return self.output_string


if __name__ == "__main__":

    description = \
        "description: \n" \
        "The Triumvirate program is meant to find the 100 most common " \
        "three word sequences in inputted text files.\n" \

    epilog = \
        "examples of use: \n" \
        "  ./triumvirate.py ./tmp/testfile.txt\n" \
        "  ./triumvirate.py ./tmp/testfileone.txt ./tmp/testfiletwo.txt\n" \
        "  cat ./tmp/testfile.txt | ./triumvirate.py\n"

    parser = argparse.ArgumentParser(epilog=epilog,
                                     description=description,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('file', type=argparse.FileType('r'), nargs='*')
    input_args = parser.parse_args()

    tri = Triumvirate(input_args)
    tri.execute()
