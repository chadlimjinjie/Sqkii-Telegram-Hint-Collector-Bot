'''
Author: Chad Lim Jin Jie
GitHub: https://github.com/chadlimjinjie
Made using:
gspread (Google Sheets API)
telebot (pyTelegramBotAPI)
datetime
Citations:
https://youtu.be/T1vqS1NL89E
'''
# imports
import gspread
import telebot
import datetime

bot = telebot.TeleBot('', parse_mode=None) # Your telegram bot API key
gc = gspread.service_account(filename = 'credentials.json')
sheets = gc.open_by_key('') # https://youtu.be/T1vqS1NL89E?t=250
worksheet = sheets.sheet1

#print(worksheet.get_all_records())

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.forward_from != None: # Check if forwarded message/hint is from a bot
        message_date = datetime.datetime.fromtimestamp(message.date).date()
        accepted_date = datetime.date(2020, 9 ,7) # Date which is after the previous hunt
        if message.forward_from.id == 1076402210: # Check if the hint was from @SqkiiBot
            if message_date >= accepted_date: # Check if the message/hint is not an old hint from a previous hunt
                # Check if it is a single hint or a hunt history
                if 'Here\'s an extra clue for your effort:' in message.text.split('\n')[0]:
                    bot.reply_to(message, 'Valid Hint')
                    hint = message.text.split('\n')[2]
                    hint = hint[0:-1] + hint[-1].replace(' ', '')
                    worksheet.append_row([hint])
                elif 'Hunting History' in message.text.split('\n')[0]:
                    bot.reply_to(message, 'Valid Hint')
                    for i in range(len(message.text.split('\n'))):
                        if i != 0 and i % 6 == 0:
                            hint = message.text.split('\n')[i].replace('Extra clue: ','')
                            worksheet.append_row([hint])
                            print(hint)
                else:
                    bot.reply_to(message, 'This is not a hint forward your Hunting History/Hint')
            else:
                bot.reply_to(message, 'This is a hint from a previous hunt')
        else:
            bot.reply_to(message, 'Please forward the original hint from @SqkiiBot')
    else:
        bot.reply_to(message, 'Please forward the original hint from @SqkiiBot')

bot.polling() # Start the bot
