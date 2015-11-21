import unittest
import os
import sys
from io import StringIO
import ply.yacc as yacc

from lab03.Cparser import Cparser
from lab03.TypeChecker import TypeChecker


def read_file(fpath):
    with open(fpath) as f:
        return f.read()


class capture:
    def __enter__(self):
        self.oldout = sys.stdout
        newout = sys.stdout = StringIO()
        return newout

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.oldout


class ErrorsTest(unittest.TestCase):
    pass


def generate_tests(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(".in"):
                test_name = "test_{0}".format(filename[0:-3])
                test_file_path = os.path.join(root, filename)
                expected_file_path = os.path.join(root, filename[0:-2] + "expected")

                test_input = read_file(test_file_path)
                expected = read_file(expected_file_path)

                def test(self):
                    # given
                    cparser = Cparser()
                    parser = yacc.yacc(module=cparser)
                    ast = parser.parse(test_input, lexer=cparser.scanner)

                    # when
                    with capture() as outstream:
                        TypeChecker().visit(ast)
                        actual = outstream.getvalue()

                    # then
                    self.assertEqual(expected, actual)

                setattr(ErrorsTest, test_name, test)


generate_tests("tests_err")

if __name__ == "__main__":
    unittest.main()

