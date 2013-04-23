#!/usr/bin/env python2

import re
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

def cha_unpickle(file):
    cha = []
    f = open(file)

    # Regular expression to extract command and text
    r_command_text = re.compile("^(.*?):(.*)$")

    # initialize text and command
    command = ""
    text = ""

    for line in f.readlines():
        line = line.rstrip()

        if line[0] != "\t":
            # new command

            # is there an old command and text to be appended?
            if text and command:
                # remove NAK
                text = re.sub("\x15.*?\x15","",text).strip()
                cha.append((command,text))

            m = r_command_text.match(line)
            if m:
                command = m.group(1).strip()
                text = m.group(2).strip()
        else:
            # continuation of a previous command
            text += " " + line.strip()

    return cha

def print_cha(cha):
    pp(cha)
    # for t in cha:
    #     print t[0]
    #     print t[1]
if __name__ == '__main__':
    cha = cha_unpickle('SpAD_119_pop_or4_ori.cha')
    print_cha(cha)
