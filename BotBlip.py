import telebot
from telebot import types
import datetime
from threading import Thread
from math import radians, cos, sin, asin, sqrt
import smtplib
from ics import Calendar, Event


class Event:
    def __init__(this):
        this.title:str
        this.description:str # многострочное описание + ссылки на ресурсы в тексте + ссылка на видео
        this.photos = []
        this.rang:int # изначально 0, можно повысить или понизить хранит (+ или - и id пользователя)
        this.tags = [] # при добавлении новых тегов они добавляются в Tags
        this.pay:int
        this.year:int
        this.max_people

    def get_string_event(this):
        return f"""{this.title}
{this.description}
Возрастное ограничение - {this.year} лет
Мест - {this.max_people}
Оплата: {this.pay}"""



class User:
    def __init__(this, name, status = "Пользователь"):
        this.name:str = name
        this.vk_id:int
        this.status:str = status
        this.reputation:int = 0 # репутация организатора
        this.last_location = None
        # подписки
        this.subscription_eventors = []
        this.subscription_tags = []
        this.subscription_place = [] # координаты радиус
        this.subscription_days_week = [] # координаты радиус

        this.remind_a = [] # напоминание за




all_users = {}
all_events = []
bot = telebot.TeleBot('6189215832:AAGBAu2VGDJ3CsNUy1DiV8O_zQXfemvVlbQ');





@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        all_users[message.chat.id].last_location = [message.location.latitude, message.location.longitude]





def profil(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    user = all_users[message.chat.id];
    if(user.status == "Пользователь"):
        kb.add("Стать организатором")
    elif(user.status == "Организатор"):
        kb.add("Стать модератором")

    kb.add("На главную")

    name = user.name
    status = user.status

    about_user = f"Имя: {name}\nСтатус: {status}"

    kb2 = types.InlineKeyboardMarkup();
    btn1 = types.InlineKeyboardButton("изменить имя", callback_data="rename")
    kb2.add(btn1);

    bot.send_message(message.chat.id, "Профиль:", reply_markup=kb)
    bot.send_message(message.chat.id, about_user, reply_markup=kb2)







def rename(message):
    all_users[message.chat.id].name = message.text
    bot.send_message(message.chat.id, "Имя успешно изменено")
    profil(message)







@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == "rename":
        bot.send_message(callback.message.chat.id, "Введите новое имя")
        bot.register_next_step_handler(callback.message, rename)







@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = message.text.lower()
    if((text == "/start") or (text == "на главную")):
        if(text == "/start" and (message.chat.id not in all_users)):
            all_users[message.chat.id] = User(message.from_user.first_name)
            bot.send_message(message.chat.id, f"Приветствую новичка {all_users[message.chat.id].name}")

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kb.add("Профиль")
        kb.add("Пользователь", "Организатор", "Модератор")
        bot.send_message(message.chat.id, "Выберите роль", reply_markup=kb)
        
    match message.text.lower():

        case "пользователь":
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            kb.add("Сегодня", "Завтра", "На этой недели")
            kb.add("Поиск по тегам", "Поиск по дням")
            kb.add("Поиск по радиусу")
            kb.add("На главную")
         
            bot.send_message(message.chat.id, "Выберите нужное действие", reply_markup=kb)

        case "организатор":
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kb2 = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Мои мероприятия", callback_data="myevents")
            btn2 = types.InlineKeyboardButton("Создать мероприятие", callback_data="crevent")
            btn3 = types.InlineKeyboardButton("Редактировать мероприятие", callback_data="edevent")
            btn4 = types.InlineKeyboardButton("Удалить мероприятие", callback_data="delevent")
            
            kb.add("На главную")
            kb2.add(btn1);
            kb2.add(btn2);
            kb2.add(btn3, btn4);

         
            bot.send_message(message.chat.id, "Организатор:", reply_markup=kb2)
            bot.send_message(message.chat.id, "Действия:", reply_markup=kb)

        case "модератор":
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            kb.add("Мероприятия на модерацию")
            kb.add("На главную")
         
            bot.send_message(message.chat.id, "Выберите нужное действие", reply_markup=kb)

        case "профиль":
            profil(message)

        case "стать организатором":
            user = all_users[message.chat.id];
            user.status = "Организатор"
            bot.send_message(message.chat.id, "Теперь вы организатор")
            profil(message)

        case "стать модератором":
            user = all_users[message.chat.id];
            user.status = "Модератор"
            bot.send_message(message.chat.id, "Теперь вы модератор")
            profil(message)

        case "поиск по радиусу":
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn = types.KeyboardButton("Определить местоположение", request_location=True)
            kb.add(btn)
            if isinstance(all_users[message.chat.id].last_location, list):
                kb.add("500 метров", "1 километр", "3 километра", "5 километров")
            kb.add("На главную")

            bot.send_message(message.chat.id, "Выберите радиус поиска", reply_markup=kb)
            
        case "500 метров":
            bot.send_message(message.chat.id, all_users[message.chat.id].last_location[1])


        case "создать мероприятие":
            ...

        case "мои мероприятия":
            ...

        case "редактировать мероприятие":
            ...

        case "удалить мероприятие":
            ...



def main():
    ...
    #while True:
    #    ...


def distance(my_location, event_location):
    lo1 = radians(my_location[0])
    la1 = radians(my_location[1])

    lo2 = radians(event_location[0])
    la2 = radians(event_location[1])

    D_Lo = lo2 - lo1
    D_La = la2 - la1

    P = sin(D_La / 2)**2 + cos(la1) * cos(la2) * sin(D_Lo / 2)**2
    Q = 2 * asin(sqrt(P))
    R_km = 6378.8
    return(Q * R_km)

# botblip@mail.ru
# пароль OaRVGrry1y3$

#Thread(target = main).start();
bot.polling()
# bot.register_next_step_handler(message, func)


# ToDo

# сегодня завтра на этой неделе и т.д.
# опред. местополож. и поиск в радиусе 5 км
# возможность купить билеты
# напоминание. ссылка в личный календарь или напоминание в боте

# местоположение, дата, время, цена, ссылка на оплату, возрастные ограничения
# редактирование и удаление своих мероприятий

# модерация
























UserStatus = ("user", "eventor", "admin"); # пользователь организатор админ
Remind = ("Week", "3 days", "2 days", "day", "half day", "3 hours", "2 hours", "hour", "half hour"); # напоминание за __
Tags = []; # динамические теги
"https://yandex.ru/maps/?ll=37.618423,55.751244&z=17&mode=search&whatshere[point]=37.618423,55.751244&whatshere[zoom]=17"

class Calendar:
    def __init__(this):
        this.dated_events = [] # [datatime, Event]
        # сортировка по времени, рейтингу евента, репутации организатора
        # показывать только мои теги 
    def get_events_in_day(day):
        ...
    def get_events_in_tags(tags):
        ...
    def get_events_in_eventors(eventor):
        ...
    def update():
        ...



