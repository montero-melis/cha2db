#!/usr/bin/env python2

import re
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint


class CHA:
    def __init__(self, file): 
        self.file = file
        self.extract()
        self.parse_meta()
        self.parse_body()
        self.process_body()
        

    def extract(self):
        cha = []
        f = open(self.file)
    
        # Regular expression to extract command and text
        reg_command_text = re.compile("^(.*?):(.*)$")
    
        # initialize text and command
        command = ""
        text = ""
    
        for line in f.readlines():
            line = line.rstrip()
    
            if line[0] != "\t":
                # new command
    
                # is there an old command and text to be appended?
                if text and command:
                    text = text.strip()
                    cha.append((command,text))
    
                m = reg_command_text.match(line)
                if m:
                    command = m.group(1).strip()
                    text = m.group(2).strip()
            else:
                # continuation of a previous command
                text += " " + line.strip()
    
        self.extracted = cha
        return self.extracted


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
            # TODO: add other comment keys (comment1, comment2 etc for other comments in transcriptions)
    
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
                reg_order = re.compile(r"ord(er)? *0?([1-4])", re.I)
                m = reg_order.match(c_val)
                if m:
                    meta['order'] = m.group(2)
                    
        self.parsed_meta = meta
        return self.parsed_meta
    
    
    def parse_body(self):
    # works on self.extracted; parses transcription body
        body = []
        
        # initialize video, role and text variables
        vid = ""
        textSuj = ""
        textExp = ""
    
        for tup in self.extracted:
            c_key = tup[0]
            c_val = tup[1]
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
        if vid: # Make sure the last tuple finds its way into the list 'body'
            body.append([vid, "*SUJ", textSuj])
            body.append([vid, "*EXP", textExp])

                    
        self.parsed_body = body
        return self.parsed_body


    def process_body(self):
        body = self.parsed_body[:] # Create copy of object to maintain independence of attributes

        # regexes to match repetitions ("[/]") and retracings ("[//]") with all their scoped text
        # the scope is either the preceding "<...>" or the preceding word
        reg_repet = re.compile(r"<[^>]+>\s*\[\/\]|\w+\s*\[\/\]")    # repetitions
        reg_retra = re.compile(r"<[^>]+>\s*\[\/\/\]|\w+\s*\[\/\/\]")    # retracings

        for descr in body: # for each description
            text = descr[2]
            
            text = re.sub("\x15.*?\x15","",text)    # remove NAK (sound bullets)
            text = re.sub("\+<","",text)            # remove "lazy" overlapping markers "+<"
            text = re.sub("\(\.\)","",text)         # remove pauses "(.)"
            text = re.sub(reg_repet,"",text)        # rm repetitions (marked by "[/]")
            text = re.sub(reg_retra,"",text)        # rm retracings (marked by "[//]")
            # remove all repeated white spaces
            # strip all white spaces from beginning and end of line
            
            descr[2] = text # replace description slot with processed string
        
        self.processed_body = body
        return self.processed_body


if __name__ == "__main__":    
    file = "SpAD_119_pop_or4_ori.cha"
    
    cha = CHA(file)      
    pp(cha.parsed_meta)
    pp(cha.parsed_body)
    #pp(cha.processed_body)
    