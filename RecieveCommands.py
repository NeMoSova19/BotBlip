import telegram_bot_calendar as TGcalendar
import Functions
import User
import telebot
import Settings
import datetime
import Event

# calendar, step = TGcalendar.DetailedTelegramCalendar().build()
# AddBotMessage(usr_id, bot.send_message(usr_id, f"select {TGcalendar.LSTEP[step]}", reply_markup=calendar));

@Settings.bot.callback_query_handler(func=lambda x: True)
def check_callback_data(callback):
    
    #global Settings.free_event_id;
    User_ID = callback.message.chat.id;
    User_NOW:User.User = Settings.all_users[User_ID];
    
    if(len(callback.message.text) != 0 and callback.message.text.split()[0].strip() == "select"):
        commands = callback.message.text.split()
    else:
        commands = callback.data.split()
        
    try:
        Settings.bot.clear_step_handler(callback.message)
    except:
        ...
        
    # User_NOW.SendMessage(text=, reply_markup=kb);
    # User_NOW.ClearAndReplaceLastMessage(text=, reply_markup=kb);
    match commands[0]:
    
        case "select":
            result, key, step = TGcalendar.DetailedTelegramCalendar().process(callback.data)
            if not result and key:
                User_NOW.SendMessage("", reply_markup=kb);
                User_NOW.ClearAndReplaceLastMessage(text=f"select {TGcalendar.LSTEP[step]}", reply_markup=key);
            elif result:
                Functions.DeleteBotMessages(User_ID);
                User_NOW.ClearAndReplaceLastMessage(text=f"You selected {result}");
                Functions.ReCallback(User_ID, "main_menu", "main_menu");            

        case "main_menu":
            kb = telebot.types.InlineKeyboardMarkup();
            kb.add(telebot.types.InlineKeyboardButton("Профиль", callback_data="profile 0"))
            kb.add(telebot.types.InlineKeyboardButton("Пользователь", callback_data="user"))
            if User_NOW.status != "Пользователь":
                kb.add(telebot.types.InlineKeyboardButton("Организатор", callback_data="eventor"))
            if User_NOW.status == "Модератор":
                kb.add(telebot.types.InlineKeyboardButton("Модератор", callback_data="moderator"))

            User_NOW.DeleteMessages()
            User_NOW.SendMessage("Главное меню", reply_markup=kb);

        case "profile":
            kb = telebot.types.InlineKeyboardMarkup();

            about_user = f"Имя: {User_NOW.name}\nСтатус: {User_NOW.status}\n"
            if User_NOW.status == "Организатор":
                about_user += f"Репутация: {User_NOW.reputation}\n"

            d = "нет данных" if (User_NOW.vk_id == None) else User_NOW.vk_id
            about_user += f"Аккаунт VK: {d}\nПодписки:\nСкоро..."

            btn1 = telebot.types.InlineKeyboardButton("изменить имя", callback_data="rename")
            kb.add(btn1);
            if(User_NOW.status == "Пользователь"):
                kb.add(telebot.types.InlineKeyboardButton("стать организатором", callback_data="upgrade_eventor"))
            elif(User_NOW.status == "Организатор"):
                kb.add(telebot.types.InlineKeyboardButton("стать модератором", callback_data="upgrade_moder"))
            kb.add(telebot.types.InlineKeyboardButton("на главную", callback_data="main_menu"))
            
            User_NOW.ClearAndReplaceLastMessage(text=f"Профиль\n{about_user}", reply_markup=kb);

        case "user":
            kb = telebot.types.InlineKeyboardMarkup()
            btn1 = telebot.types.InlineKeyboardButton("Сегодня", callback_data="now")
            btn2 = telebot.types.InlineKeyboardButton("Завтра", callback_data="tomorrow")
            btn3 = telebot.types.InlineKeyboardButton("На этой неделе", callback_data="onweek")
            btn4 = telebot.types.InlineKeyboardButton("Поиск по тегам", callback_data="find_for_tags")
            btn5 = telebot.types.InlineKeyboardButton("Поиск по дням", callback_data="find_for_days")
            btn6 = telebot.types.InlineKeyboardButton("Поиск по радиусу", callback_data="find_for_radius")
            btn7 = telebot.types.InlineKeyboardButton("На главную", callback_data="main_menu")

            kb.add(btn1, btn2, btn3)
            kb.add(btn4, btn5)
            kb.add(btn6)
            kb.add(btn7)
         
            User_NOW.ClearAndReplaceLastMessage(text="Выберите нужное действие", reply_markup=kb);

        case "eventor":
            kb = telebot.types.InlineKeyboardMarkup()
            btn1 = telebot.types.InlineKeyboardButton("Мои мероприятия", callback_data="myevents")
            btn2 = telebot.types.InlineKeyboardButton("Создать", callback_data="crevent")
            btn3 = telebot.types.InlineKeyboardButton("Редактировать", callback_data="edevent")
            btn4 = telebot.types.InlineKeyboardButton("Удалить", callback_data="delevent")
            btn5 = telebot.types.InlineKeyboardButton("На главную", callback_data="main_menu")
            
            kb.add(btn1);
            kb.add(btn2);
            kb.add(btn3, btn4);
            kb.add(btn5)
         
            User_NOW.ClearAndReplaceLastMessage(text="Выберите ", reply_markup=kb);

        case "moderator":
            kb = telebot.types.InlineKeyboardMarkup()
            btn1 = telebot.types.InlineKeyboardButton("Мероприятия на модерацию", callback_data="eventsonmoderate")
            btn2 = telebot.types.InlineKeyboardButton("На главную", callback_data="main_menu")
            kb.add(btn1)
            kb.add(btn2)
         
            User_NOW.ClearAndReplaceLastMessage(text="Выберите ", reply_markup=kb);

        case "eventsonmoderate":
            if(len(Settings.all_events_on_moderate) > 0):
                kb = telebot.types.InlineKeyboardMarkup()
                btn11 = telebot.types.InlineKeyboardButton("Принять", callback_data="eventsmoderateyes")
                btn22 = telebot.types.InlineKeyboardButton("Отклонить", callback_data="eventmoderateno")

         
                User_NOW.ClearAndReplaceLastMessage(text="Проверить:");

                i = Settings.all_events_on_moderate[0][2];
                id_ = User_ID

                User_NOW.ClearAndReplaceLastMessage(text="Главное фото:");
                if(i.main_photo):
                    img = open(i.main_photo, 'rb')
                    Settings.bot.send_photo(id_, img)

                User_NOW.ClearAndReplaceLastMessage(text="Дополнительные фото:");
                for j in i.photos:
                    img = open(j, 'rb')
                    Settings.bot.send_photo(id_, img)

                if isinstance(i.pay_web, str):
                    btn1 = telebot.types.InlineKeyboardButton("Покупка", url=i.pay_web)
                    kb.add(btn1)
                if isinstance(i.location, list):
                    btn2 = telebot.types.InlineKeyboardButton("Показать на карте", url= f"https://yandex.ru/maps/?ll={i.location[1]},{i.location[0]}&z=17&mode=search&whatshere[point]={i.location[1]},{i.location[0]}&whatshere[zoom]=17")
                    kb.add(btn2)
            
                kb.add(btn11, btn22);

                User_NOW.ClearAndReplaceLastMessage(text=i.get_string_event(), reply_markup=kb);

            else:
                User_NOW.ClearAndReplaceLastMessage(text="Мероприятий на проверку пока нет");
        
        case "rename":
            User_NOW.ClearAndReplaceLastMessage(text="Введите новое имя");
            Settings.bot.register_next_step_handler(callback.message, Functions.rename)

        case "upgrade_eventor":
            User_NOW.status = "Организатор"

            Functions.ReCallback(User_ID, "profile 1", "profile 1");

        case "upgrade_moder":
            User_NOW.status = "Модератор"

            Functions.ReCallback(User_ID, "profile 1", "profile 1");

        case "now":
            now = datetime.datetime.now()
            arr = []
            for i in Settings.all_events:
                evn = Settings.all_events[i][1]
                if(evn.start_datetime.day == now.day and evn.start_datetime.time() > now.time()):
                    arr.append(evn);
            if len(arr) == 0:
                User_NOW.ClearAndReplaceLastMessage(text="На сегодня мероприятий не найдено");
                
            else:
                arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)
                User_NOW.ClearAndReplaceLastMessage(text="Вот мероприятия на сегодня:");
                
                Functions.send_events(arr, User_ID)

        case "tomorrow":
            now = datetime.datetime.now()
            arr = []
            for i in Settings.all_events:
                evn = Settings.all_events[i][1]
                if((evn.start_datetime.day - 1) == now.day):
                    arr.append(evn);
            if len(arr) == 0:
                User_NOW.ClearAndReplaceLastMessage(text="На завтра мероприятий не найдено");
                
            else:
                arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)
                User_NOW.ClearAndReplaceLastMessage(text="Вот мероприятия на завтра:");
                
                Functions.send_events(arr, User_ID)

        case "onweek":
            now = datetime.datetime.now()
            now_week = now.isocalendar()[1]

            arr = []
            for i in Settings.all_events:
                evn = Settings.all_events[i][1]
                if(evn.start_datetime > now and now_week == evn.start_datetime.isocalendar()[1]):
                    arr.append(evn);
            if len(arr) == 0:
                User_NOW.ClearAndReplaceLastMessage(text="На этой ннедели мероприятий не найдено");
                
            else:
                arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)
        
                User_NOW.ClearAndReplaceLastMessage(text="Вот мероприятия на этой неделе:");

                Functions.send_events(arr, User_ID)

        case "find_for_tags":
            if len(Settings.all_tags) == 0:
                User_NOW.ClearAndReplaceLastMessage(text="Тегов пока нет, так как организаторы не создали не одного мероприятия");
                return;

            User_NOW.searchtags = [];
            kb = telebot.types.InlineKeyboardMarkup(row_width=2)

            for i in Settings.all_tags:
                kb.add(telebot.types.InlineKeyboardButton(i, callback_data=f"addtagtousersearch {i}"))

            kb.add(telebot.types.InlineKeyboardButton("Поиск", callback_data=f"searchfortags"))
            User_NOW.ClearAndReplaceLastMessage(text="Теги:", reply_markup=kb)      

        case "find_for_days":
            kb = telebot.types.InlineKeyboardMarkup()
            btn1 = telebot.types.InlineKeyboardButton("Понедельник", callback_data=f"findweekday {1}")
            btn2 = telebot.types.InlineKeyboardButton("Вторник",     callback_data=f"findweekday {2}")
            btn3 = telebot.types.InlineKeyboardButton("Среда",       callback_data=f"findweekday {3}")
            btn4 = telebot.types.InlineKeyboardButton("Четверг",     callback_data=f"findweekday {4}")
            btn5 = telebot.types.InlineKeyboardButton("Пятница",     callback_data=f"findweekday {5}")
            btn6 = telebot.types.InlineKeyboardButton("Суббота",     callback_data=f"findweekday {6}")
            btn7 = telebot.types.InlineKeyboardButton("Воскресенье", callback_data=f"findweekday {7}")
            btn8 = telebot.types.InlineKeyboardButton("Назад", callback_data="User_NOW")
            btn9 = telebot.types.InlineKeyboardButton("На главную", callback_data="main_menu")
            kb.add(btn1)
            kb.add(btn2)
            kb.add(btn3)
            kb.add(btn4)
            kb.add(btn5)
            kb.add(btn6)
            kb.add(btn7)
            kb.add(btn8, btn9)

            User_NOW.ClearAndReplaceLastMessage(text="Выберите день недели", reply_markup=kb)

        case "find_for_radius":
            kb = telebot.types.InlineKeyboardMarkup()
            kb2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            
            btn = telebot.types.KeyboardButton(text="Поделиться моей геолокацией",request_location=True);
            kb2.add(btn)            

            if isinstance(User_NOW.last_location, list):
                btn1 = telebot.types.InlineKeyboardButton("500 метров", callback_data=f"distance_to {0.5}")
                btn2 = telebot.types.InlineKeyboardButton("1 километр", callback_data=f"distance_to {1}")
                btn3 = telebot.types.InlineKeyboardButton("3 километра", callback_data=f"distance_to {3}")
                btn4 = telebot.types.InlineKeyboardButton("5 километров", callback_data=f"distance_to {5}")
                kb.add(btn1, btn2);
                kb.add(btn3, btn4);
            
            kb.add(telebot.types.InlineKeyboardButton("Назад", callback_data="user"))
            kb.add(telebot.types.InlineKeyboardButton("На главную", callback_data="main_menu"))

            User_NOW.DeleteMessages();
            User_NOW.SendMessage(text="_", reply_markup=kb2)
            User_NOW.SendMessage(text="Выберите нужное действие", reply_markup=kb)
  
        case "myevents":
            if len(User_NOW.event_ids) == 0:
                Settings.bot.send_message(User_ID, "Пусто")
                return;

            Functions.send_events([Settings.all_events[i][1] for i in User_NOW.event_ids], User_ID);
                    
        case "crevent":
            User_NOW.pre_event = Event.Event(Settings.free_event_id)
            kb = telebot.types.InlineKeyboardMarkup()
            btn1 = telebot.types.InlineKeyboardButton("Название*", callback_data="seteventtitle")
            btn2 = telebot.types.InlineKeyboardButton("Описание", callback_data="seteventdescription")
            btn3 = telebot.types.InlineKeyboardButton("Основное фото", callback_data="seteventmainimg")
            btn4 = telebot.types.InlineKeyboardButton("Доп фото", callback_data="addeventimg")
            btn5 = telebot.types.InlineKeyboardButton("Возрастное ограничение", callback_data="seteventage")
            btn6 = telebot.types.InlineKeyboardButton("Цена билета", callback_data="seteventpay")
            btn61 =telebot.types.InlineKeyboardButton("Ссылка на оплату", callback_data="seteventpay_web")
            btn7 = telebot.types.InlineKeyboardButton("Количество мест", callback_data="seteventplaces")
            btn8 = telebot.types.InlineKeyboardButton("Местоположение*", callback_data="seteventgeo")
            btn9 = telebot.types.InlineKeyboardButton("Время начала*", callback_data="seteventstart")
            btn10 =telebot.types.InlineKeyboardButton("Время конца", callback_data="seteventend")
            btn11 =telebot.types.InlineKeyboardButton("Теги", callback_data="seteventtags")
            btn12 =telebot.types.InlineKeyboardButton("Предпросмотр", callback_data="previewevent")
            btn13 =telebot.types.InlineKeyboardButton("Опубликовать", callback_data="sendtoverefication")
            
            kb.add(btn1, btn2);
            kb.add(btn3, btn4);
            kb.add(btn5);
            kb.add(btn6, btn61);
            kb.add(btn7, btn8);
            kb.add(btn9, btn10);
            kb.add(btn11);
            kb.add(btn12, btn13);

            User_NOW.ClearAndReplaceLastMessage(User_ID, text="Форма заполнения", reply_markup=kb);

        case "edevent":
            for ev_id in User_NOW.event_ids:
                ev = Settings.all_events[ev_id][1];
            
                kb = telebot.types.InlineKeyboardMarkup()
                btn = telebot.types.InlineKeyboardButton("Изменить", callback_data=f"editevent {ev_id}");
                kb.add(btn);
                User_NOW.ClearAndReplaceLastMessage(User_ID, text=ev.title, reply_markup=kb);
                
            else:
                User_NOW.ClearAndReplaceLastMessage(User_ID, text="Пусто");

        case "delevent":
            for ev_id in User_NOW.event_ids:
                ev = Settings.all_events[ev_id][1];

                kb = telebot.types.InlineKeyboardMarkup()
                btn = telebot.types.InlineKeyboardButton("Удалить", callback_data=f"deleteevent {ev_id}");
                
                kb.add(btn);
                User_NOW.ClearAndReplaceLastMessage(User_ID, text=ev.title, reply_markup=kb);

            else:
                User_NOW.ClearAndReplaceLastMessage(User_ID, text="Пусто");

        case "editevent":
            User_NOW.pre_event = Settings.all_events[int(commands[1])][1]

            kb = telebot.types.InlineKeyboardMarkup()
            btn1 = telebot.types.InlineKeyboardButton("Название", callback_data="seteventtitle")
            btn2 = telebot.types.InlineKeyboardButton("Описание", callback_data="seteventdescription")
            btn3 = telebot.types.InlineKeyboardButton("Основное фото", callback_data="seteventmainimg")
            btn4 = telebot.types.InlineKeyboardButton("Доп фото", callback_data="addeventimg")
            btn5 = telebot.types.InlineKeyboardButton("Возрастное ограничение", callback_data="seteventage")
            btn6 = telebot.types.InlineKeyboardButton("Цена билета", callback_data="seteventpay")
            btn61 =telebot.types.InlineKeyboardButton("Ссылка на оплату", callback_data="seteventpay_web")
            btn7 = telebot.types.InlineKeyboardButton("Количество мест", callback_data="seteventplaces")
            btn8 = telebot.types.InlineKeyboardButton("Местоположение", callback_data="seteventgeo")
            btn9 = telebot.types.InlineKeyboardButton("Время начала", callback_data="seteventstart")   
            btn10 =telebot.types.InlineKeyboardButton("Время конца", callback_data="seteventend")
            btn11 =telebot.types.InlineKeyboardButton("Теги", callback_data="seteventtags")
            btn12 =telebot.types.InlineKeyboardButton("Предпросмотр", callback_data="previewevent")
            btn13 =telebot.types.InlineKeyboardButton("Опубликовать", callback_data=f"sendtoverefication2 {commands[1]}")
            
            kb.add(btn1, btn2);
            kb.add(btn3, btn4);
            kb.add(btn5);
            kb.add(btn6, btn61);
            kb.add(btn7, btn8);
            kb.add(btn9, btn10);
            kb.add(btn11);
            kb.add(btn12, btn13);

            User_NOW.ClearAndReplaceLastMessage(User_ID, text="Выберите нужные действия", reply_markup=kb);

        case "deleteevent":
            User_ID = User_ID;
            User_NOW.event_ids.remove(int(commands[1]))
            del Settings.all_events[int(commands[1])]
            
            User_NOW.ClearAndReplaceLastMessage(User_ID, text="Удалено");

        case "eventsmoderateyes":
            if(len(Settings.all_events_on_moderate) > 0):
                User_ID_TO, evn_id, evnt = Settings.all_events_on_moderate[0]

                Settings.all_events[evn_id] = [User_ID, evnt];
                User_NOW.event_ids.append(evn_id)

                del Settings.all_events_on_moderate[0];

                User_NOW.SendNotDeletableMsg(User_ID_TO, text="Ваше мероприятие принято");
                
                Functions.ReCallback(User_ID, "moderator", "moderator");

        case "eventmoderateno":
            if(len(Settings.all_events_on_moderate) > 0):
                User_ID_TO, evn_id, evnt = Settings.all_events_on_moderate[0]

                del Settings.all_events_on_moderate[0];

                User_NOW.SendNotDeletableMsg(User_ID_TO, text="Ваше мероприятие отклонено");

                Functions.ReCallback(User_ID, "moderator", "moderator");

        case "previewevent":
            Functions.send_events([User_NOW.pre_event], User_ID, is_test=True);
           
        case "seteventtitle":
            User_NOW.ClearAndReplaceLastMessage(text="Введите название");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventtitle)

        case "seteventdescription":
            User_NOW.ClearAndReplaceLastMessage(text="Введите описание");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventdescription)

        case "seteventmainimg":
            User_NOW.ClearAndReplaceLastMessage(text="Отправьте фото (png или jpg)");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventmainimg)

        case "addeventimg":
            User_NOW.ClearAndReplaceLastMessage(text="Отправьте фото (png или jpg)");
            Settings.bot.register_next_step_handler(callback.message, Functions.addeventimg)
            
        case "seteventage":
            User_NOW.ClearAndReplaceLastMessage(text="Введите возрастное ограничение (пример: 12+)");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventage)

        case "seteventpay":
            User_NOW.ClearAndReplaceLastMessage(text="Укажите цену (если бесплатно, так и напишите)");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventpay)

        case "seteventplaces":
            User_NOW.ClearAndReplaceLastMessage(text="Укажите максимальное количество мест (или неограниченно)");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventplaces)

        case "seteventgeo":
            User_NOW.ClearAndReplaceLastMessage(text="Укажите геолакацию: долгота и широта, через пробел");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventgeo)

        case "seteventtags":
            User_NOW.ClearAndReplaceLastMessage(text="Перечислите основные направления вашего мероприятия через пробел");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventage)

        case "seteventstart":
            User_NOW.ClearAndReplaceLastMessage(text="Укажите дату начала и время. \nпример: 23.04.2004 12:43");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventstart)

        case "seteventend":
            User_NOW.ClearAndReplaceLastMessage(text="Укажите дату окончания и время. \nпример: 23.04.2004 12:50");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventend)

        case "seteventpay_web":
            User_NOW.ClearAndReplaceLastMessage(text="Укажите ссылку на страницу оплаты");
            Settings.bot.register_next_step_handler(callback.message, Functions.seteventpay_web)

        case "sendtoverefication":
            if(User_NOW.pre_event.title and User_NOW.pre_event.start_datetime and User_NOW.pre_event.location):
                
                Settings.all_events_on_moderate.append([User_ID, Settings.free_event_id, User_NOW.pre_event]);
                Settings.free_event_id+=1;
                #User_NOW.pre_event = Event.Event()
                Settings.bot.send_message(User_ID, "Успешно отправлено на проверку")

                Functions.ReCallback(User_ID, "eventor", "eventor")

            else:
                User_NOW.ClearAndReplaceLastMessage(text="Какие-то из обязательных параметров не указаны");

        case "sendtoverefication2":
            if(User_NOW.pre_event.title and User_NOW.pre_event.start_datetime and User_NOW.pre_event.location):
                User_ID = User_ID;
                User_NOW.event_ids.remove(int(commands[1]))
                del Settings.all_events[int(commands[1])]
                
                Settings.all_events_on_moderate.append([User_ID, Settings.free_event_id, User_NOW.pre_event]);
                Settings.free_event_id+=1;
                #User_NOW.pre_event = Event.Event()
                User_NOW.ClearAndReplaceLastMessage(text="Успешно отправлено на проверку");
                
                Functions.ReCallback(User_ID, "eventor", "eventor")

            else:
                User_NOW.ClearAndReplaceLastMessage(text="Какие-то из обязательных параметров не указаны");

        case "addtagtousersearch":
            tag = commands[1]
            if(tag not in User_NOW.searchtags):
                User_NOW.searchtags.append(tag)
                User_NOW.ClearAndReplaceLastMessage(text="Добавлен тег в поисковый фильтр");
                return;
            
            User_NOW.searchtags.remove(tag)
            User_NOW.ClearAndReplaceLastMessage(text="Тег удалён из поискового фильтра");

        case "searchfortags":
            arr = []
            tags = User_NOW.searchtags;
            for i in Settings.all_events:
                for t in Settings.all_events[i][1].tags:
                    if t in tags:
                        arr.append(Settings.all_events[i][1])
                        break;

            if len(arr) == 0:
                User_NOW.ClearAndReplaceLastMessage(text="Мероприятия по указанным тегам не найдены");
                return;
            Functions.send_events(arr, User_ID)

        case "findweekday":
            day = int(commands[1])
            arr = []
            for i in Settings.all_events:
                Settings.all_events[i][1].start_datetime.isoweekday()
                if Settings.all_events[i][1].start_datetime.isoweekday() == day and Settings.all_events[i][1].start_datetime > datetime.datetime.now():
                    arr.append(Settings.all_events[i][1])

            if len(arr) == 0:
                User_NOW.ClearAndReplaceLastMessage(text="Ничего не нашлось");
                return;

            User_NOW.ClearAndReplaceLastMessage(text=f"Вот мероприятия на {Settings.day_of_week[day]}");
            Functions.send_events(arr, User_ID)

        case "reminder":
            ev_id = commands[1]
            kb = telebot.types.InlineKeyboardMarkup()
            btn1 =  telebot.types.InlineKeyboardButton("За неделю",   callback_data=f"setremindermin {ev_id} {10080}")
            btn2 =  telebot.types.InlineKeyboardButton("За 3 дня",    callback_data=f"setremindermin {ev_id} {4320}")
            btn3 =  telebot.types.InlineKeyboardButton("За 2 дня",    callback_data=f"setremindermin {ev_id} {2880}")
            btn4 =  telebot.types.InlineKeyboardButton("За 1 день",   callback_data=f"setremindermin {ev_id} {1440}")
            btn5 =  telebot.types.InlineKeyboardButton("За 12 часов", callback_data=f"setremindermin {ev_id} {720}")
            btn6 =  telebot.types.InlineKeyboardButton("За 6 часов",  callback_data=f"setremindermin {ev_id} {360}")
            btn7 =  telebot.types.InlineKeyboardButton("За 3 часа",   callback_data=f"setremindermin {ev_id} {180}")
            btn8 =  telebot.types.InlineKeyboardButton("За 2 часа",   callback_data=f"setremindermin {ev_id} {120}")
            btn9 =  telebot.types.InlineKeyboardButton("За 1 час",    callback_data=f"setremindermin {ev_id} {60}")
            btn10 = telebot.types.InlineKeyboardButton("За 30 минут", callback_data=f"setremindermin {ev_id} {30}")
            btn11 = telebot.types.InlineKeyboardButton("За 1 минуту", callback_data=f"setremindermin {ev_id} {1}")
            kb.add(btn1 )
            kb.add(btn2 )
            kb.add(btn3 )
            kb.add(btn4 )
            kb.add(btn5 )
            kb.add(btn6 )
            kb.add(btn7 )
            kb.add(btn8 )
            kb.add(btn9 )
            kb.add(btn10)
            kb.add(btn11)
            
            User_NOW.ClearAndReplaceLastMessage(text="За сколько напомнить?", reply_markup=kb);

        case "setremindermin":
            ev_id = int(commands[1])
            minut = int(commands[2])
           
            if len(User_NOW.reminder.values()) == 0:
                User_NOW.reminder[ev_id] = [Settings.all_events[ev_id][1].start_datetime-datetime.timedelta(minutes=minut)]
            else:
                User_NOW.reminder[ev_id].append(Settings.all_events[ev_id][1].start_datetime-datetime.timedelta(minutes=minut))
                
        case "distance_to":
            dist = commands[1];
            if isinstance(User_NOW.last_location, list):
                arr = []
                for i in Settings.all_events:
                    evn:Event = Settings.all_events[i][1]
                    if evn.location:
                        if Functions.distance(User_NOW.last_location, evn.location) <= int(dist):
                            arr.append(evn);

                if len(arr) == 0:
                    User_NOW.ClearAndReplaceLastMessage(text=f"В радиусе {dist} километров мероприятий не найдено");
                    
                else:
                    arr = sorted(arr, key=lambda x: x.start_datetime, reverse=True)

                    User_NOW.ClearAndReplaceLastMessage(text="Вот найденные мероприятия:");
                    Settings.send_events(arr, User_ID)

            else:
                User_NOW.ClearAndReplaceLastMessage(text="Геолокация устарела, пожалуйста обновите её");