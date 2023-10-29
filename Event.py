from datetime import datetime

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
            this.start_datetime = datetime.strptime(dt, "%d.%m.%Y %H:%M")
            return True;
        except:
            return False;

    def set_data_end(this, dt:str):
        try:
            this.end_datetime = datetime.strptime(dt, "%d.%m.%Y %H:%M")
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