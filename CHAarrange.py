import re
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
	#These are the dictionary keys extracted from the transcription header:
		# 'lang_interact': language of interaction
		# 'ppt_name': participant name
		# 'ppt_role': participant role
		# 'ppt_gender': gender of participant
		# 'ppt_group': group of the participant
		# 'exp_name': experimenter name
		# 'transcr': name of transcriber
		# 'order': one of the four semi-randomized orders in which the videoclips were shown

	for tup in parsedObj:
		# Check language of interaction
		if tup[0] == '@Languages':
			meta['lang_interact'] = tup[1]
		# Check participants' names and roles
		elif tup[0] == '@Participants':
			listParticipants = tup[1].split(",")
			for field in listParticipants:
				if field.split()[0] == "SUJ":
					meta['ppt_name'] = field.split()[1]	# participant name
					meta['ppt_role'] = field.split()[2]	# participant role
				elif field.split()[0] == "EXP":
					meta['exp_name'] = field.split()[1]	#experimenter name
		# Check other information about participants
		elif tup[0] == '@ID':
			listID = tup[1].split("|")
			# split tup[1] by pipes '|' and create list whose elements are each field before a pipe
			if listID[2] == 'SUJ':
				meta['ppt_gender'] = listID[4]
				meta['ppt_group'] = listID[5]
			elif listID[2] == 'EXP':
				meta['exp_gender'] = listID[4]
		# check transcriber's name
		elif tup[0] == '@Transcriber':
			meta['transcr'] = tup[1]
		# check order in which the videos where shown (1--4)
		elif tup[0] == '@Comment':
			r_order = re.compile(r"ord(er)? *0?([1-4])")
			m = r_order.I(tup[1])
			if m:
				meta['order'] = m.group(2)
	return meta

