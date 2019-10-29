"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!


"""
#gr-morsecode-enc: a morse-code encoder
#-----------------------------------------------------------------------
#
#
#This is the alpha test release of gr-morsecode-enc, a embedded python block for generating and
#sending morse-code.
#
#The python code itself is located inside the "morse-code generator" epy_block and as a seperate file "gr-morsecode-enc.py".
#
#
# (C) Kristoff Bonne, ON1ARF
# GPL v3
#
#Release-information:
#Version: 0.0.1 (20190221)
#
# 73s . kristoff - ON1ARF


import numpy as np
from gnuradio import gr

from bitstring import BitArray

import time



class morsecode_enc(gr.sync_block):
	def __createmorsecode(self, text):
		morsecode={
		'A': '.-',     'B': '-...',   'C': '-.-.', 
		'D': '-..',    'E': '.',      'F': '..-.',
		'G': '--.',    'H': '....',   'I': '..',
		'J': '.---',   'K': '-.-',    'L': '.-..',
		'M': '--',     'N': '-.',     'O': '---',
		'P': '.--.',   'Q': '--.-',   'R': '.-.',
		'S': '...',    'T': '-',      'U': '..-',
		'V': '...-',   'W': '.--',    'X': '-..-',
		'Y': '-.--',   'Z': '--..',

		'0': '-----',  '1': '.----',  '2': '..---',
		'3': '...--',  '4': '....-',  '5': '.....',
		'6': '-....',  '7': '--...',  '8': '---..',
		'9': '----.',
		'.': '.-.-.-',	',': '--..--',	'?': '..--..',
		'!': '-.-.--', '-': '-....-', '/': '-..-.',
		':': '---...',	'\'':'.----.',	')': '-.--.-',
		';': '-.-.-',	'(': '-.--.',	'=': '-...-',
		'@': '.--.-.',	'&': '.-...'
		}

		cwtext=""

		count_w=0
		for word in text.split():
			cwtext += "0000000" if count_w > 0 else ""
			count_w += 1

			count_c=0
			for c in word:
				# if not first char in word, add space to previous char
				cwtext += "000" if count_c > 0 else ""
				count_c+=1

				try:
					cwcode=morsecode[c.upper()]
				except KeyError:
					raise ValueError(c)
				#end try


				count_cw=0
				for b in cwcode:
					cwtext += "0" if count_cw > 0 else ""
					count_cw +=1

					if b == ".":
						cwtext+="1"
					elif b == "-":
						cwtext+="111"
					else:
						raise ValueError(b)
					#end else - elif - if
				#end for (cwcode)

			#end for (characters)

		# end for (words)
		return(cwtext)
	#end def __createmorsecode



	def __init__(self, wpm = 18, samplerate = 48000, sleeptime= 5, text="CQ CQ CQ CQ DE ON1ARF ON1ARF K"):  # only default arguments here
		gr.sync_block.__init__(
			self,
			name='morsecode encoder',
			in_sig=[],
			out_sig=[np.complex64]
		)



		# morse-code speed is defined as "Words per minute". This "word" is "Paris" (50 time-units)
		# one timeunit = 60 / (50 * wpm), ... or 1.2 / wpm
		# number of samples per timeunit = timeunit * samplerate

		self.numsamp=int(round(samplerate*1.2/wpm))
		self.numsamp_sleep = int(round(samplerate * sleeptime / self.numsamp))


		self.cwmessage = self.__createmorsecode(text)
		self.cwmessagelen = len(self.cwmessage)
		# we send packers of "numsamp" samples
		self.set_output_multiple(self.numsamp)

		# state machine
		self.state = 0
		self.scount=0


		#tone or no tone
		self.tone=[np.complex(1) for j in range(self.numsamp)]
		self.notone=[np.complex(0) for j in range(self.numsamp)]


	#end __init__


	def work(self, input_items, output_items):

		while True:
			if self.state == 0:
				# state 0 -> send cw message

				if self.scount >= self.cwmessagelen:
					# got to state 1 if complete message is send
					self.state=1
					self.scount=0
				else:
					# send character and go to next char
					output_items[0][:self.numsamp]=self.tone if self.cwmessage[self.scount] == "1" else self.notone
					self.scount += 1
					return self.numsamp
				#end else - if

			elif self.state == 1:
				# state 1 -> silence (sleeping)
				if self.scount >= self.numsamp_sleep:
					# got to state 0 if done sleeping
					self.state=0
					self.scount=0
				else:
					# send silence
					output_items[0][:self.numsamp]=self.notone
					self.scount += 1
					return self.numsamp
				#end else - if

			else:
				# unknown state.
				# we should never come here, re-init
				self.state=0
				self.scount=0

			#end state machine

		#end endless loop

	#end work
# end class "morsecode_enc"

