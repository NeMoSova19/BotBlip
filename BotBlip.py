﻿import telebot
from telebot import types
import datetime
import time
import validators
from threading import Thread
from math import radians, cos, sin, asin, sqrt


all_users = {} # usr_id: User
all_events = {} # evn_id: [usr_id, Event]
all_events_on_moderate = [] # [usr_id, evn_id, Event]
all_tags = [] # str Tags
free_event_id = 0
day_of_week = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среду",
    4: "Четверг",
    5: "Пятницу",
    6: "Субботу",
    7: "Воскресенье"}
day_of_week_norm = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье"}
bot = telebot.TeleBot('6189215832:AAGBAu2VGDJ3CsNUy1DiV8O_zQXfemvVlbQ');



class Event:
    def __init__(this, _id):
        this.main_photo = None;
        this.photos = []
        this.title:str = None
        this.description:str = None # многострочное описание + ссылки на ресурсы в тексте + ссылка на видео
        this.start_datetime:datetime = None
        this.end_datetime:datetime = None
        this.year:int = "нет ограничений"
        this.max_people = "не ограничено"
        this.pay:str = "бесплатно"
        this.pay_web = None
        this.tags = [] # при добавлении новых тегов они добавляются в Tags
        this.location = None
        this.rang:int = 0 # изначально 0, можно повысить или понизить хранит (+ или - и id пользователя)
        this.id = _id;

    def set_data_start(this, dt:str):
        try:
            this.start_datetime = datetime.datetime.strptime(dt, "%d.%m.%Y %H:%M")
            return True;
        except:
            return False;

    def set_data_end(this, dt:str):
        try:
            this.end_datetime = datetime.datetime.strptime(dt, "%d.%m.%Y %H:%M")
            return True;
        except:
            return False;

    def get_string_event(this):
        desc = "нету" if this.description==None else this.description; 
        end = "не указан" if this.end_datetime==None else this.end_datetime; 
        year = "нету" if (this.year in (None, "нет", "")) else this.year; 
        mpeop = "неограниченно" if (this.max_people in (None, "")) else this.max_people; 
        pay = "бесплатно" if (this.max_people in (None, "", "нет", "нету")) else this.max_people; 

        return f"""🌏{this.title}🌏
🗒Описание: {desc}
🕑Начало: {this.start_datetime}
🕔Конец: {end}
🙅‍Возрастное ограничение: {year}
🪑Количество мест: {mpeop}
💸Оплата: {pay}
Оценка: {this.rang} 👍👎"""



class User:
    def __init__(this, name, status = "Пользователь"):
        this.name:str = name
        this.status:str = status
        this.reputation:int = 0 # репутация организатора
        this.vk_id = None # кнопка привязки/отвязка соцсети
        # подписки
        this.subscription_tags = []      # теги
        this.subscription_days_week = [] # дни недели
        this.reminder = {} # {Event_id: [время во сколько будет напоминание:datatime]}
        # для поиска
        this.searchtags = []
        # другое
        this.event_ids = [] # все эвенты организатора 
        this.pre_event = None # 
        this.last_location = None
        this.bot_msg_id = None




def distance(my_location, event_location):
    lo1 = radians(my_location[0])
    la1 = radians(my_location[1])

    lo2 = radians(float(event_location[0]))
    la2 = radians(float(event_location[1]))

    D_Lo = lo2 - lo1
    D_La = la2 - la1

    P = sin(D_La / 2)**2 + cos(la1) * cos(la2) * sin(D_Lo / 2)**2
    Q = 2 * asin(sqrt(P))
    R_km = 6371
    return(Q * R_km)

def send_events(arr:list, id_):

    for i in arr:
        img = None
        if(i.main_photo):
            img = open(i.main_photo, 'rb')
            
        kb2 = types.InlineKeyboardMarkup()
        if isinstance(i.pay_web, str):
            btn1 = types.InlineKeyboardButton("Покупка", url=i.pay_web)
            kb2.add(btn1)
        if isinstance(i.location, list):
            btn2 = types.InlineKeyboardButton("Показать на карте", url= f"https://yandex.ru/maps/?ll={i.location[1]},{i.location[0]}&z=17&mode=search&whatshere[point]={i.location[1]},{i.location[0]}&whatshere[zoom]=17")
            kb2.add(btn2) 

        kb2.add(types.InlineKeyboardButton("Напомнить", callback_data=f"reminder {i.id}"))
            
        if(img):
            msg = bot.send_photo(id_, img, i.get_string_event(), reply_markup=kb2);
        else:
            msg = bot.send_message(id_, i.get_string_event(), reply_markup=kb2)

        list_img = []
        for i in i.photos:
            list_img.append(open(i, 'rb'))
        
        if len(list_img) != 0:
            bot.send_media_group(id_, media=[types.InputMediaPhoto(i) for i in list_img]);
            
