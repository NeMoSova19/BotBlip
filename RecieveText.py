import telegram_bot_calendar as TGcalendar
import RecieveCommands

from Settings import *
from Event import Event
from Functions import *
from User import User

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    User_ID = message.chat.id;
    text = message.text.lower()

    if(User_ID not in all_users):
        all_users[User_ID] = User(message.from_user.first_name, User_ID)
        all_users[User_ID].SendNotDeletableMsg(f"Приветствую, {all_users[User_ID].name}!")
        
    if text == "/start":
        bot.delete_message(User_ID, message.message_id) # удаление пользовательской команды
        ReCallback(User_ID, "main_menu", "main_menu");

    else:
        bot.delete_message(User_ID, message.message_id) # удаление пользовательской команды