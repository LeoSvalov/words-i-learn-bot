from resources import *
import telebot
import time
from telebot import apihelper

token = "1056573429:AAEZXiBvCqYBHIDmtmN26hDyxWfHAjj7gmU"
ip = '110.49.101.58'
port = '1080'
apihelper.proxy = {
  'https': 'socks5://{}:{}'.format(ip,port)
}
bot = telebot.TeleBot(token)
flag = 0
# start - Beginning of the bot
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hey, *dude*! Let's start learning some english! ", parse_mode='Markdown')

# help - Description of all commands
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'there will be help, believe me' , parse_mode='Markdown')

@bot.message_handler(commands=['wotd'])
def wotd_message(message):
	reply = parse_word_of_the_day()
	bot.send_message(message.chat.id, reply , parse_mode='Markdown')

@bot.message_handler(commands=['definition'])
def definition_message(message):
    bot.send_message(message.chat.id, 'Well, give me the word that you want to get definition for:' , parse_mode='Markdown')
    global flag
    flag = 2

@bot.message_handler(commands=['synonyms'])
def synonyms_message(message):
    bot.send_message(message.chat.id, 'Well, give me the word that you want to get synonyms for:' , parse_mode='Markdown')
    global flag
    flag = 1



@bot.message_handler(content_types=['text'])
def text_message(message):
	global flag
	if flag == 1:
		output = parse_synonyms(message.text)
		flag = 0
		bot.send_message(message.chat.id, output, parse_mode='Markdown')
	elif flag == 2:
		output = parse_word(message.text)
		flag = 0
		bot.send_message(message.chat.id, output, parse_mode='Markdown')
	else:
		if message.text == "Hello" or message.text == "Hi" or message.text == "hi":
			bot.send_message(message.chat.id, 'Well, hello hello, yound lady! How are u doing?', parse_mode='Markdown')
		else: bot.send_message(message.chat.id, "*Sorry buddy, totally didn't get your point! Try to use commands, hope it will help u!*", parse_mode='Markdown')


def main():
	try:
		bot.polling(none_stop=True)

	except Exception as err:
		time.sleep(5)
		print("Internet error!")

if __name__ == '__main__':
	main()