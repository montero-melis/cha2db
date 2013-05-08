#!/usr/bin/env python2

import re
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

class CHA:
    def __init__(self, file): 
        self.file = file
        self.extract()
        self.parse_body()
        self.parse_meta()
        
    def extract(self):
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
    
        self.extracted = cha
        return self.extracted
 
    
    def parse_body(self):
    # works on self.extracted; parses transcription body
        body = []
        
        # initialize video, role and text variables
        vid = ""
        textSuj = ""
        textExp = ""
    
        # for now this makes only sense starting AFTER the metainformation,
        # i.e. when encountering the first @G tuple
        for tup in self.extracted:
            c_key = tup[0]
            c_val = tup[1]    # CAMBIAR TODAS LAS OCURRENCIAS!
            if c_key == "@G":
                if vid:
                    body.append([vid, "*SUJ", textSuj])
                    body.append([vid, "*EXP", textExp])
                    textSuj = ""
                    textExp = ""
                vid = c_val
            else:           
                if c_key == "*EXP":
                    textExp += " " + c_val
                elif c_key == "*SUJ":
                    textSuj += " " + c_val
                    
        self.parsed_body = body
        return self.parsed_body
    
    
    ## Metainformation
    def parse_meta(self):
        meta = dict()
        #These are the dictionary keys parsed from the transcription header:
            # 'lang_interact': language of interaction
            # 'ppt_name': participant name
            # 'ppt_role': participant role
            # 'ppt_gender': gender of participant
            # 'ppt_group': group of the participant
            # 'exp_name': experimenter name
            # 'transcr': name of transcriber
            # 'order': one of th*e four semi-randomized orders in which the videoclips were shown
    
        for tup in self.extracted:
            c_key = tup[0]
            c_val = tup[1]    # CAMBIAR TODAS LAS OCURRENCIAS!
            # Check language of interaction
            if c_key == '@Languages':
                meta['lang_interact'] = c_val
            # Check participants' names and roles
            elif c_key == '@Participants':
                listParticipants = c_val.split(",")
                for field in listParticipants:
                    if field.split()[0] == "SUJ":
                        meta['ppt_name'] = field.split()[1] # participant name
                        meta['ppt_role'] = field.split()[2] # participant role
                    elif field.split()[0] == "EXP":
                        meta['exp_name'] = field.split()[1] #experimenter name
            # Check other information about participants
            elif c_key == '@ID':
                listID = c_val.split("|")
                # split c_val by pipes '|' and create list whose elements are each field before a pipe
                if listID[2] == 'SUJ':
                    meta['ppt_gender'] = listID[4]
                    meta['ppt_group'] = listID[5]
                elif listID[2] == 'EXP':
                    meta['exp_gender'] = listID[4]
            # check transcriber's name
            elif c_key == '@Transcriber':
                meta['transcr'] = c_val
            # check order in which the videos where shown (1--4)
            elif c_key == '@Comment':
                r_order = re.compile(r"ord(er)? *0?([1-4])", re.I)
                m = r_order.match(c_val)
                if m:
                    meta['order'] = m.group(2)
                    
        self.parsed_meta = meta
        return self.parsed_meta
    
        
if __name__ == "__main__":    
    file = "SpAD_119_pop_or4_ori.cha"
    
    cha = CHA(file)      
    pp(cha.parsed_meta)
    pp(cha.parsed_body)
    