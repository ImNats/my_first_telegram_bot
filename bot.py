from codeop import CommandCompiler
import logging
import ephem
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


def user_in_log(update,context,command_name):
    # вывели в консоль программы сообщение
    print(f'Пользователь нажал /{command_name}: ')
    print(update['message']['date'])
    print(update['message']['chat'])


def greer_user(update,context):
    # вывели в консоль программы сообщение
    command_name = 'start'
    user_in_log(update,context,command_name)

    # вывели сообщение пользователю в telegram-чат
    update.message.reply_text(
        'Привет!!!'
        + '\nА меня зовут ТэБоттик :)'
        + '\nВы запустили мой телеграмм ботик!!!!'
        # + '\nКак тебя зовут?'
    )

def goodbye_user(update,context):
    # вывели в консоль программы сообщение
    command_name = 'exit'
    user_in_log(update,context,command_name)

    # вывели сообщение пользователю в telegram-чат
    update.message.reply_text(
        'Пока!!!'
        +'\nПриходи поболтаем еще :)'
    )


def describe_my_skill(update,context):
    # вывели в консоль программы сообщение
    command_name = 'my_skills'
    user_in_log(update,context,command_name)

    # вывели сообщение пользователю в telegram-чат
    update.message.reply_text(
        'Я умею пока не много: '
        +'\n  * здороваться :)'
        +'\n  * Могу угадать в каком созвездии была планета '
        +'\n  * попробовать тебе ответить на вопрос '
        +'\n  * повторять слова '
        +'\n  * говорить пока :('
    )


def what_do_next(update, context):
    if find_planet(update, context) is not None:
        text_to_user = find_planet(update, context)
    elif ask_me(update, context) is not None:
        text_to_user = ask_me(update, context) 
    elif talk_with_me_echo(update, context) is not None:
        text_to_user = talk_with_me_echo(update, context)
    update.message.reply_text(text_to_user)


def ask_planet(update, context):
    text = '''Классно!!! Расположение какой планеты ты хочешь узнать? 
    Вот какие планеты я знаю: <code>
        Меркурий | Mercury
        Венера   | Venus
        Марс     | Mars
        Юпитер   | Jupiter
        Сатурн   | Saturn
        Уран     | Uranus
        Нептун   | Neptune
        Плутон   | Pluto
        Солнце   | Sun
        Луна     | Moon </code>
    Введи в ответ название планеты: '''
    update.message.reply_text(text, parse_mode='HTML')


def find_planet(update, context):
    user_planet = update.message.text
    planet_not_found = False

    if user_planet in {'Mercury','Меркурий'}:
        planet_id=ephem.Mercury('2022/09/19')
    elif user_planet in {'Venus','Венера'}:
        planet_id=ephem.Venus('2022/09/19')
    elif user_planet in {'Mars','Марс'}:
        planet_id=ephem.Mars('2022/09/19')
    elif user_planet in {'Jupiter','Юпитер'}:
        planet_id=ephem.Jupiter('2022/09/19')
    elif user_planet in {'Saturn','Сатурн'}:
        planet_id=ephem.Saturn('2022/09/19')
    elif user_planet in {'Uranus','Уран'}:
        planet_id=ephem.Uranus('2022/09/19')
    elif user_planet in {'Neptune','Нептун'}:
        planet_id=ephem.Neptune('2022/09/19')
    elif user_planet in {'Pluto','Плутон'}:
        planet_id=ephem.Pluto('2022/09/19')
    elif user_planet in {'Sun','Солнце'}:
        planet_id=ephem.Sun('2022/09/19')
    elif user_planet in {'Moon','Луна'}:
        planet_id=ephem.Moon('2022/09/19')
    else:
        planet_not_found = True
    
    if planet_not_found:
        text_to_user = None
    else:
        text_to_user = 'Она была в созвездии '+ephem.constellation(planet_id)[1]
    
    return text_to_user


questions_and_answers = {
    'Привет': 'Привет!',
    'Привет!': 'Привет!',
    'Пока': 'Пока!',
    'Пока!': 'Пока!',
    'Как дела?': 'Хорошо!',
    'Как жизнь?': 'Хорошо!',
    'Что делаешь?': 'Программирую',
    'Какая завтра погода?': 'Дождливая :(',
    'Что ты умеешь?': 'Отвечать на вопросы!',
    'Что умеешь?': 'Отвечать на вопросы!',
    'Завтра будет гроза?': 'Сейчас не май, не будет!',
    'Как провел лето?': 'Валялся на пляже!'
}


def ask_me(update, context):
    text_from_user = update.message.text
    if questions_and_answers.get(text_from_user) is not None:
        print(text_from_user)
        text_to_user = questions_and_answers[text_from_user]
        return text_to_user


def talk_with_me_echo(update, context):
    text_from_user = update.message.text
    text_to_user = text_from_user
    print(text_to_user)
    text_to_user = 'Я знаю ты сказал: ' + text_to_user + '!!!' + '\nОткрой меню и я расскажу, чему еще я научилась'
    return text_to_user

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
    mybot.dispatcher.add_handler(CommandHandler('exit', goodbye_user))
    mybot.dispatcher.add_handler(CommandHandler('my_skills', describe_my_skill))
    mybot.dispatcher.add_handler(CommandHandler('ask_planet', ask_planet))

    mybot.dispatcher.add_handler(MessageHandler(Filters.text, what_do_next))


    logging.info('telegram bot starting')
    # заставили бота запрашивать с сервера телеграмма все входящие в него сообщения
    mybot.start_polling()
    # бот остановится, когда мы его попросим остановится
    mybot.idle()


if __name__ == "__main__":
    main()