cha2db
======

Python program: takes transcriptions in .cha format (see CHILDES project or TalkBank.org) as input, and outputs the relevant information in SQLite database format.

Short description of the individual programs:

CHAparse.py
-----------

Parses the transcriptions for the linguistic Popi task, which follow CHILDES conventions and are in .cha format.
The output is a dictionary-type of structure for the metadata included in the transcriptions (i.e. the information in the header), and a list-type of structure for the body of the transcriptions. 
The list for the transcription-body is a list of lists having three entries: [videoname, role, word].
Role refers to either *SUJ (the participant) or *EXP (the experimenter).

dbPopul.py
----------

This program populates the database with the output from CHAparse.py (see above).
