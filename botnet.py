import telebot
from telebot import TeleBot
from telethon import TelegramClient
from telethon.tl.functions.channels import ReportSpam
import re

API_ID = 'apiid' #Апи айди
API_HASH = 'api hash' #апи хеш
BOT_TOKEN = 'BotToken' #вставь токен бота которого получил в Botfahter

bot = TeleBot(BOT_TOKEN)




# Список сессий
sessions = [
    ('session_name1', 'phone_number1'),  # Замените на ваши данные
    ('session_name2', 'phone_number2'),
    # Добавляйте дополнительные сессии по мере необходимости
]

clients = [TelegramClient(session_name, API_ID, API_HASH) for session_name, _ in sessions]

@bot.message_handler(commands=['snos'])
def handle_snos(message):
    link = message.text.split()[1] if len(message.text.split()) > 1 else None
    if link:
        bot.send_message(message.chat.id, "Обработка ссылки...")
        for session_name, phone in sessions:
            client = next(client for client in clients if client.session.session_name == session_name)
            client.loop.run_until_complete(report_message(link, message.chat.id, client))
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите ссылку.")

async def report_message(link, chat_id, client):
    match = re.search(r't.me/(.+)/(\d+)', link)
    if not match:
        bot.send_message(chat_id, "Неверная ссылка.")
        return

    chat_username = match.group(1)
    message_id = int(match.group(2))

    await client.start()
    async with client:
        chat = await client.get_entity(chat_username)
        await client(ReportSpam(chat))
        bot.send_message(chat_id, f"Жалоба на сообщение отправлена с сессии {client.session.session_name}.")


if __name__ == "__main__":
    for client in clients:
        client.start()
    bot.polling()