def location(message):
    if message.location is not None:
        all_users[message.chat.id].last_location = [message.location.latitude, message.location.longitude]
       
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        kb.add("Местоположение уже определено")
        kb.add("500 метров", "1 километр", "3 километра", "5 километров")
        kb.add("На главную")

        bot.send_message(message.chat.id, "Выберите радиус поиска", reply_markup=kb)

def rename(message):
    all_users[message.chat.id].name = message.text
    bot.send_message(message.chat.id, "Имя установлено")
    check_callback_data(types.CallbackQuery(message.chat.id,message=message, from_user=None, data = "profile 1", chat_instance=None, json_string=None))

def seteventtitle(message):
    all_users[message.chat.id].pre_event.title = message.text;
    bot.send_message(message.chat.id, "Название установлено")

def seteventdescription(message):
    all_users[message.chat.id].pre_event.description = message.text;
    bot.send_message(message.chat.id, "Описание установлено")

def seteventmainimg(message):
    fileID = None;

    if(message.photo):
        fileID = message.photo[-1].file_id
    elif(message.document):
        fileID = message.document.file_id

    if(message.photo or message.document):

        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        path = f"Imgs/MainImage{free_event_id}.jpg"

        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        all_users[message.chat.id].pre_event.main_photo = path;
        bot.send_message(message.chat.id, "Изображение установлено")

    else:
        bot.send_message(message.chat.id, "Изображение не определено")

def addeventimg(message):
    fileID = None;

    if(message.photo):
        fileID = message.photo[-1].file_id
    elif(message.document):
        fileID = message.document.file_id

    if(message.photo or message.document):

        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        path = f"Imgs/SideImage{free_event_id}{len(all_users[message.chat.id].pre_event.photos)}.jpg";

        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        all_users[message.chat.id].pre_event.photos.append(path);
        bot.send_message(message.chat.id, "Изображение добавлено")

    else:
        bot.send_message(message.chat.id, "Изображение не определено")

def seteventage(message):
    all_users[message.chat.id].pre_event.year = message.text;
    bot.send_message(message.chat.id, "Возрастное ограничение установлено")

def seteventpay(message):
    all_users[message.chat.id].pre_event.pay = message.text;
    bot.send_message(message.chat.id, "Цена установлена")

def seteventplaces(message):
    all_users[message.chat.id].pre_event.max_people = message.text;
    bot.send_message(message.chat.id, "Количество мест установлено")

def seteventgeo(message):
    list_geo = message.text.split();
    if isinstance(list_geo, list) and (len(list_geo) == 2):
        try:
            [float(i) for i in list_geo]
            all_users[message.chat.id].pre_event.location = list_geo;
            bot.send_message(message.chat.id, "Местоположение установлено")
            return;
        except:
            ...
    bot.send_message(message.chat.id, "Неправильный формат")

def seteventtags(message):
    all_users[message.chat.id].pre_event.tags = message.text.split();

    for i in all_users[message.chat.id].pre_event.tags:
        if(i not in all_tags):
            all_tags.append(i)

    bot.send_message(message.chat.id, "Теги добавлены")

def seteventstart(message):
    if(all_users[message.chat.id].pre_event.set_data_start(message.text)):
        bot.send_message(message.chat.id, "Время начала установлено")
        return;
    bot.send_message(message.chat.id, "Некорректный ввод")

def seteventend(message):
    if(all_users[message.chat.id].pre_event.set_data_end(message.text)):
        bot.send_message(message.chat.id, "Время окончания установлено")
        return;
    bot.send_message(message.chat.id, "Некорректный ввод")

def seteventpay_web(message):
    url = message.text;
    if validators.url(url):
        all_users[message.chat.id].pre_event.pay_web = url;
        bot.send_message(message.chat.id, "Ссылка на оплату установлена")
        return;
    bot.send_message(message.chat.id, "Некорректный адрес")



