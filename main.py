import telebot
import constants
import user_com
import datetime
import random
import time
bot = telebot.TeleBot(constants.token)

QIWI_text = '''Здесь вы можете пополнить баланс QIWI. 
Перечислите деньги на данный номер, и, в течение час деньги переведутся в игровую валюту
При отправке, напишите свой id и ваш уникальных код перевода
Ваш id - %s
Ваш уникальный код перевода #%s'''

Yandex_text = '''Здесь вы можете пополнить баланс ЯД. 
Перечислите деньги на данный номер, и, в течение час деньги переведутся в игровую валюту
При отправке, напишите свой id и ваш уникальных код перевода
Ваш id - %s
Ваш уникальный код перевода #%s'''

btc_text = '''Для пополнения BTC с внешнего кошелька используйте многоразовый адрес ниже.
(сумма не менее 0,001 BTC).

После чего средства поступят на ваш кошелёк после 1-го подтверждения сети'''

hello_text = '''Привет! В данном боте мы предлагаем заключить тебе пари и угадать, куда пойдёт курс Биткоина «вниз» или «вверх».

Если ты будешь прав мы начислим тебе 80% от твоей ставки. 

К примеру ты поставил 1 BTC и верно угадал направление, в таком случае мы выплатим тебе 1,8 BTC, при этом курс мог изменится даже на 1$ в нужном тебе направлении.

Период ставки можно выбирать самому, всего 6 вариантов

Удачных тебе пари
!'''

ref_text = '''Кстати, у нас действует реферальная система, а это значит, что за каждого человека, который перейдёт по твоей реферальный ссылке и пополнит баланс, мы выплатим тебе 0,0005 BTC(~3$)

Свою реферальную ссылку, ты можешь найти в разделе «Дополнительно»
'''

pary_text = '''Пари проводятся каждый день, независимо от курса. Баланс вы можете пополнить нажав на кнопку в меню. 
'''

@bot.message_handler(commands= ['start'])
def start(message):
    if str(message.text)[:6] == '/start':
        try:
            link_name = str(message.text)[7:]
        except:
            link_name = ''
        hello = user_com.registration(message.from_user.id, message.from_user.first_name, str(message.from_user.id), link_name)
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('💰Пополнить баланс', '🤝Пари')
        user_markup.row('💸Вывести средства', '💼Мой баланс')
        user_markup.row('🔥Дополнительно')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, hello_text + ref_text + pary_text + hello, reply_markup= user_markup)
        bot.register_next_step_handler(sent, introduction)

    s = user_com.o_clock()
    if s != []:
        for i in s:
            info = user_com.info(i)
            try:
                money = user_com.parse(i)
            except:
                break
            if info[8] == 'less':
                if float(money) < float(info[7]):
                    user_com.add_plus(info[0], info[6] * 1.8)
                    bot.send_message(info[0], 'Ставка прошла')
                else:
                    bot.send_message(info[0], 'Ставка не прошла')
            else:
                if money > info[7]:
                    user_com.add_plus(info[0], info[6] * 1.8)
                    bot.send_message(info[0], 'Ставка прошла')
                else:
                    bot.send_message(info[0], 'Ставка не прошла')
            user_com.null(info[0])

def introduction(message):
    if message.text == '💰Пополнить баланс':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('Bitcoin- btc', 'Etherium - eth')
        user_markup.row('QIWI - rub', 'Yd - rub')
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, ' Выберите метод пополнения⬇️', reply_markup= user_markup)
        bot.register_next_step_handler(sent, payment)

    elif message.text == '💼Мой баланс':
        bot.send_message(message.from_user.id, 'Ваш баланс ' + str(user_com.info(message.from_user.id)[2]) + ' ВТС')
        message.text = 'start'
        start_one(message)

    elif message.text == '🔥Дополнительно':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('Задать вопрос', 'Рефералы')
        user_markup.row('FAQ')
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'Выберете валюту', reply_markup=user_markup)
        bot.register_next_step_handler(sent, alse)

    elif message.text == '🤝Пари':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('BTC/USD')
        user_markup.row('ETH/USD')
        user_markup.row('XRP/USD')
        user_markup.row('BCC/USD')
        user_markup.row('EOS/USD')
        user_markup.row('LTC/USD')
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'Выберите валюту', reply_markup= user_markup)
        bot.register_next_step_handler(sent, Bitcoin_def)

    else:
        bot.send_message(message.from_user.id, '"'+message.text+'", я не знаю эту команду')
        message.text = 'start'
        start_one(message)


