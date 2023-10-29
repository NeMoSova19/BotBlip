import Settings

class User:
    def __init__(this, name, user_id:int, status = "Пользователь"):
        this.name:str = name
        this.status:str = status
        this.user_id:int = user_id
        
        this.event_ids = [] # все эвенты организатора 
        this.pre_event = None # 
        this.last_location = None
        this.bot_msg_ids:list = []
        
        # в разработке
        this.reputation:int = 0 # репутация организатора
        this.vk_id = None # кнопка привязки/отвязка соцсети
        
        # подписки
        this.reminder = {} # {Event_id: [время во сколько будет напоминание:datatime]}
        this.subscription_tags = []      # теги
        this.subscription_days_week = [] # дни недели
        
        # для поиска
        this.searchtags = []
        
    def DeleteMessages(this):
        for i in this.bot_msg_ids:
            #print("delete", i.message_id);
            Settings.bot.delete_message(this.user_id, i.message_id);
        
        this.bot_msg_ids = [];
    
    def SendMessage(this, text, reply_markup = None):
        msg = Settings.bot.send_message(chat_id=this.user_id, text=text, reply_markup=reply_markup)
        #print("create", msg.message_id);
        this.bot_msg_ids.append(msg);
    
    def SendNotDeletableMsg(this, text):
        Settings.bot.send_message(chat_id=this.user_id, text=text)
        
    def EditLastMessage(this, text = None, reply_markup = None):
        #print("edit", this.bot_msg_ids[-1].message_id);
        if text: 
            Settings.bot.edit_message_text(chat_id = this.user_id, message_id = this.bot_msg_ids[-1].message_id, text=text)
        if reply_markup: 
            Settings.bot.edit_message_reply_markup(chat_id = this.user_id, message_id = this.bot_msg_ids[-1].message_id, reply_markup=reply_markup)
        
    def ClearAndReplaceLastMessage(this, text=None, reply_markup=None):
        if(len(this.bot_msg_ids) != 0):
            for i in range(0, len(this.bot_msg_ids)-1):
                Settings.bot.delete_message(this.user_id, this.bot_msg_ids[i].message_id);
                
            this.bot_msg_ids = [this.bot_msg_ids[-1]];
            
            this.EditLastMessage(text, reply_markup)

        else:
            if(text == None): text = "";
            this.SendMessage(text, reply_markup);