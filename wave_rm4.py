# Copyright (c) 2020 cybernesto

import sys, re, struct, wave
import getopt

def usage():
	print('Usage: python wave_rm4.py [-hbv] <robi_file.rm4>\n')
	print('  -h       Show this help')
	print('  -b       make a backup of the input file')
	print('  -v       verbose output')

def calcWaveRMS(wavefile, steps):
	try:
		ifile = wave.open(wavefile)
		print("Processing " + wavefile)
		sw = ifile.getsampwidth()

		fmts = (None, "=B", "=h", None, "=l")
		fmt = fmts[sw]

		dcs  = (None, 128, 0, None, 0)
		dc = dcs[sw]

		samplerate = ifile.getparams()[2]

		ms = 0.
		rms = 0
		j=0
		k=0
		rmslist = []
		for i in range(ifile.getnframes()):
			if ms < steps[j]:
				iframe=ifile.readframes(1)
				rms = rms + (struct.unpack(fmt,iframe)[0]-dc)**2
				ms = ms+1000./samplerate
				k=k+1
			else:
				if j < len(steps) - 1:
					rmslist.append((rms/k)**.5)
					j=j+1
				else:
					print("pose too short!")
				
				rms =0
				ms=0
				k=0
		# Pad longer poses with 0s
		rmslist = rmslist + [0]*(len(steps)-j) 
		mean = sum(rmslist) / float(len(rmslist))
##		print(rmslist, mean)
##		print(steps)
##		print([x > mean/2 for x in rmslist])
##		print()
		return([x > mean/2 for x in rmslist])
	except:
		print("Cannot read file or file not found !")
		print(wavefile)
	finally:
		ifile.close()
	



def main():
	backup = False
	verbose = False
	
	print('Vocal luminiscence calculator for Robi v1.1b')
	print('Copyright cybernesto 2019 - 2022')
	print()
	try:
		opts, args = getopt.getopt(
		               sys.argv[1:],
		               'hbv',
		               ['help', 'backup', 'verbose'])
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)
    
	if len(args) == 0:
		usage()
		sys.exit(2)
	for o, a in opts:
		if o in ('-h', '--help'):
			usage()
			sys.exit()
		elif o in ('-b', '--backup'):
			backup = True
		elif o in ('-v', '--verbose'):
			verbose = True
			
	try:
		f = open(args[0], 'r', encoding="SHIFT_JIS")
		lines = f.readlines()
		print("Reading " + args[0])
		f.close()
	except OSError as e:
		print("Cannot read file or file not found !")
		print(args[0])
		exit()
	
	if backup:
		# save a backup file
		try:
			f = open(args[0][:-4]+'.BAK',"w", encoding="SHIFT_JIS", newline='\r\n')
			f.writelines(lines)
			f.close()
		except:
			print("Cannot write file or file not found !")
			print(args[0][:-4]+'.BAK')
			exit()

	#Read binary for address calculation
	try:
		f = open(args[0],"rb")
		byte = f.read(1)
		add = 0
		lineadds = [0]
		while byte:
			# Find EOL
			if byte == b'\n':
				lineadds.append(add+1)
			byte = f.read(1)
			add = add+1
	except OSError as e:
		print(f"{type(e)}: {e}")
		exit()			
	finally:
		f.close()

	blocks = {}
	tempBlock = {}
	splitregex = r'[<,>,=,"]'
	poseParse = False
	endtagpos = 0
	
	#Read text for RE Block parsing
	for i, line in enumerate(lines):
		if re.search(r'[^/]medit', line): #block
			# tempBlock was not added yet, because no jump was found but a new block
			# has started. Set the current address as the jump address of the last block
			# and add it to the list.
			if  tempBlock != {} and 'jumpAdd' not in tempBlock:
				tempBlock['jumpAdd'] = lineadds[i]
				blocks[tempBlock['address']] = tempBlock

			tempBlock = {}
			tempBlock['address'] = lineadds[i]
			tempBlock['line'] = i
		if re.search(r'block name', line): #name
			tempBlock['name'] = re.split(splitregex, line)[3]
		if re.search(r'\b(0x0b00)', line): #wait
			tempBlock['wait'] = int(re.split(splitregex, line)[8],0)*20
		if poseParse:
			if re.search(r'0x[0-9A-Fa-f]{4}', line):
				pose = pose + re.findall(r'0x[0-9A-Fa-f]{4}', line)
		if re.search(r'\b(0x0a00)', line): #pose
			pose = []
			poseParse = True
		if re.search(r'\b(play)', line): #play sound                        
			line = re.sub(r'\\','/',line)
			tempBlock['wavefile'] = "./" + re.split(splitregex, line)[3]
		if re.search(r'\b(jump)', line): #jumps
			tempBlock['jumpAdd'] = int(re.split(splitregex, line)[3],0)
			blocks[tempBlock['address']] = tempBlock
		if re.search(r'[/]mem_w', line) and poseParse:
			tempBlock['pose'] = pose
			poseParse = False
		if re.search(r'<',line): #tag begin
			if endtagpos < lineadds[i]:
				endtagpos = lineadds[i]


       
	# Check the wavefile list and go through the jump lines followed
	fixlines = []
	old = {}
	old['delays'] = []
	old['wavefile'] = []
	old['mouthRMS'] = []
	
	for b in blocks:
		if 'wavefile' in blocks[b]:			
			delays = []
			mouth = []
			waitLines = []
			waitAdds = []
			tempAdds = [] # Adress list to avoid endless loops

			address = blocks[b]['jumpAdd']
			while address < endtagpos and address not in tempAdds and 'wavefile' not in blocks[address]:
				tempAdds.append(address)
				#this could be sent to a translating service
				if verbose:
					if 'name' in blocks[address]:
						print(blocks[address]['name'], address)
				if 'wait' in blocks[address]:
					delays.append(blocks[address]['wait'])
					mouth.append(int(blocks[address]['pose'][70],0) != 0)
					waitAdds.append(address)
					#consider a fix distance from block begin and line with mouth data
					waitLines.append(blocks[address]['line']+6)
				address = blocks[address]['jumpAdd']
				
			if delays == old['delays'] and blocks[b]['wavefile'] == old['wavefile']:
				mouthRMS = old['mouthRMS']			
			else:
				try:
					#use the collected delays to calculate the RMS values
					mouthRMS = calcWaveRMS(blocks[b]['wavefile'], delays)
					old['mouthRMS'] = mouthRMS
					old['delays'] = delays
					old['wavefile'] = blocks[b]['wavefile']
				except:
					print("Command aborted")


			if mouth != mouthRMS:
				if verbose:
					print(mouth, "should be", mouthRMS)
				fixlines = fixlines + waitLines
				for i, line in enumerate(waitLines):
					a = blocks[waitAdds[i]]['pose'][48:72]
					if mouthRMS[i]:
						a[-2] = "0x0032"
					else:
						a[-2] = "0x0000"
					#lines[i] = ','.join(format(x, '#06x') for x in a)
					lines[line] = '\t'+','.join(a)+',\n'			
		

	# save the corrected file
	try:
		f = open(args[0],"w",encoding="SHIFT_JIS",newline='\r\n')
		f.writelines(lines)
		f.close()
	except:
		print("Cannot write file or file not found !")
		print(args[0])
		exit()
        

main()

