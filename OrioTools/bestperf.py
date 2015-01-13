import re
import os
import sys
import glob

bestfile = ''
bestTime = 1000000
acumAll = 0

for filename in glob.glob("./times/time_of_*"):

	print filename

	acum = 0
	timesAcum = 0

	f = open(filename)

	for line in f:

		split1 = re.split(': | |\n',line)
		if len(split1) > 3 and split1[0] == 'Time':
			timesAcum = timesAcum + float(split1[5])
			acum = acum + 1

	f.close()

	if acum >0 and timesAcum>0:
		timesAcum = timesAcum / acum


		print "Result for: ",filename," = ",timesAcum
		if timesAcum < bestTime:
			bestfile = filename
			bestTime = timesAcum
			acumAll = acum

print "Best times: "
print "\t filename: ",bestfile
print "\t time: ",bestTime

	





