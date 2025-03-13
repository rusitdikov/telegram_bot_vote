import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

#⛔️ вставь токен тут:
bot = telebot.TeleBot(7906336905:AAEG1wlCl2C7HElzttpVJ-kbnM1GT32lPFs)

#⛔️ тут сам канал (для проверки подписки):
CHANNEL_ID = @rso_official

votes = {}

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'creator', 'administrator']
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Бот для подписчиков канала.\nВведи /vote, чтобы голосовать!')

@bot.message_handler(commands=['vote'])
def vote(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f'❌ сперва подпишись на канал: {CHANNEL_ID}')
        return

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Конкурсант 1 🔥", callback_data='contestant_1'))
    markup.add(InlineKeyboardButton("Конкурсант 2 💎", callback_data='contestant_2'))
    markup.add(InlineKeyboardButton("Конкурсант 3 🚀", callback_data='contestant_3'))

    bot.send_message(message.chat.id, "Выбирай фаворита:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('contestant_'))
def query_vote(call):
    if not is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, '❌ Ты не подписан на канал!', show_alert=True)
        return

    if call.from_user.id in votes:
        bot.answer_callback_query(call.id, '⚠️ Ты уже голосовал!', show_alert=True)
        return

    votes[call.from_user.id] = call.data
    bot.answer_callback_query(call.id, '✅ Твой голос засчитан!', show_alert=True)

bot.infinity_polling()
