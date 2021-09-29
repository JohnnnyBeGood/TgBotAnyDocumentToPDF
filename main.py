import os
import telebot
from dotenv import load_dotenv
from os.path import join, dirname
import requests
import urllib

# иницилизация бота и токена бота
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
API_TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(API_TOKEN)


# command description used in the "help" command
commands = {  
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands',
    'convert'     : 'Converting a file',
}


# help page
@bot.message_handler(commands=['help'])
def command_help(message):
    chat_id = message.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + " : "
        help_text += commands[key] + "\n"
    bot.send_message(chat_id, help_text)  # send the generated help page

# start page
@bot.message_handler(commands=['start'])
def command_start(message):
    strtMsg = f'''
Hello {message.from_user.first_name} {message.from_user.last_name}
This bot will helps you to do many things with pdf's 🥳
Some of the main features are:
◍ `Convert images to PDF`
◍ `Convert files to pdf`
'''
    bot.send_message(message.chat.id, strtMsg)

# convert page
@bot.message_handler(commands=['convert'])
def command_convert_file(message):
    msg = bot.send_message(message.chat.id, """Пожалуйста отправте файл:""")
    bot.register_next_step_handler(msg, process_filesend_step_1)


def process_filesend_step_1(message):
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    file_name = message.document.file_name
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(
        API_TOKEN, file_info.file_path))
    rezult_file = file_to_convert(file_name)
    file = open(rezult_file, 'rb')
    bot.send_document(message.chat.id, file)
    os.remove(rezult_file)


def file_to_convert(file_name):
    command = 'unoconv -f pdf \'{}\''.format(file_name)
    os.system(command)
    p = os.path.abspath(file_name)
    name = os.path.basename(p)
    file_wo_extension = os.path.splitext(name)[0]
    return file_wo_extension + '.pdf'

# random erroneous text
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    errMsg = f'''к сожалению я не понимаю вашу команду,
    пожалуйста используйте /help
    '''
    bot.send_message(message.from_user.id, errMsg)


if __name__ == '__main__':

    # Enable saving next step handlers to file "./.handlers-saves/step.save".
    # Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
    # saving will hapen after delay 2 seconds.
    bot.enable_save_next_step_handlers(delay=2)

    # Load next_step_handlers from save file (default "./.handlers-saves/step.save")
    # WARNING It will work only if enable_save_next_step_handlers was called!
    bot.load_next_step_handlers()
    bot.polling(non_stop=True)