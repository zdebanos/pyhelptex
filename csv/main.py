import sys
import argparse
from common.PyhelptexFunction import PyhelptexFunction
from common.common import to_stderr


class CsvFunction(PyhelptexFunction):
    def __init__(self, name):
        self._name = name
        self.input_file_name = None
        self.output_file_name = None
        self.delimeter = None
        self.convert_dots_to_commas = None

    @property
    def name(self):
        return self._name

    def __call__(self, input_file, output_file, delimeter, convert_dots_to_commas):
        self.input_file_name = input_file
        self.output_file_name = output_file
        self.delimeter = delimeter
        self.convert_dots_to_commas = convert_dots_to_commas
        self._main()

    def call_script(self, arguments):
        self.input_file_name, self.output_file_name, self.delimeter, \
            self.convert_dots_to_commas = self.analyze_args(arguments)
        to_stderr("CSV2TEX Launching")
        self._main()


    def csv_extractor(self, file_name, delimeter):
        ptr = self.file_examiner(file_name)
        if (ptr is None):
            sys.exit()
        else:
            lines = []
            ret = []
            line_count = 0
            max_rows = 0
            lines = [line.strip() for line in ptr.readlines()]
            for line in lines:
                buf = line.split(delimeter)
                length_buf = len(buf)
                if length_buf > max_rows:
                    max_rows = length_buf 
                for word in buf:
                    word = word.replace('.', ',')
                ret.append(buf)
                line_count += 1
        ptr.close()
        return ret, line_count, max_rows

    def file_writer(self, file_name, phrase):
        try:
            f = open(file_name, "w")
            f.write(phrase)
        except:
            print("error writing to file", file_name)
        f.close()

    def file_examiner(self, file_name):
        try:
            f = open(file_name, encoding='utf-8') 
            print(file_name, "opened")
            return f
        except FileNotFoundError:
            to_stderr(file_name, "does not exist, quitting")
            return None

    def analyze_args(self, arguments):
        parser = argparse.ArgumentParser() 
        parser.add_argument("input_file", help="the input .csv file")
        parser.add_argument("output_file", help="name of the .tex output file")
        parser.add_argument("delimeter", help="the delimeter of values")
        parser.add_argument("-cdtc","--convert-dots-to-commas",\
            help="convert dots to commas (useful when working with dec. commas)",\
            action="store_true")
        arguments.pop(0)
        args = parser.parse_args(args=arguments)
        if args.convert_dots_to_commas and args.delimeter == '.':
            print("delimeter is dot and trying to convert dots to commas - quitting")
            sys.exit()
        return args.input_file, args.output_file, args.delimeter,\
            args.convert_dots_to_commas

    def generate_tex_table(self, csv_list, lines, max_rows, convert_dots_to_commas):
        ret_table = ""
        to_stderr("Generating TeX table of", lines, "lines")
        if lines == 0:
            to_stderr("zero rows - no table generated, quitting")
            sys.exit()
        tabular_header = "\\begin{tabular}{"
        for row in range(max_rows):
            if row == 0:
                tabular_header += "||"
            tabular_header += "c|"
            if row == max_rows-1:
                tabular_header += "|"

        tabular_header += "}\n"
        ret_table += tabular_header # \begin{tabular}{...}
        ret_table += "\\hline\n"
        for line in csv_list:
            buf = ""
            length = len(line)
            for row in range(length):
                if row == length-1:
                    buf += line[row] + " "
                else:
                    buf += line[row] + " & "
            if length < max_rows:
                for i in range(max_rows-length):
                    buf += "& "
            buf += "\\\\\n"
            ret_table += buf
            ret_table += "\\hline\n"
        ret_table += "\\end{tabular}\n"
        if convert_dots_to_commas:
            ret_table = ret_table.replace(".", ",")
        return ret_table

    def _main(self):
        csv_list, lines, max_rows = self.csv_extractor(self.input_file_name, self.delimeter)
        table = self.generate_tex_table(csv_list, lines, max_rows, self.convert_dots_to_commas)
        self.file_writer(self.output_file_name, table)
        