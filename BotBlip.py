from asyncio.windows_events import NULL
import telebot
from telebot import types
import datetime
from threading import Thread
from math import radians, cos, sin, asin, sqrt
import smtplib
from ics import Calendar, Event


all_users = {} # usr_id: User
all_events = {} # evn_id: [usr_id, Event]
all_events_on_moderate = [] # [usr_id, evn_id, Event]
free_event_id = 0
Del_Event = None
new_event:Event
bot = telebot.TeleBot('6189215832:AAGBAu2VGDJ3CsNUy1DiV8O_zQXfemvVlbQ');


class Event:
    def __init__(this):
        this.main_photo = NULL;
        this.photos = []
        this.title:str = ""
        this.description:str = "" # многострочное описание + ссылки на ресурсы в тексте + ссылка на видео
        this.start_datetime = []
        this.end_datetime = []
        this.year:int = "нет ограничений"
        this.max_people = "не ограничено"
        this.pay:str = "бесплатно"
        this.pay_web = None
        this.tags = [] # при добавлении новых тегов они добавляются в Tags
        this.location = None
        this.rang:int = 0 # изначально 0, можно повысить или понизить хранит (+ или - и id пользователя)

    def get_string_event(this):
        return f"""{this.title}
Описание: {this.description}
Начало: {this.start_datetime}
Конец: {this.end_datetime}
Возрастное ограничение: {this.year}
Количество мест: {this.max_people}
Оплата: {this.pay}"""

class User:
    def __init__(this, name, status = "Пользователь"):
        this.name:str = name
        this.status:str = status
        this.reputation:int = 0 # репутация организатора
        this.vk_id:int # кнопка привязки/отвязка соцсети
        # подписки
        this.subscription_eventors = []
        this.subscription_tags = []
        this.subscription_place = [] # координаты радиус
        this.subscription_days_week = [] # координаты радиус

        this.remind_a = [] # напоминание за

        this.event_ids = [] # все эвенты организатора 

        this.last_location = None

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        all_users[message.chat.id].last_location = [message.location.latitude, message.location.longitude]
        print(message.location)

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

def seteventtitle(message):
    new_event.title = message.text;
    bot.send_message(message.chat.id, "Успешно")

def seteventdescription(message):
    new_event.description = message.text;
    bot.send_message(message.chat.id, "Успешно")

