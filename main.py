# copyright 2020-21 @Mohamed Rizad
# Telegram @riz4d
# Instagram @riz.4d
import telebot
import requests
from telebot.types import InlineKeyboardButton

# Fillout Here The BotToken it gets from botfather further queries @riz4d 0n telegram
bot = telebot.AKJAS('BOT_TOKEN')

while True:
    try:

        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='Generate email'))
        keyboard.add(InlineKeyboardButton(text='Refresh inbox'))
        keyboard.add(InlineKeyboardButton(text='About'))


        @bot.message_handler(commands=['start'])
        def start_message(message):
            bot.send_message(message.chat.id,
'''
Hello 👋
I am Akira Temp Email Generator which help users to generate a temporary email address.

**Usage of Temporary Mail**
• It can help you to login to a source by hiding your real identity to be saved from mischievous things.
• It can make you to do experimental works in internet by hiding original identity.

Want to know everything about temp-mail system, then /about to know more...!!!

This bot is developed by [Akhil](https://github.com/AKH1LS) for educational purposes to learn about how an API works.
If you are facing issues in generating, report in our project [support group](https://telegram.dog/Akira_Support).

Maintained under [Project Akira](https://telegram.dog/Akira_News).

''',
                             reply_markup=keyboard)


        @bot.message_handler(content_types=['text'])
        def send_text(message):
            if message.text.lower() == 'generate email':
                email = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
                ekeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                ekeyboard.add(InlineKeyboardButton(text='Generate Email'))
                ekeyboard.add(InlineKeyboardButton(text='Refresh Inbox\n[' + str(email) + "]"))
                ekeyboard.add(InlineKeyboardButton(text='About'))
                bot.send_message(message.chat.id, "Your Temporary E-mail:")
                bot.send_message(message.chat.id, str(email), reply_markup=ekeyboard)
            elif message.text.lower() == 'refresh inbox':
                bot.send_message(message.chat.id, 'First, generate an email', reply_markup=keyboard)
            elif message.text.lower() == 'about':
                bot.send_message(message.chat.id,
'''
**Introducing Akira Temp Mail**

Akira Temp mail is a temporary email address generator that can help you to do experimental works by hiding original identity.

**Is it legal or illegal ?**

In some preferences, it is legal, but even we can't refuse that you are doing cheating on internet. If you are using it for educational purposes and fair-use only, it can be considered as
legal but if you are cheating by hiding your identity, it's totally illegal.

**Benefits of this Temp Mail Bot**

You can use it to do experiments on internet by hiding your identity. Even sometimes it can be seen that you need temporary address to login for a service,
then also you need to get a temp mail. It can be seen so complicated to make a mail from temp mail generator website (even though not it is). Using bot, you just have
to click some buttons and you have your temp mail in front of you.

**Purpose of Making**

This bot was made for educational purposes made by [Akhil Parmar](https://github.com/AKH1LS) to code within an API and how it works.
Uses [1secmail.com](https://www.1secmail.com) API to generate temp mail for you..

Maintained under [Akira Project](https://telegram.dog/Akira_News).

''')
            elif message.text.lower()[14] == "[":
                email = message.text.lower()[15:message.text.lower().find("]")]
                bkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                bkeyboard.add(InlineKeyboardButton(text='Refresh inbox\n[' + str(email) + "]"))
                bkeyboard.add(InlineKeyboardButton(text='Generate email'))
                try:
                    data = requests.get(
                        "https://www.1secmail.com/api/v1/?action=getMessages&login=" + email[:email.find(
                            "@")] + "&domain=" + email[email.find("@") + 1:]).json()
                    if 'id' in data[0]:
                        for i in range(len(data)):
                            id = data[i]['id']
                            subject = data[i]['subject']
                            fromm = data[i]['from']
                            date = data[i]['date']
                            if len(subject) > 15:
                                subject = str(subject[0:15]) + "..."
                            bkeyboard.add(InlineKeyboardButton(
                                text=str(subject) + "\n from: " + fromm + " in " + "[id" + str(id) + "][" + str(
                                    email) + "]"))
                            bot.send_message(message.chat.id,
                                             "Subject: " + subject + "\n From: " + fromm + "\n Date:" + date,
                                             reply_markup=bkeyboard)
                            count = i + 1
                        bot.send_message(message.chat.id, "Here " + str(
                            count) + " message we're found\nClick on the below button to read the message\n\n If you have any query, report at @Akira_Support...")
                    else:
                        bot.send_message(message.chat.id, 'Nothing found', reply_markup=bkeyboard)
                except BaseException:
                    bot.send_message(message.chat.id, 'No messages were received...', reply_markup=bkeyboard)
            elif message.text.lower().find("[id"):
                try:
                    data = message.text.lower()[message.text.lower().find("[id"):]
                    id = data[data.find("[") + 3:data.find(']')]
                    email = data[data.find("][") + 2:-1]
                    msg = requests.get("https://www.1secmail.com/api/v1/?action=readMessage&login=" + email[:email.find(
                        "@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + id).json()
                    bot.send_message(message.chat.id,
                                     'Message ✉️\n\n   From: ' + msg['from'] + "\n   Subject: " + msg[
                                         'subject'] + "\n   Date: " + msg[
                                         'date'] + "\n   text: " + msg['textBody'])
                except BaseException:
                    pass


        bot.polling(none_stop=True, interval=1, timeout=5000)
    except BaseException:
        pass
        

