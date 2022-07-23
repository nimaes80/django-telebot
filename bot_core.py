# Initials
from os import environ
from pathlib import Path
from sys import path

import django

BASE_DIR = Path(__file__).resolve().parent

path.append(f'{BASE_DIR}/config/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 
django.setup()

# Imports 
import telebot
from django.contrib.auth import get_user_model
from telebot import apihelper
from telebot.types import Message

# Main Codes


TOKEN = ""

apihelper.proxy = {
	'https': 'socks5h://127.0.0.1:9050',
	# 'http':'http://127.0.0.1:8118',
	# 'https':'https://127.0.0.1:8118'
}

bot = telebot.TeleBot(TOKEN)

User = get_user_model()
USERS = {

}

class UserInstance:
	def __init__(self, username:str, chat_id:int) -> None:
		self._username : str = username
		self._chat_id : int = chat_id
		self._password : str = None

	@property
	def username(self) -> str:
		return self._username

	@property
	def chat_id(self) ->  int:
		return self._chat_id

	@property
	def password(self) -> str:
		return self._password




@bot.message_handler(commands=['start', ])
def start(message:Message):
	bot.send_message(message.chat.id, "Howdy, how are you doing?\nYou can Login to your account and twitte what you want.")


@bot.message_handler(commands=['register', 'signup'])
def register_start(message:Message):
	msg = bot.send_message(message.chat.id, "Ok, Please send me your username:")
	bot.register_next_step_handler(msg, register_username)


def register_username(message:Message):
	CHAT_ID = message.chat.id
	USRENAME = message.text

	user = UserInstance(USRENAME, CHAT_ID)
	USERS[CHAT_ID] = user

	msg = bot.send_message(CHAT_ID, "Almost done, Now send account password:")
	bot.register_next_step_handler(msg, register_password)

def register_password(message:Message):
	CHAT_ID = message.chat.id
	user = USERS[CHAT_ID]
	user._password = message.text
	USERS.pop(CHAT_ID)
	add_user(user)
	msg = bot.send_message(CHAT_ID, "Done. You can now login as your username.")
	# bot.register_next_step_handler(msg, login_start)


def add_user(_user):
	user = User.objects.get_or_create(chat_id=_user.chat_id)[0]
	print(user)
	user.username = _user.username
	user.set_password(_user.password)
	user.save()
	bot.send_message(_user.chat_id, "Your Data saved.")




@bot.message_handler(commands=['login', 'signin'])
def login_start(message:Message):
	bot.send_message(message.chat.id, "Please Send me your username and password")







if __name__ == '__main__':
	print("Start polling...")
	bot.infinity_polling()
	# bot.polling()



