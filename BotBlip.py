# pip
# Pillow
# pytelegrambotapi

import telebot;
import calendar
import json

bot = telebot.TeleBot('6189215832:AAGBAu2VGDJ3CsNUy1DiV8O_zQXfemvVlbQ');

def func(message):
    bot.send_message(message.from_user.id, "googbye")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "hello":
        bot.send_message(message.from_user.id, """Are you wellcome!
  This is you videos:
https://www.youtube.com/watch?v=rGkvMwTi3b4""", disable_web_page_preview=True)
        bot.register_next_step_handler(message, func)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "write me")
    else:
        bot.send_message(message.from_user.id, "/help.")


bot.polling(none_stop=True, interval=0)



# ����� �������� ��������� ������������ ����������� ����� bot.register_next_step_handler(message, func) ������� �� ����� ������������ ������� ������� fun�.


UserStatus = ("user", "eventor", "admin"); # ������������ ����������� �����
Tags = []; # ������������ ����
"https://yandex.ru/maps/?ll=37.618423,55.751244&z=17&mode=search&whatshere[point]=37.618423,55.751244&whatshere[zoom]=17"

class User:
    def __init__(this):
        this.name:str
        this.id:int
        this.status:str # UserStatus

class Event:
    def __init__(this):
        this.title:str
        this.description:str # ������������� �������� + ������ �� ������� � ������ + ������ �� �����
        this.photos = []
        # ����
        this.reputation:int # ���������� 0, ����� �������� ��� �������� ������ (+ ��� - � id ������������)
        this.tags = [] # ��� ���������� ����� ����� ��� ����������� � Tags
        this.pay:int
        this.year:int