@bot.callback_query_handler(func=lambda callback: True)
def check_callback_data(callback):
    global free_event_id;
    usr_id = callback.message.chat.id;

    commands = callback.data.split()
    try:
        bot.clear_step_handler(callback.message)
    except:
        ...
    match commands[0]:
    
        case "main_menu":
            if all_users[usr_id].bot_msg_id: # удаление предыдущего сообщения бота
                bot.delete_message(usr_id, all_users[usr_id].bot_msg_id.message_id)
                all_users[usr_id].bot_msg_id = None
            
            kb = types.InlineKeyboardMarkup();
            kb.add(types.InlineKeyboardButton("Профиль", callback_data="profile 0"))
            kb.add(types.InlineKeyboardButton("Пользователь", callback_data="user"))
            if all_users[usr_id].status != "Пользователь":
                kb.add(types.InlineKeyboardButton("Организатор", callback_data="eventor"))
            if all_users[usr_id].status == "Модератор":
                kb.add(types.InlineKeyboardButton("Модератор", callback_data="moderator"))

            all_users[usr_id].bot_msg_id = bot.send_message(usr_id, "Главное меню", reply_markup=kb)


        case "profile":
            kb = types.InlineKeyboardMarkup();
            user = all_users[usr_id];
            name = user.name
            status = user.status

            about_user = f"Имя: {name}\nСтатус: {status}\n"
            if status == "Организатор":
                about_user += f"Репутация: {user.reputation}\n"

            d = "нет данных" if (user.vk_id == None) else user.vk_id
            about_user += f"Аккаунт VK: {d}\nПодписки:\nСкоро..."

            btn1 = types.InlineKeyboardButton("изменить имя", callback_data="rename")
            kb.add(btn1);
            if(user.status == "Пользователь"):
                kb.add(types.InlineKeyboardButton("стать организатором", callback_data="upgrade_eventor"))
            elif(user.status == "Организатор"):
                kb.add(types.InlineKeyboardButton("стать модератором", callback_data="upgrade_moder"))
            kb.add(types.InlineKeyboardButton("на главную", callback_data="main_menu"))

            if int(commands[1]) == 1: # new
                if all_users[usr_id].bot_msg_id:
                    bot.delete_message(usr_id, all_users[usr_id].bot_msg_id.message_id)
            elif all_users[usr_id].bot_msg_id: # replace
                bot.edit_message_text(chat_id = usr_id, message_id = all_users[usr_id].bot_msg_id.id, text=f"Профиль\n{about_user}")
                bot.edit_message_reply_markup(chat_id = usr_id, message_id = all_users[usr_id].bot_msg_id.id, reply_markup=kb)
                return;
                
            all_users[usr_id].bot_msg_id = bot.send_message(usr_id, f"Профиль\n{about_user}", reply_markup=kb)

        case "user":
            kb = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Сегодня", callback_data="now")
            btn2 = types.InlineKeyboardButton("Завтра", callback_data="tomorrow")
            btn3 = types.InlineKeyboardButton("На этой неделе", callback_data="onweek")
            btn4 = types.InlineKeyboardButton("Поиск по тегам", callback_data="find_for_tags")
            btn5 = types.InlineKeyboardButton("Поиск по дням", callback_data="find_for_days")
            btn6 = types.InlineKeyboardButton("Поиск по радиусу", callback_data="find_for_radius")
            btn7 = types.InlineKeyboardButton("На главную", callback_data="main_menu")

            kb.add(btn1, btn2, btn3)
            kb.add(btn4, btn5)
            kb.add(btn6)
            kb.add(btn7)
         
            bot.edit_message_text(chat_id = usr_id, message_id = all_users[usr_id].bot_msg_id.id, text="Выберите нужное действие")
            bot.edit_message_reply_markup(chat_id = usr_id, message_id = all_users[usr_id].bot_msg_id.id, reply_markup=kb)

        case "eventor":
            kb = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Мои мероприятия", callback_data="myevents")
            btn2 = types.InlineKeyboardButton("Создать", callback_data="crevent")
            btn3 = types.InlineKeyboardButton("Редактировать", callback_data="edevent")
            btn4 = types.InlineKeyboardButton("Удалить", callback_data="delevent")
            btn5 = types.InlineKeyboardButton("На главную", callback_data="main_menu")
            
            kb.add(btn1);
            kb.add(btn2);
            kb.add(btn3, btn4);
            kb.add(btn5)
         
            bot.edit_message_text(chat_id = usr_id, message_id = all_users[usr_id].bot_msg_id.message_id, text = 'Выберите действие')
            bot.edit_message_reply_markup(usr_id, all_users[usr_id].bot_msg_id.message_id, reply_markup=kb)

        case "moderator":
            kb = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Мероприятия на модерацию", callback_data="myevents")
            btn2 = types.InlineKeyboardButton("На главную", callback_data="main_menu")
            kb.add(btn1)
            kb.add(btn2)
         
            bot.edit_message_text(chat_id = usr_id, message_id = all_users[usr_id].bot_msg_id.message_id, text = 'Выберите действие')
            bot.edit_message_reply_markup(usr_id, all_users[usr_id].bot_msg_id.message_id, reply_markup=kb)


        case "rename":
            bot.send_message(callback.message.chat.id, "Введите новое имя")
            bot.register_next_step_handler(callback.message, rename)

        case "upgrade_eventor":
            user = all_users[usr_id];
            user.status = "Организатор"
            bot.send_message(usr_id, "Теперь вы организатор")

            if all_users[usr_id].bot_msg_id: # удаление предыдущего сообщения бота
                bot.delete_message(usr_id, all_users[usr_id].bot_msg_id.message_id)
                all_users[usr_id].bot_msg_id = None

            callback.data = "profile 1"
            check_callback_data(callback)

        case "upgrade_moder":
            user = all_users[usr_id];
            user.status = "Модератор"
            bot.send_message(usr_id, "Теперь вы модератор")

            if all_users[usr_id].bot_msg_id: # удаление предыдущего сообщения бота
                bot.delete_message(usr_id, all_users[usr_id].bot_msg_id.message_id)
                all_users[usr_id].bot_msg_id = None

            callback.data = "profile 1"
            check_callback_data(callback)


        case "now":
            now = datetime.datetime.now()
            arr = []
            for i in all_events:
                evn = all_events[i][1]
                if(evn.start_datetime.day == now.day and evn.start_datetime.time() > now.time()):
                    arr.append(evn);
            if len(arr) == 0:
                bot.send_message(usr_id, "На сегодня мероприятий не найдено")
                
            else:
                arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)
                bot.send_message(usr_id, "Вот мероприятия на сегодня:")
                
                send_events(arr, usr_id)

        case "tomorrow":
            now = datetime.datetime.now()
            arr = []
            for i in all_events:
                evn = all_events[i][1]
                if((evn.start_datetime.day - 1) == now.day):
                    arr.append(evn);
            if len(arr) == 0:
                bot.send_message(usr_id, "На завтра мероприятий не найдено")
                
            else:
                arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)
                bot.send_message(usr_id, "Вот мероприятия на завтра:")
                
                send_events(arr, usr_id)

        case "onweek":
            now = datetime.datetime.now()
            now_week = now.isocalendar()[1]

            arr = []
            for i in all_events:
                evn = all_events[i][1]
                if(evn.start_datetime > now and now_week == evn.start_datetime.isocalendar()[1]):
                    arr.append(evn);
            if len(arr) == 0:
                bot.send_message(usr_id, "На этой недели мероприятий не найдено")
                
            else:
                arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)
        
                bot.send_message(usr_id, "Вот мероприятия на этой недели:")

                send_events(arr, usr_id)

        case "find_for_tags":
            if len(all_tags) == 0:
                bot.send_message(usr_id, "Тегов пока нет, так как организаторы не создали не одного мероприятия");
                return;

            all_users[usr_id].searchtags = [];
            kb2 = types.InlineKeyboardMarkup(row_width=2)

            for i in all_tags:
                kb2.add(types.InlineKeyboardButton(i, callback_data=f"addtagtousersearch {i}"))

            kb2.add(types.InlineKeyboardButton("Поиск", callback_data=f"searchfortags"))
            bot.send_message(usr_id, "Теги:", reply_markup=kb2);

        case "find_for_days":
            kb = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Понедельник", callback_data=f"findweekday {1}")
            btn2 = types.InlineKeyboardButton("Вторник",     callback_data=f"findweekday {2}")
            btn3 = types.InlineKeyboardButton("Среда",       callback_data=f"findweekday {3}")
            btn4 = types.InlineKeyboardButton("Четверг",     callback_data=f"findweekday {4}")
            btn5 = types.InlineKeyboardButton("Пятница",     callback_data=f"findweekday {5}")
            btn6 = types.InlineKeyboardButton("Суббота",     callback_data=f"findweekday {6}")
            btn7 = types.InlineKeyboardButton("Воскресенье", callback_data=f"findweekday {7}")
            btn8 = types.InlineKeyboardButton("Назад", callback_data="user")
            btn9 = types.InlineKeyboardButton("На главную", callback_data="main_menu")
            kb.add(btn1)
            kb.add(btn2)
            kb.add(btn3)
            kb.add(btn4)
            kb.add(btn5)
            kb.add(btn6)
            kb.add(btn7)
            kb.add(btn8, btn9)

            text = "Выберите день недели"
            if all_users[usr_id].bot_msg_id: # replace
                bot.edit_message_text(chat_id = usr_id, message_id = all_users[usr_id].bot_msg_id.id, text=text)
                bot.edit_message_reply_markup(chat_id = usr_id, message_id = all_users[usr_id].bot_msg_id.id, reply_markup=kb)
                return;
                
            all_users[usr_id].bot_msg_id = bot.send_message(usr_id, text, reply_markup=kb)

        case "find_for_radius":
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton("Определить местоположение", request_location=True)
            kb.add(btn)
            if isinstance(all_users[usr_id].last_location, list):
                kb.add("500 метров", "1 километр", "3 километра", "5 километров")
            kb.add("На главную")

            bot.send_message(usr_id, "Выберите радиус поиска", reply_markup=kb)
  

        case "myevents":
            usr = all_users[callback.message.chat.id]
            if len(usr.event_ids) == 0:
                bot.send_message(callback.message.chat.id, "Пусто")
                return;

            send_events([all_events[i][1] for i in usr.event_ids], callback.message.chat.id);
                    
        case "crevent":
            all_users[callback.message.chat.id].pre_event = Event(free_event_id)
            kb2 = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Название", callback_data="seteventtitle")
            btn2 = types.InlineKeyboardButton("Описание", callback_data="seteventdescription")
            btn3 = types.InlineKeyboardButton("Основное фото", callback_data="seteventmainimg")
            btn4 = types.InlineKeyboardButton("Доп фото", callback_data="addeventimg")
            btn5 = types.InlineKeyboardButton("Возрастное ограничение", callback_data="seteventage")
            btn6 = types.InlineKeyboardButton("Цена билета", callback_data="seteventpay")
            btn61 =types.InlineKeyboardButton("Ссылка на оплату", callback_data="seteventpay_web")
            btn7 = types.InlineKeyboardButton("Количество мест", callback_data="seteventplaces")
            btn8 = types.InlineKeyboardButton("Местоположение", callback_data="seteventgeo")
            btn9 = types.InlineKeyboardButton("Время начала", callback_data="seteventstart")
            btn10 =types.InlineKeyboardButton("Время конца", callback_data="seteventend")
            btn11 =types.InlineKeyboardButton("Теги", callback_data="seteventtags")
            btn12 =types.InlineKeyboardButton("Предпросмотр", callback_data="previewevent")
            btn13 =types.InlineKeyboardButton("Опубликовать", callback_data="sendtoverefication")
            
            kb2.add(btn1, btn2);
            kb2.add(btn3, btn4);
            kb2.add(btn5);
            kb2.add(btn6, btn61);
            kb2.add(btn7, btn8);
            kb2.add(btn9, btn10);
            kb2.add(btn11);
            kb2.add(btn12, btn13);

            #bot.send_message(callback.message.chat.id, "Выберите нужные действия (Название, Местоположение и Дата начала - обязательны)", reply_markup=kb2)
            bot.edit_message_text(chat_id=usr_id, message_id=all_users[usr_id].bot_msg_id.message_id, text="Выберите нужные действия (Название, Местоположение и Дата начала - обязательны)")
            bot.edit_message_reply_markup(usr_id, all_users[usr_id].bot_msg_id.message_id, reply_markup=kb2);

        case "edevent":
            usr = all_users[callback.message.chat.id]
           
            for ev_id in usr.event_ids:
                ev = all_events[ev_id][1];
            
                kb2 = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton("Изменить", callback_data=f"editevent {ev_id}");
                kb2.add(btn);
                bot.send_message(callback.message.chat.id, ev.title, reply_markup=kb2)
                
            else:
                bot.send_message(callback.message.chat.id, "Пусто")

        case "delevent":
            usr = all_users[callback.message.chat.id]
            
            for ev_id in usr.event_ids:
                ev = all_events[ev_id][1];

                kb2 = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton("Удалить", callback_data=f"deleteevent {ev_id}");
                
                kb2.add(btn);
                bot.send_message(callback.message.chat.id, ev.title, reply_markup=kb2)

            else:
                bot.send_message(callback.message.chat.id, "Пусто")

        case "editevent":
            all_users[callback.message.chat.id].pre_event = all_events[int(commands[1])][1]

            kb2 = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Название", callback_data="seteventtitle")
            btn2 = types.InlineKeyboardButton("Описание", callback_data="seteventdescription")
            btn3 = types.InlineKeyboardButton("Основное фото", callback_data="seteventmainimg")
            btn4 = types.InlineKeyboardButton("Доп фото", callback_data="addeventimg")
            btn5 = types.InlineKeyboardButton("Возрастное ограничение", callback_data="seteventage")
            btn6 = types.InlineKeyboardButton("Цена билета", callback_data="seteventpay")
            btn61 =types.InlineKeyboardButton("Ссылка на оплату", callback_data="seteventpay_web")
            btn7 = types.InlineKeyboardButton("Количество мест", callback_data="seteventplaces")
            btn8 = types.InlineKeyboardButton("Местоположение", callback_data="seteventgeo")
            btn9 = types.InlineKeyboardButton("Время начала", callback_data="seteventstart")   #######################
            btn10 =types.InlineKeyboardButton("Время конца", callback_data="seteventend")
            btn11 =types.InlineKeyboardButton("Теги", callback_data="seteventtags")
            btn12 =types.InlineKeyboardButton("Предпросмотр", callback_data="previewevent")
            btn13 =types.InlineKeyboardButton("Опубликовать", callback_data=f"sendtoverefication2 {commands[1]}")
            
            kb2.add(btn1, btn2);
            kb2.add(btn3, btn4);
            kb2.add(btn5);
            kb2.add(btn6, btn61);
            kb2.add(btn7, btn8);
            kb2.add(btn9, btn10);
            kb2.add(btn11);
            kb2.add(btn12, btn13);

            bot.send_message(callback.message.chat.id, "Выберите нужные действия", reply_markup=kb2)

        case "deleteevent":
            usr_id = callback.message.chat.id;
            all_users[usr_id].event_ids.remove(int(commands[1]))
            del all_events[int(commands[1])]
            bot.send_message(usr_id, "Удалено")


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


        case "previewevent":
            send_events([all_users[callback.message.chat.id].pre_event], callback.message.chat.id)
           
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
            bot.send_message(callback.message.chat.id, "Укажите дату начала и время. \nпример: 23.04.2004 12:43")
            bot.register_next_step_handler(callback.message, seteventstart)

        case "seteventend":
            bot.send_message(callback.message.chat.id, "Укажите дату окончания и время. \nпример: 23.04.2004 17:50")
            bot.register_next_step_handler(callback.message, seteventend)

        case "seteventpay_web":
            bot.send_message(callback.message.chat.id, "Введите ссылку на страницу оплаты")
            bot.register_next_step_handler(callback.message, seteventpay_web)

        case "sendtoverefication":
            if(all_users[callback.message.chat.id].pre_event.title and all_users[callback.message.chat.id].pre_event.start_datetime and all_users[callback.message.chat.id].pre_event.location):
                
                all_events_on_moderate.append([callback.message.chat.id, free_event_id, all_users[callback.message.chat.id].pre_event]);
                free_event_id+=1;
                #all_users[callback.message.chat.id].pre_event = Event()
                bot.send_message(callback.message.chat.id, "Успешно отправлено на проверку")

                kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
                kb2 = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton("Мои мероприятия", callback_data="myevents")
                btn2 = types.InlineKeyboardButton("Создать", callback_data="crevent")
                btn3 = types.InlineKeyboardButton("Редактировать", callback_data="edevent")
                btn4 = types.InlineKeyboardButton("Удалить", callback_data="delevent")
                
                kb.add("На главную")
                kb2.add(btn1);
                kb2.add(btn2);
                kb2.add(btn3, btn4);

                bot.send_message(callback.message.chat.id, "Выберите действие", reply_markup=kb2)
                bot.send_message(callback.message.chat.id, "Действия:", reply_markup=kb)

            else:
                bot.send_message(callback.message.chat.id, "Какие-то из обязательных параметров не указаны")

        case "sendtoverefication2":
            if(all_users[callback.message.chat.id].pre_event.title and all_users[callback.message.chat.id].pre_event.start_datetime and all_users[callback.message.chat.id].pre_event.location):
                usr_id = callback.message.chat.id;
                all_users[usr_id].event_ids.remove(int(commands[1]))
                del all_events[int(commands[1])]
                
                all_events_on_moderate.append([callback.message.chat.id, free_event_id, all_users[callback.message.chat.id].pre_event]);
                free_event_id+=1;
                #all_users[callback.message.chat.id].pre_event = Event()
                bot.send_message(callback.message.chat.id, "Успешно отправлено на проверку")

                kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
                kb2 = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton("Мои мероприятия", callback_data="myevents")
                btn2 = types.InlineKeyboardButton("Создать", callback_data="crevent")
                btn3 = types.InlineKeyboardButton("Редактировать", callback_data="edevent")
                btn4 = types.InlineKeyboardButton("Удалить", callback_data="delevent")
                
                kb.add("На главную")
                kb2.add(btn1);
                kb2.add(btn2);
                kb2.add(btn3, btn4);

                bot.send_message(callback.message.chat.id, "Выберите действие", reply_markup=kb2)
                bot.send_message(callback.message.chat.id, "Действия:", reply_markup=kb)

            else:
                bot.send_message(callback.message.chat.id, "Какие-то из обязательных параметров не указаны")

        case "addtagtousersearch":
            tag = commands[1]
            if(tag not in all_users[callback.message.chat.id].searchtags):
                all_users[callback.message.chat.id].searchtags.append(tag)
                bot.send_message(callback.message.chat.id, "Добавлен тег в поисковый фильтр");
                return;
            
            all_users[callback.message.chat.id].searchtags.remove(tag)
            bot.send_message(callback.message.chat.id, "Тег удалён из поискового фильтра");

        case "searchfortags":
            arr = []
            tags = all_users[callback.message.chat.id].searchtags;
            for i in all_events:
                for t in all_events[i][1].tags:
                    if t in tags:
                        arr.append(all_events[i][1])
                        break;

            if len(arr) == 0:
                bot.send_message(callback.message.chat.id, "Мероприятия по указанным тегам не найдены");
                return;
            send_events(arr, callback.message.chat.id)

        case "findweekday":
            day = int(commands[1])
            arr = []
            for i in all_events:
                all_events[i][1].start_datetime.isoweekday()
                if all_events[i][1].start_datetime.isoweekday() == day and all_events[i][1].start_datetime > datetime.datetime.now():
                    arr.append(all_events[i][1])

            if len(arr) == 0:
                bot.send_message(callback.message.chat.id, "Ничего не нашлось")
                return;

            bot.send_message(callback.message.chat.id, f"Вот мероприятия на {day_of_week[day]}")
            send_events(arr, callback.message.chat.id)

        case "reminder":
            ev_id = commands[1]
            kb2 = types.InlineKeyboardMarkup()
            btn1 =  types.InlineKeyboardButton("За неделю",   callback_data=f"setremindermin {ev_id} {10080}")
            btn2 =  types.InlineKeyboardButton("За 3 дня",    callback_data=f"setremindermin {ev_id} {4320}")
            btn3 =  types.InlineKeyboardButton("За 2 дня",    callback_data=f"setremindermin {ev_id} {2880}")
            btn4 =  types.InlineKeyboardButton("За 1 день",   callback_data=f"setremindermin {ev_id} {1440}")
            btn5 =  types.InlineKeyboardButton("За 12 часов", callback_data=f"setremindermin {ev_id} {720}")
            btn6 =  types.InlineKeyboardButton("За 6 часов",  callback_data=f"setremindermin {ev_id} {360}")
            btn7 =  types.InlineKeyboardButton("За 3 часа",   callback_data=f"setremindermin {ev_id} {180}")
            btn8 =  types.InlineKeyboardButton("За 2 часа",   callback_data=f"setremindermin {ev_id} {120}")
            btn9 =  types.InlineKeyboardButton("За 1 час",    callback_data=f"setremindermin {ev_id} {60}")
            btn10 = types.InlineKeyboardButton("За 30 минут", callback_data=f"setremindermin {ev_id} {30}")
            btn11 = types.InlineKeyboardButton("За 1 минуту", callback_data=f"setremindermin {ev_id} {1}")
            kb2.add(btn1 )
            kb2.add(btn2 )
            kb2.add(btn3 )
            kb2.add(btn4 )
            kb2.add(btn5 )
            kb2.add(btn6 )
            kb2.add(btn7 )
            kb2.add(btn8 )
            kb2.add(btn9 )
            kb2.add(btn10)
            kb2.add(btn11)
            bot.send_message(callback.message.chat.id, "За сколько напомнить?", reply_markup=kb2);

        case "setremindermin":
            ev_id = int(commands[1])
            minut = int(commands[2])
           
            if len(all_users[callback.message.chat.id].reminder.values()) == 0:
                all_users[callback.message.chat.id].reminder[ev_id] = [all_events[ev_id][1].start_datetime-datetime.timedelta(minutes=minut)]
            else:
                all_users[callback.message.chat.id].reminder[ev_id].append(all_events[ev_id][1].start_datetime-datetime.timedelta(minutes=minut))
            
                