def Bitcoin_def(message):
    if message.text == 'BTC/USD':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        money = user_com.parse('BTC')
        constants.valume = 'BTC'
        user_markup.row('1 Час')
        user_markup.row('2 Часа')
        user_markup.row('4 Часа')
        user_markup.row('6 Часов')
        user_markup.row('12 Часов')
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'На данный момент курс: ' + str(money) + '$ за BTS. Выберете время, через сколько вы хотите, чтобы ставка сыграла',reply_markup=user_markup)
        bot.register_next_step_handler(sent, time_case)
    elif message.text == 'ETH/USD':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        money = user_com.parse('ETH')
        constants.valume = 'ETH'
        user_markup.row('1 Час')
        user_markup.row('2 Часа')
        user_markup.row('4 Часа')
        user_markup.row('6 Часов')
        user_markup.row('12 Часов')
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'На данный момент курс: ' + str(money) + '$ за ETH. Выберете время, через сколько вы хотите, чтобы ставка сыграла',reply_markup=user_markup)
        bot.register_next_step_handler(sent, time_case)
    elif message.text == 'XRP/USD':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        money = user_com.parse('XRP')
        constants.valume = 'XRP'
        user_markup.row('1 Час')
        user_markup.row('2 Часа')
        user_markup.row('4 Часа')
        user_markup.row('6 Часов')
        user_markup.row('12 Часов')
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'На данный момент курс: ' + str(money) + '$ за XRP. Выберете время, через сколько вы хотите, чтобы ставка сыграла',reply_markup=user_markup)
        bot.register_next_step_handler(sent, time_case)
    elif message.text == 'EOS/USD':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        money = user_com.parse('EOS')
        constants.valume = 'EOS'
        user_markup.row('1 Час')
        user_markup.row('2 Часа')
        user_markup.row('4 Часа')
        user_markup.row('6 Часов')
        user_markup.row('12 Часов')
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'На данный момент курс: ' + str(money) + '$ за EOS. Выберете время, через сколько вы хотите, чтобы ставка сыграла',reply_markup=user_markup)
        bot.register_next_step_handler(sent, time_case)
    elif message.text == 'LTC/USD':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        money = user_com.parse('LTC')
        constants.valume = 'LTC'
        user_markup.row('1 Час')
        user_markup.row('2 Часа')
        user_markup.row('4 Часа')
        user_markup.row('6 Часов')
        user_markup.row('12 Часов')
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'На данный момент курс: ' + str(money) + '$ за LTC. Выберете время, через сколько вы хотите, чтобы ставка сыграла',reply_markup=user_markup)
        bot.register_next_step_handler(sent, time_case)
    elif message.text == 'Назад':
        message.text = 'start'
        start_one(message)

    else:
        message.text = 'start'
        start_one(message)


def payment(message):
    if message.text == 'Bitcoin- btc':
        bot.send_message(message.from_user.id, btc_text + '\n' + str(random.choice(constants.btc_list)) )
        message.text = 'start'
        start_one(message)

    elif message.text == 'Etherium - eth':
        bot.send_message(message.from_user.id, btc_text + '\n' + str(random.choice(constants.eth_list)))
        message.text = 'start'
        start_one(message)

    elif message.text == 'Назад':
        message.text = 'start'
        start_one(message)

    else:
        message.text = 'start'
        start_one(message)


def end_pay(message):
    if message.text == 'Назад':
        message.text = 'start'
        start_one(message)

    else:
        message.text = 'start'
        start_one(message)





def time_case(message):
    if message.text == '1 Час':
        user_com.set_alarm(1, message.from_user.id)
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'Сколько ставите?', reply_markup=user_markup)
        bot.register_next_step_handler(sent, pay)
    elif message.text == '2 Часа':
        user_com.set_alarm(2, message.from_user.id)
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'Сколько ставите?', reply_markup=user_markup)
        bot.register_next_step_handler(sent, pay)
    elif message.text == '4 Часа':
        user_com.set_alarm(4, message.from_user.id)
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'Сколько ставите?', reply_markup=user_markup)
        bot.register_next_step_handler(sent, pay)
    elif message.text == '6 Часов':
        user_com.set_alarm(6, message.from_user.id)
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'Сколько ставите?', reply_markup=user_markup)
        bot.register_next_step_handler(sent, pay)
    elif message.text == '12 Часов':
        user_com.set_alarm(12, message.from_user.id)
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('Назад')
        user_markup.one_time_keyboard = True
        sent = bot.send_message(message.from_user.id, 'Сколько ставите?', reply_markup=user_markup)
        bot.register_next_step_handler(sent, pay)
    else:
        message.text = 'start'
        start_one(message)


def pay(message):
    if message.text == 'Назад':
        message.text = 'start'
        start_one(message)

    else:
        try:
            q = float(message.text)
            if  q <= user_com.info(message.from_user.id)[2]:
                user_com.add_plus(message.from_user.id, -q)
                user_com.pay(message.from_user.id, q)
                user_markup = telebot.types.ReplyKeyboardMarkup(True)
                user_markup.row('Больше', 'Меньше')
                user_markup.one_time_keyboard = True
                sent = bot.send_message(message.from_user.id, 'Ставка принята' , reply_markup=user_markup)
                bot.register_next_step_handler(sent, pay_l)
            else:
                bot.send_message(message.from_user.id, 'Не хватает денег')
                message.text = 'start'
                start_one(message)

        except:
            bot.send_message(message.from_user.id, 'Что-то пошло не так, попробуйте еще раз..')
            message.text = 'start'
            start_one(message)


