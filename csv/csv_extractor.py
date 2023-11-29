# file_examiner checks the existence of a file
# csv_extractor extracts words surrounded by ','

import sys

def file_examiner(file_name):
    try:
        f = open(file_name, encoding='utf-8') 
        print(file_name, "opened")
        return f
    except FileNotFoundError:
        print('"', file_name, '"', "does not exist, quitting")
        return None

def csv_extractor(file_name, delimeter, convert_dots_to_commas):
    ptr = file_examiner(file_name)
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