@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    usr_id = message.chat.id;
    text = message.text.lower()

    if(usr_id not in all_users):
        all_users[usr_id] = User(message.from_user.first_name)
        bot.send_message(usr_id, f"Приветствую, {all_users[usr_id].name}!")
        
    if text in ("/start", "/restart"):
        message.text = "main_menu"
        bot.delete_message(usr_id, message.message_id) # удаление пользовательской команды
        check_callback_data(types.CallbackQuery(usr_id,message=message, from_user=None, data = "main_menu", chat_instance=None, json_string=None))

    else:
        bot.delete_message(usr_id, message.message_id) # удаление пользовательской команды


    match message.text.lower():            
        # 2 страница модератор
        case "мероприятия на модерацию":
            if(len(all_events_on_moderate) > 0):
                kb2 = types.InlineKeyboardMarkup()
                btn11 = types.InlineKeyboardButton("Принять", callback_data="eventsmoderateyes")
                btn22 = types.InlineKeyboardButton("Отклонить", callback_data="eventmoderateno")

         
                bot.send_message(message.chat.id, "Проверить:")

                i = all_events_on_moderate[0][2];
                id_ = message.chat.id

                bot.send_message(id_, "Главное фото:")
                if(i.main_photo):
                    img = open(i.main_photo, 'rb')
                    bot.send_photo(id_, img)

                bot.send_message(id_, "Дополнительные фото:")
                for j in i.photos:
                    img = open(j, 'rb')
                    bot.send_photo(id_, img)

                bot.send_message(id_, "Остальное:")
                if isinstance(i.pay_web, str):
                    btn1 = types.InlineKeyboardButton("Покупка", url=i.pay_web)
                    kb2.add(btn1)
                if isinstance(i.location, list):
                    btn2 = types.InlineKeyboardButton("Показать на карте", url= f"https://yandex.ru/maps/?ll={i.location[1]},{i.location[0]}&z=17&mode=search&whatshere[point]={i.location[1]},{i.location[0]}&whatshere[zoom]=17")
                    kb2.add(btn2)
            
                kb2.add(btn11, btn22);

                bot.send_message(id_, i.get_string_event(), reply_markup=kb2)

            else:
                bot.send_message(message.chat.id, "Мероприятий на проверку пока нет")


        # 3 страница поиск по радиусу
        case "500 метров":
            if isinstance(all_users[message.chat.id].last_location, list):
                arr = []
                for i in all_events:
                    evn:Event = all_events[i][1]
                    if evn.location:
                        if distance(all_users[message.chat.id].last_location, evn.location) <= 0.5:
                            arr.append(evn);

                if len(arr) == 0:
                    bot.send_message(message.chat.id, "В радиусе 500 метров мероприятий не найдено")
                    
                else:
                    arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)

                    bot.send_message(message.chat.id, "Вот найденные мероприятия:")

                    send_events(arr, message.chat.id)
                    
            else:
                bot.send_message(message.chat.id, "Геолокация устарела, пожалуйста обновите её")

        case "1 километр":
            if isinstance(all_users[message.chat.id].last_location, list):
                arr = []
                for i in all_events:
                    evn:Event = all_events[i][1]
                    if evn.location:
                        if distance(all_users[message.chat.id].last_location, evn.location) <= 1:
                            arr.append(evn);

                if len(arr) == 0:
                    bot.send_message(message.chat.id, "В радиусе 1 километра мероприятий не найдено")
                    
                else:
                    arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)

                    bot.send_message(message.chat.id, "Вот найденные мероприятия:")
                    
                    send_events(arr, message.chat.id)

            else:
                bot.send_message(message.chat.id, "Геолокация устарела, пожалуйста обновите её")

        case "3 километра":
            if isinstance(all_users[message.chat.id].last_location, list):
                arr = []
                for i in all_events:
                    evn:Event = all_events[i][1]
                    if evn.location:
                        if distance(all_users[message.chat.id].last_location, evn.location) <= 3:
                            arr.append(evn);

                if len(arr) == 0:
                    bot.send_message(message.chat.id, "В радиусе 3 километров мероприятий не найдено")
                    
                else:
                    arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)

                    bot.send_message(message.chat.id, "Вот найденные мероприятия:")
                    
                    send_events(arr, message.chat.id)

            else:
                bot.send_message(message.chat.id, "Геолокация устарела, пожалуйста обновите её")

        case "5 километров":
            if isinstance(all_users[message.chat.id].last_location, list):
                arr = []
                for i in all_events:
                    evn:Event = all_events[i][1]
                    if evn.location:
                        if distance(all_users[message.chat.id].last_location, evn.location) <= 5:
                            arr.append(evn);

                if len(arr) == 0:
                    bot.send_message(message.chat.id, "В радиусе 5 километров мероприятий не найдено")
                    
                else:
                    arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)

                    bot.send_message(message.chat.id, "Вот найденные мероприятия:")
                    
                    send_events(arr, message.chat.id)

            else:
                bot.send_message(message.chat.id, "Геолокация устарела, пожалуйста обновите её")






def main():
    while True:
        now = datetime.datetime.now()
        for i in all_users: # i - user_id
            container = all_users[i].reminder # reminder[j] - list
            for j in container: #j - event_id
                for k in container[j]:
                    if(k <= now):
                        all_users[i].reminder[j].remove(k);
                        bot.send_message(i, "Сработало напоминание!");
                        send_events([all_events[j][1]], i);
                        ... #таймер

        time.sleep(1)



Thread(target=main, args=()).start()
bot.polling() 