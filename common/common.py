import sys

def to_stderr(*args, sep=' '):
    output = sep.join(map(str, args))
    print(output, file=sys.stderr)

def to_stdout(*args, sep=' '):
    output = sep.join(map(str, args))
    print(output, file=sys.stdout)

