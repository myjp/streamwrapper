#!/usr/bin/env python

import time
import re
import datetime
import os

# specify output directory for your recordings
OUTPUT_DIR = "~/"

print "Step by step assistant for scheduled stream recordings using streamripper and at jobs."

# recording name (important for file name)
while 1:
	print "Enter recording name:",
	input = raw_input()

	# basic post-processing of input  / avoid blanks in file name
	input = input.strip()
	input = input.replace(" ", "-")

	# checks if input is empty (Warning: No further checks!)
	if len(input) > 0:
		name = input
		break
	else:
		print "Input is empty.  Try again."

# stream url
while 1:
	print "Enter stream URL:",
	input = raw_input()
	input = input.strip()

	if len(input) > 0:
		url = input
		break
	else:
		print "Input is empty.  Try again."



# date of scheduled recording
while 1:
	print "Enter recording date [dd.mm.yyyy]:",
	input = raw_input()
	input = input.strip()

	try:
		startdate = time.strptime(input, "%d.%m.%Y")
		break
	except ValueError:
		print "Wrong input format [dd.mm.yyyy].  Try again."


# time of scheduled recording
while 1:
	print "Enter recording time [hh:mm]:",
	input = raw_input()
	input = input.strip()

	try:
		starttime = time.strptime(input, "%H:%M")
		break
	except ValueError:
		print "Wrong input format [hh:mm].  Try again."

# length of recording
while 1:
	print "Enter recording length [hh:mm]:",
	input = raw_input()
	input = input.strip()

	# manual check of input with regular expression
	if re.match("\d+:[0-5]\d", input) != None:		
		ipt_hours = int(input.split(":")[0])
		ipt_minutes = int(input.split(":")[1])

		length = datetime.timedelta(hours=ipt_hours, minutes=ipt_minutes)
		break
	else:
		print "Wrong input format [hh:mm].  Try again."

# creating file name of recording
filename = time.strftime("%Y-%m-%d", startdate) + "_" + time.strftime("%H:%M", starttime) + "_" + name

# creating streamripper command
streamripper = "streamripper %(url)s -s -A -l %(length)s -d %(outputdir)s -a %(filename)s" % {"url" : url, "length" : length.seconds, "outputdir" : OUTPUT_DIR, "filename" : filename}

# creating at command
at = "echo '%(streamripper)s' | at -M %(time)s %(date)s" % {"streamripper" : streamripper, "time" : time.strftime("%H:%M", starttime), "date" : time.strftime("%m/%d/%Y", startdate)}

# execute command
os.system(at)
