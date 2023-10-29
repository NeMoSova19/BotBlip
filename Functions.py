import RecieveCommands
import validators
import Functions

from Settings import *
from math import radians, cos, sin, asin, sqrt
from telebot import types

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

def send_events(arr:list, id_, is_test:bool = False):

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

        if not is_test:
            kb2.add(types.InlineKeyboardButton("Напомнить", callback_data=f"reminder {i.id}"))
            
        if(img):
            bot.send_photo(id_, img, i.get_string_event(), reply_markup=kb2);
        else:
            all_users[id_].SendMessage(text=i.get_string_event(), reply_markup=kb2);

        list_img = []
        for i in i.photos:
            list_img.append(open(i, 'rb'))
        
        if len(list_img) != 0:
            bot.send_media_group(id_, media=[types.InputMediaPhoto(i) for i in list_img]);
       
@bot.message_handler(content_types=['location'])
def handle_location(message):
    bot.delete_message(message.chat.id, message.message_id) # удаление пользовательской команды
    print("{0}, {1}".format(message.location.latitude, message.location.longitude))            

def rename(message):
    all_users[message.chat.id].name = message.text
    bot.delete_message(message.chat.id, message.message_id) # удаление пользовательской команды
    Functions.ReCallback(message.chat.id, "profile 1", "profile 1");

def seteventtitle(message):
    all_users[message.chat.id].pre_event.title = message.text;
    bot.delete_message(message.chat.id, message.message_id) # удаление пользовательской команды

def seteventdescription(message):
    all_users[message.chat.id].pre_event.description = message.text;
    bot.delete_message(message.chat.id, message.message_id) # удаление пользовательской команды

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

def ReCallback(User_ID, text:str, data:str):
    chat = types.Chat(User_ID, type="private")
    user = types.User(User_ID, False, "None")
    message = types.Message(content_type="text",chat=chat, message_id=0, from_user=user,date=0,options=[],json_string="");
    message.text = text;
    RecieveCommands.check_callback_data(types.CallbackQuery(User_ID,message=message, from_user=None, data = data, chat_instance=None, json_string=None))
