# cryptobot
Slackbot that provides a console for feather duster cryptanalyis tool

# Setup
Modify the slackbot_settings.py.example to use the API of your slack room you want. See Slack documentation on how to generate an API key for that. 

docker build -t cryptobot .

docker run cryptobot

# Usage

* help: Print usage details
* analyze: show details about a ciphertext
* shift: use the alpha_shift (because everyone tries ROT13 right away)
* crack: use the featherduster autopwn mode to try various methods of cracking a ciphertext

For more information about Feather Duster: https://github.com/nccgroup/featherduster/
