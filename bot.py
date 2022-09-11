import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

print('Я запустила py-скрипт с моим telegram bot')

logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s:: process %(process)d: %(levelname)s: %(name)s: %(message)s'    
    )

# # Настройки прокси
# PROXY = {
#     'proxy_url': settings.PROXY_URL,
#     'urllib3_proxy_kwargs': {
#         'username': settings.PROXY_USERNAME, 
#         'password': settings.PROXY_PASSWORD
#         }
#     }


def greer_user(update,context):
    # вывели в консоль программы сообщение
    print('Пользователь нажал /start: ')
    print(update['message']['date'])
    print(update['message']['chat'])
    # print('Пользователь нажал /start: '+update['message']['date']+': '+update['message']['chat'])

    # вывели сообщение пользователю в telegram-чат
    update.message.reply_text('Привет!!! Вы запустили мой телеграмм ботик!!!! \nКак тебя зовут?')


def talk_with_me (update, context):
    text_from_user = update.message.text
    text_to_user = text_from_user
    print(text_to_user)
    update.message.reply_text(
        'Привет, '+text_to_user+'!!!'
        +'\nА меня зовут ТэБоттик :)'
        +'\nПока это все что я умею...'
        )

# здесь будет лежать тело бота
def main():
    # авторизовали бота на сервере телеграм
    mybot = Updater(
        settings.API_KEY, 
        use_context=True
        # request_kwargs=PROXY
    )

    # настраиваем диспетчера:
    mybot.dispatcher.add_handler(CommandHandler('start', greer_user))
    mybot.dispatcher.add_handler(MessageHandler(Filters.text, talk_with_me))

    logging.info('telegram bot starting')
    # заставили бота запрашивать с сервера телеграмма все входящие в него сообщения
    mybot.start_polling()
    # бот остановится, когда мы его попросим остановится
    mybot.idle()


if __name__ == "__main__":
    main()