def seteventmainimg(message):
    if(message.photo):
        print ('message.photo =', message.photo)
        fileID = message.photo[-1].file_id
        print ('fileID =', fileID)
        file_info = bot.get_file(fileID)
        print ('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(f"MainImage{free_event_id}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        new_event.main_photo = f"MainImage{free_event_id}.jpg";
        bot.send_message(message.chat.id, "Успешно")

    elif(message.document):
        print ('message.photo =', message.photo)
        fileID = message.document.file_id
        print ('fileID =', fileID)
        file_info = bot.get_file(fileID)
        print ('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(f"MainImage{free_event_id}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        new_event.main_photo = f"MainImage{free_event_id}.jpg";
        bot.send_message(message.chat.id, "Успешно")

    else:
        bot.send_message(message.chat.id, "Изображение не определено")

def addeventimg(message):
    if(message.photo):
        print ('message.photo =', message.photo)
        fileID = message.photo[-1].file_id
        print ('fileID =', fileID)
        file_info = bot.get_file(fileID)
        print ('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(f"SideImage{free_event_id}{len(new_event.photos)}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        new_event.photos.append(f"SideImage{free_event_id}{len(new_event.photos)}.jpg");
        bot.send_message(message.chat.id, "Успешно")

    elif(message.document):
        print ('message.photo =', message.photo)
        fileID = message.document.file_id
        print ('fileID =', fileID)
        file_info = bot.get_file(fileID)
        print ('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(f"SideImage{free_event_id}{len(new_event.photos)}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        new_event.photos.append(f"SideImage{free_event_id}{len(new_event.photos)}.jpg");
        bot.send_message(message.chat.id, "Успешно")

    else:
        bot.send_message(message.chat.id, "Изображение не определено")

def seteventage(message):
    new_event.year = message.text;
    bot.send_message(message.chat.id, "Успешно")

def seteventpay(message):
    new_event.pay = message.text;
    bot.send_message(message.chat.id, "Успешно")

def seteventplaces(message):
    new_event.max_people = message.text;
    bot.send_message(message.chat.id, "Успешно")

def seteventgeo(message):
    new_event.location = message.text.split();
    bot.send_message(message.chat.id, "Успешно")

def seteventtags(message):
    new_event.tags = message.text.split();
    bot.send_message(message.chat.id, "Успешно")

def seteventstart(message):
    new_event.start_datetime = message.text.split();
    bot.send_message(message.chat.id, "Успешно")

def seteventend(message):
    new_event.end_datetime = message.text.split();
    bot.send_message(message.chat.id, "Успешно")

def seteventpay_web(message):
    print(message)
    new_event.pay_web = message.text;
    print(new_event.pay_web)
    bot.send_message(message.chat.id, "Успешно")

def deleteevent(message):
    print("ok")
    #global Del_Event;
    #del all_events[Del_Event];
    #all_users[message.chat.id].event_ids.remove(Del_Event)

def editeteevent(message):
    print("ok")



@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    match callback.data:
        case "rename":
            bot.send_message(callback.message.chat.id, "Введите новое имя")
            bot.register_next_step_handler(callback.message, rename)

        case "myevents":
            for key in all_users: # usr_id: User
                if(key == callback.message.chat.id):
                    usr = all_users[key];
                    print(len(usr.event_ids))
                    for ev in usr.event_ids:
                        ev = all_events[ev][1];

                        #bot.send_message(key, ev);
                        if(ev.main_photo):
                            img = open(ev.main_photo, 'rb')
                            bot.send_photo(callback.message.chat.id, img)
                             
                        kb2 = types.InlineKeyboardMarkup()
                        if isinstance(ev.pay_web, str):
                            btn1 = types.InlineKeyboardButton("Покупка", url=all_events[ev].pay_web)
                            kb2.add(btn1)
                        if isinstance(ev.location, list):
                            btn2 = types.InlineKeyboardButton("Показать на карте", url= f"https://yandex.ru/maps/?ll={ev.location[1]},{ev.location[0]}&z=17&mode=search&whatshere[point]={ev.location[1]},{ev.location[0]}&whatshere[zoom]=17")
                            kb2.add(btn2)

                        bot.send_message(callback.message.chat.id, ev.get_string_event(), reply_markup=kb2)
                        
                        for i in ev.photos:
                            img = open(i, 'rb')
                            bot.send_photo(callback.message.chat.id, img)
                    break;

        case "crevent":
            global new_event
            new_event = Event()
            kb2 = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Установить название", callback_data="seteventtitle")
            btn2 = types.InlineKeyboardButton("Добавить описание", callback_data="seteventdescription")
            btn3 = types.InlineKeyboardButton("Добавить главное фото", callback_data="seteventmainimg")
            btn4 = types.InlineKeyboardButton("Добавить побочное фото", callback_data="addeventimg")
            btn5 = types.InlineKeyboardButton("Установить возрастное ограничение", callback_data="seteventage")
            btn6 = types.InlineKeyboardButton("Установить цену", callback_data="seteventpay")
            btn61 = types.InlineKeyboardButton("Добавить ссылку на оплату", callback_data="seteventpay_web")
            btn7 = types.InlineKeyboardButton("Установить количество мест", callback_data="seteventplaces")
            btn8 = types.InlineKeyboardButton("Установить геолокацию", callback_data="seteventgeo")
            btn9 = types.InlineKeyboardButton("Установить время начала", callback_data="seteventstart")
            btn10 = types.InlineKeyboardButton("Установить время конца", callback_data="seteventend")
            btn11 = types.InlineKeyboardButton("Установить теги", callback_data="seteventtags")
            btn12 = types.InlineKeyboardButton("Предпросмотр", callback_data="previewevent")
            btn13 = types.InlineKeyboardButton("Отправить на проверку", callback_data="sendtoverefication")
            
            kb2.add(btn1);
            kb2.add(btn2);
            kb2.add(btn3);
            kb2.add(btn4);
            kb2.add(btn5);
            kb2.add(btn6);
            kb2.add(btn61);
            kb2.add(btn7);
            kb2.add(btn8);
            kb2.add(btn9);
            kb2.add(btn10);
            kb2.add(btn11);
            kb2.add(btn12);
            kb2.add(btn13);

            bot.send_message(callback.message.chat.id, "Выберите нужные действия", reply_markup=kb2)

        case "edevent":
            for key in all_users: # usr_id: User
                if(key == callback.message.chat.id):
                    usr = all_users[key];

                    for ev in usr.event_ids:
                        ev = all_events[ev][1];

                        kb2 = types.InlineKeyboardMarkup()
                        btn = types.InlineKeyboardButton("Изменить", callback_data="editeteevent");
                        
                        kb2.add(btn);
                        bot.send_message(callback.message.chat.id, ev.title, reply_markup=kb2)
                        
                    break;

        case "delevent":
            for key in all_users: # usr_id: User
                if(key == callback.message.chat.id):
                    usr = all_users[key];

                    for ev in usr.event_ids:
                        ev = all_events[ev][1];

                        kb2 = types.InlineKeyboardMarkup()
                        btn = types.InlineKeyboardButton("Удалить", callback_data="deleteevent");
                        
                        kb2.add(btn);
                        bot.send_message(callback.message.chat.id, ev.title, reply_markup=kb2)
                        
                    break;

        case "eventsmoderateyes":
            if(len(all_events_on_moderate) > 0):
                usr_id, evn_id, evnt = all_events_on_moderate[0]

                all_events[evn_id] = [usr_id, evnt];
                all_users[usr_id].event_ids.append(evn_id)

                del all_events_on_moderate[0];

                bot.send_message(callback.message.chat.id, "Принято")
                bot.send_message(usr_id, "Ваше мероприятие принято")

        case "eventmoderateno":
            if(len(all_events_on_moderate) > 0):
                usr_id, evn_id, evnt = all_events_on_moderate[0]

                del all_events_on_moderate[0];

                bot.send_message(callback.message.chat.id, "Отклонено")
                bot.send_message(usr_id, "Ваше мероприятие отклонено")

                #all_users[usr_id].event_ids.append(evn_id)

        case "previewevent":
            if(new_event.main_photo):
                img = open(new_event.main_photo, 'rb')
                bot.send_photo(callback.message.chat.id, img)
            
            kb2 = types.InlineKeyboardMarkup()
            if isinstance(new_event.pay_web, str):
                btn1 = types.InlineKeyboardButton("Покупка", url=new_event.pay_web)
                kb2.add(btn1)
            if isinstance(new_event.location, list):
                btn2 = types.InlineKeyboardButton("Показать на карте", url= f"https://yandex.ru/maps/?ll={new_event.location[1]},{new_event.location[0]}&z=17&mode=search&whatshere[point]={new_event.location[1]},{new_event.location[0]}&whatshere[zoom]=17")
                kb2.add(btn2)
            bot.send_message(callback.message.chat.id, new_event.get_string_event(), reply_markup=kb2)
            
            for i in new_event.photos:
                img = open(i, 'rb')
                bot.send_photo(callback.message.chat.id, img)

        case "seteventtitle":
            bot.send_message(callback.message.chat.id, "Введите название")
            bot.register_next_step_handler(callback.message, seteventtitle)

        case "seteventdescription":
            bot.send_message(callback.message.chat.id, "Введите описание")
            bot.register_next_step_handler(callback.message, seteventdescription)

        case "seteventmainimg":
            bot.send_message(callback.message.chat.id, "Отправьте фото (png или jpg)")
            bot.register_next_step_handler(callback.message, seteventmainimg)

        case "addeventimg":
            bot.send_message(callback.message.chat.id, "Отправьте фото (png или jpg)")
            bot.register_next_step_handler(callback.message, addeventimg)
            
        case "seteventage":
            bot.send_message(callback.message.chat.id, "Введите возрастное ограничение (пример: 12+)")
            bot.register_next_step_handler(callback.message, seteventage)

        case "seteventpay":
            bot.send_message(callback.message.chat.id, "Укажите цену (если бесплатно, так и напишите)")
            bot.register_next_step_handler(callback.message, seteventpay)

        case "seteventplaces":
            bot.send_message(callback.message.chat.id, "Укажите максимальное количество мест (или неограниченно)")
            bot.register_next_step_handler(callback.message, seteventplaces)

        case "seteventgeo":
            bot.send_message(callback.message.chat.id, "Укажите геолакацию: долгота и широта, через пробел")
            bot.register_next_step_handler(callback.message, seteventgeo)

        case "seteventtags":
            bot.send_message(callback.message.chat.id, "Перечислите основные направления вашего мероприятия через пробел")
            bot.register_next_step_handler(callback.message, seteventtags)

        case "seteventstart":
            bot.send_message(callback.message.chat.id, "Укажите дату начала и время. пример: 23.04.2004 12.43")
            bot.register_next_step_handler(callback.message, seteventstart)

        case "seteventend":
            bot.send_message(callback.message.chat.id, "Укажите дату окончания и время. пример: 23.04.2004 17.50")
            bot.register_next_step_handler(callback.message, seteventend)

        case "seteventpay_web":
            bot.send_message(callback.message.chat.id, "Введите ссылку на страницу оплаты")
            bot.register_next_step_handler(callback.message, seteventpay_web)

        case "sendtoverefication":
            global free_event_id;
            all_events_on_moderate.append([callback.message.chat.id, free_event_id, new_event]);
            free_event_id+=1;
            new_event = Event()
            bot.send_message(callback.message.chat.id, "Успешно отправлено на проверку")








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

        case "мероприятия на модерацию":
            if(len(all_events_on_moderate) > 0):
                kb2 = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton("Да", callback_data="eventsmoderateyes")
                btn2 = types.InlineKeyboardButton("Нет", callback_data="eventmoderateno")

                kb2.add(btn1, btn2);
         
                bot.send_message(message.chat.id, "Проверить:")
                usr_id, evn_id, evn = all_events_on_moderate[0];
                bot.send_message(message.chat.id, evn.get_string_event(), reply_markup=kb2)

            else:
                bot.send_message(message.chat.id, "Мероприятий на проверку пока нет")




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



