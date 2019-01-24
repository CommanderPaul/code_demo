#!/usr/bin/env python3

import os
import unittest
from triumvirate import Triumvirate
import tempfile
import shutil
from subprocess import Popen
from subprocess import PIPE


class TriumvirateTests(unittest.TestCase):

    TEST_TEXT = '''
    
    bears beets beans beet bears but not beers.
    Beer beer beer?
    beans beer beans        * beans-bear-beans?
    beans,beer,beans == >> beer! beer! Beer! bEEr
    BaCON[beer[bacon]]bAcon{beer}}bacon
    beer----------->beer  beer
    bacon&beer&bacon
    '''

    EXPECTED_OUTPUT = "4 - beer beer beer, 3 - beer bacon beer, " \
                      "3 - bacon beer bacon, 2 - beer beans beer, " \
                      "2 - beans beer beans, 2 - beer beer bacon, 1" \
                      " - bears beets beans, 1 - beets beans beet, " \
                      "1 - beans beet bears, 1 - beet bears but, 1 " \
                      "- bears but not, 1 - but not beers, 1 - not" \
                      " beers beer, 1 - beers beer beer, 1 - beer " \
                      "beer beans, 1 - beer beans beans, 1 - beans " \
                      "beans bear, 1 - beans bear beans, 1 - bear " \
                      "beans beans, 1 - beans beans beer, 1 - beans " \
                      "beer beer, 1 - beer bacon bacon, 1 - bacon " \
                      "bacon beer, 1 - bacon beer beer\nfinished!\n"

    def test_piped_input(self):

        test_directory = tempfile.mkdtemp(
            prefix='filetest_'
        )
        file_path = os.path.join(test_directory, 'filename')
        file_pointer = open(file_path, 'w')
        file_pointer.write(self.TEST_TEXT)
        file_pointer.close()
        test_file = test_directory + "/filename"
        p1 = Popen(["cat", test_file], stdout=PIPE)
        p2 = Popen(['./triumvirate.py'], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()
        result = p2.communicate()[0]
        p1.wait()
        self.maxDiff = None
        self.assertEqual(self.EXPECTED_OUTPUT, result.decode("utf-8"))
        shutil.rmtree(test_directory)

    def test_file_input(self):

        test_directory = tempfile.mkdtemp(
            prefix='filetest_',
        )
        file_path = os.path.join(test_directory, 'filename')
        file_pointer = open(file_path, 'w')
        file_pointer.write(self.TEST_TEXT)
        file_pointer.close()
        test_file = test_directory + "/filename"
        output = Popen(['./triumvirate.py', test_file], stdout=PIPE)
        self.maxDiff = None
        self.assertEqual(self.EXPECTED_OUTPUT,
                         output.stdout.read().decode("utf-8"))
        output.stdout.close()
        output.wait()
        shutil.rmtree(test_directory)

    def test_is_new_word(self):

        args = "some args from argparse"
        tri = Triumvirate(args)

        tri.new_word = []
        result = tri.is_new_word(True)
        self.assertFalse(result)

        tri.new_word = ["beans"]
        result = tri.is_new_word(True)
        self.assertFalse(result)

        tri.new_word = []
        result = tri.is_new_word(False)
        self.assertFalse(result)

        tri.new_word = ["beans"]
        result = tri.is_new_word(False)
        self.assertTrue(result)

    def test_add_char_to_word(self):

        args = "some args from argparse"
        tri = Triumvirate(args)

        result = tri.add_char_to_word('a')
        self.assertTrue(result)

        result = tri.add_char_to_word('-')
        self.assertFalse(result)

    @staticmethod
    def test_read_size():
        assert Triumvirate.READ_SIZE == 1


if __name__ == '__main__':
    unittest.main()
