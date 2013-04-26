#!/usr/bin/env python2

import re
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

class CHA:
    def __init__(self, file): 
        self.file = file
        self.parse()
        
    def parse(self):
        cha = []
        f = open(self.file)
    
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
    
        self.cha = cha
        return cha
 
    def pp(self):
        pp(self.cha)
        
if __name__ == "__main__":    
    file = "SpAD_119_pop_or4_ori.cha"
    
    cha = CHA(file)
    #cha.pp()

for tup in cha.parse():
	print tup
