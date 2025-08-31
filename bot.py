# demo bot
import telebot
from telebot import types
from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    feedback TEXT,
    date TEXT
)
''')
conn.commit()
cur.close()
conn.close()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Menu", callback_data='Menu')
    btn2 = types.InlineKeyboardButton("Kontakti", callback_data='Kontakti')
    btn3 = types.InlineKeyboardButton("HOT PRICES", callback_data='HOT PRICES')
    btn4 = types.InlineKeyboardButton("Atsauksmes", callback_data='Atsauksmes')
    btn5 = types.InlineKeyboardButton("Mūsu tīmekļa vietne", url="https://www.fullfire.lv/")
    markup.row(btn1, btn4)
    markup.row(btn2, btn3)
    markup.row(btn5)
    bot.send_message(
        message.chat.id,
        f"Labdien, {message.from_user.first_name}, kā es jums varu palīdzēt?",
        reply_markup=markup
    )

@bot.message_handler(commands=['all_feedback'])
def all_feedback(message):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT username, feedback, date FROM feedback ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        bot.send_message(message.chat.id, "Nav vēl neviena atsauksme.")
        return

    text = ""
    for row in rows:
        username, feedback_text, date_text = row
        text += f"[{date_text}] {username}: {feedback_text}\n\n"

    # Если текст длинный, разбиваем на несколько сообщений
    for chunk in [text[i:i+4000] for i in range(0, len(text), 4000)]:
        bot.send_message(message.chat.id, chunk)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'Menu':
        bot.send_photo(callback.message.chat.id, open('./menu.png', 'rb'))
    elif callback.data == 'Kontakti':
        bot.send_photo(callback.message.chat.id, open('./map.png', 'rb'))
        bot.send_message(callback.message.chat.id, "Jelgavas iela 23a")
    elif callback.data == 'HOT PRICES':
        bot.send_message(
            callback.message.chat.id,
            "FULLFIRE LAVASH XL - 6$ \nBROKASTU LAVASH L - 5.60$ \nBURRITO LAVASH XL - 6$"
        )
        #or you can send a photo of the menu
        #bot.send_photo(callback.message.chat.id, open('./hot_prices.png', 'rb'))

    elif callback.data == 'Atsauksmes':
        bot.send_message(callback.message.chat.id, "Ievadiet savu atsauksmi")
        bot.register_next_step_handler(callback.message, save_feedback)

def save_feedback(message):
    feedback = message.text
    dt = datetime.fromtimestamp(message.date).strftime("%Y-%m-%d %H:%M:%S")
    
    # Сохраняем в SQLite
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO feedback(user_id, username, feedback, date) VALUES (?, ?, ?, ?)",
        (message.from_user.id, message.from_user.first_name, feedback, dt)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    # # Сохраняем в файл
    # with open("feedback.txt", "a", encoding="utf-8") as f:
    #     f.write(f"[{dt}] {message.from_user.first_name}: {feedback}\n")
    
    bot.send_message(
        message.chat.id,
        f"Paldies par atsauksmi! Jūs rakstījāt:\n{feedback}"
    )

bot.polling(none_stop=True)
