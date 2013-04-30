
"""Pseudocode for arranging the body of the transcription into right format"""

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





