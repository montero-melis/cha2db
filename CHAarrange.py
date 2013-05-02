
"""Pseudocode for arranging the body of the transcription into right format"""

## transcription body:
# Take a parsed CHA object as input:
def arrange(parsedObj):
	arranged = []
	
	# initialize video, role and text variables
	vid = ""
	textSuj = ""
	textExp = ""

	# for now this makes only sense starting AFTER the metainformation,
	# i.e. when encountering the first @G tuple
	for tup in parsedObj:
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


## Metainformation
def arrangeMeta(parsedObj):
	meta = dict()

	# Initialize variables for metainformation
	# This is actually not needed, but put explanatory comments after each key-value assignment below
	lang_interact = "" # language of interaction
	ppt_name = "" # 'ppt' stands for participant
	ppt_role = ""
	ppt_gender = ""
	ppt_group = ""
	exp_name = "" # 'exp' stands for experimenter
	transcr = "" # name of transcriber
	order = ""

	for tup in parsedObj:
		if tup[0] == '@Languages':
			meta['lang_interact'] = tup[1]
		elif tup[0] == '@Participants':
			# Little regex needed here:
			# split tup[1] by comma ','
			# for each side of the comma:
			# NB Write the conditional statements so that BOTH are checked
				#if the 1st word == SUJ
					# meta['ppt_name'] = 2nd word
					# meta['ppt_role'] = 3rd word
				# if 1st word == EXP
					#meta['exp_name'] = 2nd word
		elif tup[0] == '@ID':
			listID = # split tup[1] by pipes '|' and create list whose elements are each field before a pipe
			if listID[2] == 'SUJ':
				meta['ppt_gender'] = listID[4]
				meta['ppt_group'] = listID[5]
			elif listID[2] == 'EXP':
				meta['exp_gender'] = listID[4]
		elif tup[0] == '@Transcriber':
			meta['transcr'] = tup[1]
		elif tup[0] == '@Comment':
			# This field is a bit more tricky because there might be different tipes of comments
			# see if it matches with (case insensitive) 'ord'
			# if true, grep whatever digit or group of digits come directly after that string (no whitespaces)
			# the format might be '1' or '01', and there are only four orders 1,2,3,4 (or 01,02,03,04)
				# meta['order'] = that number