def pay_l(message):
    if message.text == 'Больше':
        money = float(user_com.parse(constants.valume))
        write = user_com.more_less(message.from_user.id, 'more', money, constants.valume)
        bot.send_message(message.from_user.id, 'Посмотрим, что будет в '+ str(write[0]))
    elif message.text == 'Меньше':
        money = float(user_com.parse(constants.valume))
        write = user_com.more_less(message.from_user.id, 'less', money, constants.valume)
        bot.send_message(message.from_user.id, 'Посмотрим, что будет в ' + str(write[0]))
    message.text = 'start'
    start_one(message)


def alse(message):
    if message.text == 'Задать вопрос':
        sent  = bot.send_message(message.from_user.id, 'Пожалуйста, введите ваш вопрос.')
        bot.register_next_step_handler(sent, question)
    elif message.text == 'Рефералы':
        info = user_com.info(message.from_user.id)
        bot.send_message(message.from_user.id, 'За каждого приведенного реферала, который пополнит баланс, вам начислится 0,0005 BTC \n Это ваша реферальная ссылка: http://t.me/testbitcoinkifirbot?start=' + str(info[3]) + ' . \n Ваши рефералы: ' + str(info[5]))
        message.text = 'start'
        start_one(message)

    else:
        bot.send_message(message.from_user.id, '"' + message.text + '", я не знаю эту команду')
        message.text = 'start'
        start_one(message)


def question(mesaage):
    bot.send_message(constants.admin, mesaage.text + ' id:' + str(mesaage.from_user.id) + ' Имя:' + str(mesaage.from_user.first_name))
    bot.send_message(mesaage.from_user.id, 'Спасибо, в ближайшее время с вами свяжется наш оператор по Вашему вопросу')
    mesaage.text = 'start'
    start_one(mesaage)


def admin_in(message):
    if message.text == 'Закинуть деньги':
        sent = bot.send_message(message.from_user.id, 'Какую сумму вы хотите закинуть? и какой id у пользователя?')
        bot.register_next_step_handler(sent, admin_add)

    elif message.text == 'Прибавть деньги игроку':
        sent = bot.send_message(message.from_user.id, 'На сколько вы хотите увеличить счет игрока? и какой id у пользователя?')
        bot.register_next_step_handler(sent, admin_add_plus)
    elif message.text == 'Прибавть деньги игроку':
        message.text = 'start'
        start_one(message)

    else:
        bot.send_message(message.from_user.id, '"' + message.text + '", я не знаю эту команду')
        message.text = 'start'
        start_one(message)


def admin_add(message):
    try:
        text = message.text.split()
        user_com.add(text[1], text[0])
        bot.send_message(message.from_user.id, 'Спасибо, деньги в игре')
        message.text = 'start'
        start_one(message)

    except:
        bot.send_message(message.from_user.id, 'Неверный формат')
        message.text = 'start'
        start_one(message)


def admin_add_plus(message):
    try:
        text = message.text.split()
        user_com.add_plus(int(text[1]), int(text[0]))
        bot.send_message(message.from_user.id, 'Спасибо, деньги в игре')
        message.text = 'start'
        start_one(message)

    except:
        bot.send_message(message.from_user.id, 'Неверный формат')
        message.text = 'start'
        start_one(message)


def start_one(message):
    s = user_com.o_clock()
    if s != []:
        for i in s:
            info = user_com.info(i)
            try:
                money = user_com.parse(i)
            except:
                break
            if info[8] == 'less':
                if float(money) < float(info[7]):
                    user_com.add_plus(info[0], info[6] * 1.8)
                    bot.send_message(info[0], 'Ставка прошла')
                else:
                    bot.send_message(info[0], 'Ставка не прошла')
            else:
                if money > info[7]:
                    user_com.add_plus(info[0], info[6] * 1.8)
                    bot.send_message(info[0], 'Ставка прошла')
                else:
                    bot.send_message(info[0], 'Ставка не прошла')
            user_com.null(info[0])

    time_now()

    if message.text == 'start':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row('💰Пополнить баланс', '🤝Пари')
        user_markup.row('💸Вывести средства', '💼Мой баланс')
        user_markup.row('🔥Дополнительно')
        sent = bot.send_message(message.from_user.id, 'Чем еще могу помочь?' ,reply_markup=user_markup)
        telebot.types.ReplyKeyboardMarkup(False)
        bot.register_next_step_handler(sent, introduction)
    else:
        introduction(message)


def time_now():
    for i in constants.time:
        if  str(datetime.datetime.today().time())[2:5] == i:
            id_ = user_com.all_id()
            for j in id_:
                try:
                    bot.send_message(j, 'Самое время делать ствки!')
                except:
                    pass

bot.polling(none_stop=True , timeout=30 )


