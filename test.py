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
      

# Take a parsed CHA object as input:
def arrange(CHAobj):
    arranged = []
    
    # initialize video, role and text variables
    vid = ""
    textSuj = ""
    textExp = ""

    # for now this makes only sense starting AFTER the metainformation,
    # i.e. when encountering the first @G tuple
    for tup in CHAobj:
        if tup[0] == "@G":
            if vid:
                arranged.append([vid, "*SUJ", textSuj])
                arranged.append([vid, "*EXP", textExp])
                textSuj = ""
                textExp = ""
            vid = tup[1]
        else:           
            if tup[0] == "*EXP":
                textExp += " " + tup[1]
            elif tup[0] == "*SUJ":
                textSuj += " " + tup[1]
    return arranged


if __name__ == "__main__":    
    file = "SpAD_119_pop_or4_ori.cha"
    
    cha = CHA(file)
    #cha.pp()

# for tup in cha.parse():
# 	print tup

outp= cha.parse()
#print outp
pretp = pprint.PrettyPrinter(indent=4)
pretp.pprint(arrange(outp))
#print arrange(outp)
