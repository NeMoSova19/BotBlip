import RecieveText, Settings, Functions, User, Event, datetime

from threading import Thread
from time import sleep

def RemainingLoop():
    while True:
        now = datetime.datetime.now()
        for i in Settings.all_users: # i - user_id
            container = Settings.all_users[i].reminder # reminder[j] - list
            for j in container: #j - event_id
                for k in container[j]:
                    if(k <= now):
                        Settings.all_users[i].reminder[j].remove(k);
                        Settings.bot.send_message(i, "Сработало напоминание!");
                        Functions.send_events([Settings.all_events[j][1]], i);
                        ... #таймер
        sleep(1)


Thread(target=RemainingLoop, args=()).start()

print("Server started");
Settings.bot.polling() 

# Error 309: User.ClearAndReplaceLastMessage() got multiple values for argument 'text'

{
  "id": 5120192724200265000,
  "chat_instance": "-2441527340029028207",
  "data": "cbcal_0_s_y_2025_10_28",
  
  "from_user": {
    "id": 1192137767,
    "is_bot": 0,
    "first_name": "Владислав",
    "username": "Vladislavyr",
    "language_code": "ru"
  },
  "message": {
    "content_type": "text",
    "id": 8409,
    "message_id": 8409,
    "from_user": "<telebot.types.User object at 0x0000028C60D0A250>",
    "date": 1698449173,
    "chat": "<telebot.types.Chat object at 0x0000028C60D0B4D0>",
    "text": "select year",
    "reply_markup": "<telebot.types.InlineKeyboardMarkup object at 0x0000028C60D0BE10>",
  },
}

{
  "id": 5120192724200265000,
  "from_user": {
    "id": 1192137767,
    "is_bot": 0,
    "first_name": "Владислав",
    "username": "Vladislavyr",
    "language_code": "ru"
  },
  "message": {
    "content_type": "text",
    "id": 8409,
    "message_id": 8409,
    "from_user": "<telebot.types.User object at 0x0000028C60D0A250>",
    "date": 1698449173,
    "chat": "<telebot.types.Chat object at 0x0000028C60D0B4D0>",
    "text": "select year",
    "reply_markup": "<telebot.types.InlineKeyboardMarkup object at 0x0000028C60D0BE10>",
    "json": {
      "message_id": 8409,
      "from": {
        "id": 6189215832,
        "is_bot": 1,
        "first_name": "EventHub",
        "username": "BotBlip_bot"
      },
      "chat": {
        "id": 1192137767,
        "first_name": "Владислав",
        "username": "Vladislavyr",
        "type": "private"
      },
      "date": 1698449173,
      "text": "select year",
      "reply_markup": {
        "inline_keyboard": [
          [
            {
              "text": "2022",
              "callback_data": "cbcal_0_s_y_2022_10_28"
            },
            {
              "text": "2023",
              "callback_data": "cbcal_0_s_y_2023_10_28"
            }
          ],
          [
            {
              "text": "2024",
              "callback_data": "cbcal_0_s_y_2024_10_28"
            },
            {
              "text": "2025",
              "callback_data": "cbcal_0_s_y_2025_10_28"
            }
          ],
          [
            {
              "text": "<<",
              "callback_data": "cbcal_0_g_y_2019_10_28"
            },
            {
              "text": " ",
              "callback_data": "cbcal_0_n"
            },
            {
              "text": ">>",
              "callback_data": "cbcal_0_g_y_2027_10_28"
            }
          ]
        ]
      }
    }
  },
  "chat_instance": "-2441527340029028207",
  "data": "cbcal_0_s_y_2025_10_28",
  "json": {
    "id": "5120192724200264569",
    "from": {
      "id": 1192137767,
      "is_bot": 0,
      "first_name": "Владислав",
      "username": "Vladislavyr",
      "language_code": "ru"
    },
    "message": {
      "message_id": 8409,
      "from": {
        "id": 6189215832,
        "is_bot": 1,
        "first_name": "EventHub",
        "username": "BotBlip_bot"
      },
      "chat": {
        "id": 1192137767,
        "first_name": "Владислав",
        "username": "Vladislavyr",
        "type": "private"
      },
      "date": 1698449173,
      "text": "select year",
      "reply_markup": {
        "inline_keyboard": [
          [
            {
              "text": "2022",
              "callback_data": "cbcal_0_s_y_2022_10_28"
            },
            {
              "text": "2023",
              "callback_data": "cbcal_0_s_y_2023_10_28"
            }
          ],
          [
            {
              "text": "2024",
              "callback_data": "cbcal_0_s_y_2024_10_28"
            },
            {
              "text": "2025",
              "callback_data": "cbcal_0_s_y_2025_10_28"
            }
          ],
          [
            {
              "text": "<<",
              "callback_data": "cbcal_0_g_y_2019_10_28"
            },
            {
              "text": " ",
              "callback_data": "cbcal_0_n"
            },
            {
              "text": ">>",
              "callback_data": "cbcal_0_g_y_2027_10_28"
            }
          ]
        ]
      }
    },
    "chat_instance": "-2441527340029028207",
    "data": "cbcal_0_s_y_2025_10_28"
  }
}