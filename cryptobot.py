from slackbot.bot import respond_to
from slackbot.bot import listen_to
import cryptanalib as ca
import feathermodules
import re
import sys

from feathermodules.stream import *
from feathermodules.block import *
from feathermodules.classical import *
from feathermodules.auxiliary import *
from feathermodules.custom import *
from feathermodules.pubkey import *

feathermodules.samples = []
feathermodules.results = False
feathermodules.selected_attack_name = ''
feathermodules.current_options = {}

@respond_to('help', re.IGNORECASE)
def hi(message):
    message.reply("Hi. I'm a crypto crack bot. Send me ciphertext by using \n'crack <unknown ciphertext>'\n'shift <rot13>'\n'analyze <ciphertext>'")
    # react with thumb up emoji
    message.react('+1')

@respond_to('crack (.*)')
def crack(message, ciphertext):
	message.reply('Cracking in progress...for ciphertext %s' % ciphertext)
	feathermodules.samples += ciphertext.split()
	#feathermodules.samples.append(ciphertext)
	try: 
		autopwn(message, "Test1")
		message.reply("Cracked successful. Pay me for the answer")
	except:
		print("Unexpected error:", sys.exc_info()[0])
		message.reply("This went poorly. What are you even doing right now?")
	feathermodules.samples = []

@respond_to('shift (.*)')
def shift(message, ciphertext):
	message.reply('Cracking in progress...for ciphertext %s' % ciphertext)
	#feathermodules.samples += ciphertext.split()
	try: 
		result = ca.break_alpha_shift(ciphertext)
		message.reply(unicode(result))
		message.reply("Cracked successful. Pay me for the answer")
	except:
		print("Unexpected error:", sys.exc_info()[0])
		message.reply("This went poorly. What are you even doing right now?")
	feathermodules.samples = []

@respond_to('analyze (.*)')
def analyze(message, ciphertext):
	message.reply('Analysis in progress...for ciphertext %s' % ciphertext)
	try: 
		result = ca.analyze_ciphertext(ciphertext)
		#message.reply(unicode(result))
		message.reply(unicode('\n'.join(['%s:: %s' % (key, value) for (key, value) in result.items()])))
	except:
		print("Unexpected error:", sys.exc_info()[0])
		message.reply("This went poorly. What are you even doing right now?")
	feathermodules.samples = []

# autopwn
def autopwn(message, line):
      if len(feathermodules.samples) == 0:
         message.reply('No loaded samples. Please use the \'import\' command.')
         return False
      message.reply('[+] Analyzing samples...')
      message.reply("Ciphertext is %s" % feathermodules.samples)
      analysis_results = ca.analyze_ciphertext(feathermodules.samples, verbose=True)
      if analysis_results['decoded_ciphertexts'] != feathermodules.samples:
         feathermodules.samples = analysis_results['decoded_ciphertexts']
         try:
         	message.reply(analysis_results['decoded_ciphertexts'])
         except:
         	pass
      for attack in feathermodules.module_list.keys():
         if len(set(feathermodules.module_list[attack]['keywords']) & set(analysis_results['keywords'])) > 0:
            message.reply('Running module: %s' % attack)
            try: 
              feathermodules.current_options = feathermodules.module_list[attack]['options']
              results = feathermodules.module_list[attack]['attack_function'](feathermodules.samples)
              message.reply(unicode(results))
            except: 
              print("EXCEPTION: ", sys.exc_info()[0])
              pass