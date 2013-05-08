/130424
/Development plan for cha2db program
/G Montero-Melis

This file is still a high-level development plan, but it considers the actual architecture of the Python program.

See Downey (2009, p.176 and p.37)

1. Parse `transcription.cha`
========================

The `parse` method of the CHA class parses a transcription file in .cha format.
The output is a list of tuples.
The first element in each tuple contains what could be called a key, while the second contains a value.
(**NOTE: For consistency, change variable names in `CHA.parse`: command-->key, text-->value**)

Keys and values in a parsed CHA object
----------------------------------

Keys contain any of the information that is found at the beginning of a line in the transcription file.
It is natural to establish a division between header-keys and body-keys.

**Header-keys** include metainformation such as the languages that are used: `@Languages`, whose value is a three letter code for a language (e.g. 'spa' for Spanish); they also contain information about the participants: `@Participants`, `@ID`, and so on, whose values will help sorting the data.
There are more than half a dozen header-keys.

**Body-keys** belong to the body of the transcription, which contains the actual spoken interaction.
Body-keys are of two kinds: keys that start with an asterisk `*` identify the speaker, either as the experimenter (`*EXP`) or as the participant/subject (`*SUJ`). 
Their respective values are single sentences, that is, utterances containing a single main verb.
The other text-key is `@G` whose value is the videoclip that is being described, e.g. `prd_balcol`.
So the `@G`-tuples provide the context to which the utterances refer.


2. Processing of the parsed CHA object
=================================

There is much stuff in the transcriptions we want to get rid off before we start populating the database.
All of this stuff is of course there in the parsed object as well.
Getting rid of what is not needed is done in this 2nd step.

It is natural to divide the processing into **header-processing** and **body-processing**, since each of these need different type of processing.
The architecture of the program should reflect this, so that it becomes easy to change something in how the metainformation contained in the transcription header is processed without having to worry about whether these changes will affect the info from the body of the transcription, and viceversa.

