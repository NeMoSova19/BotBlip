import telebot
import User


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