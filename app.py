from telebot import TeleBot, types
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time

start_date = "dd/mm/yyyy" #mention_your_start_date_here
token = "xxxxxx:xxxxxxxxxxxxxxxxxx" #add_your_telebot_token
bot = TeleBot(token)

#add_telegram_chat_id_of_people_to_be_notified
people_list = ['xxxxxxx', 'xxxxxxx'] #can_add_any_number_of_people

def Scrape(day):
   link = []
   content = requests.get("https://github.com/harsh-bothra/learn365/blob/main/README.md").text
   soup = BeautifulSoup(content, 'lxml')
   main_table = soup.find_all('table')[1]
   all_rows = main_table.find_all('tr')
   all_rows.pop(0)
   #fetch_particular_link
   r = all_rows[day-1].find('a')
   link.append(r.text)
   link.append("https://github.com/" + r["href"])
   return link

def Sender():
   today_date = (datetime.now() + timedelta(hours=5.5)).strftime("%d/%m/%Y")
   d1 = datetime.strptime(start_date, "%d/%m/%Y")
   d2 = datetime.strptime(today_date, "%d/%m/%Y")
   num = (d2-d1).days
   res = Scrape(num)
   message = "Hello Today you need to read this !\n\n✅ Day : {}\n\n✅ Title : {}\n\n✅ Link : {} \n\n✅ PUSH YOUR UPDATES IN GITHUB".format(num, res[0], res[1])
   for person in people_list:
     markup = types.ReplyKeyboardMarkup(row_width=5, one_time_keyboard=True)
     btn_one = types.KeyboardButton('Done 👍')
     btn_two = types.KeyboardButton('Will Do 🏃')
     btn_three = types.KeyboardButton('Skip ⏭️')
     markup.row(btn_one, btn_two)
     markup.row(btn_three)
     bot.send_message(person, message, reply_markup=markup, disable_web_page_preview=True)
   print("done")

while True:
   print("running...")
   t = (datetime.now() + timedelta(hours=5.5))
   #change_according_to_your_time - notifies at 5AM, 10AM, 5PM, 9PM
   if t.strftime("%I:%M") == '05:00' and t.strftime("%p") == 'AM':
     Sender()
   if t.strftime("%I:%M") == '10:00' and t.strftime("%p") == 'AM':
     Sender()
   if t.strftime("%I:%M") == '05:00' and t.strftime("%p") == 'PM':
     Sender()
   if t.strftime("%I:%M") == '09:00' and t.strftime("%p") == 'PM':
     Sender()
   time.sleep(60)
