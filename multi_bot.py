import telebot
from covid import Covid
from telebot import types
from bs4 import BeautifulSoup
import requests

#info about covid
covid = Covid()

#token
bot = telebot.TeleBot('token')

#start message
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hello, user')

#covid message
@bot.message_handler(commands=['covid'])
def start1(message):
    bot.send_message(message.chat.id, 'choose a country', reply_markup=markup)


#link message
@bot.message_handler(commands=['link'])
def messages1(message):
        bot.send_message(message.chat.id, 'insert a link')
        bot.register_next_step_handler(message, reg_name)
        bot.register_next_step_handler(message, parse)



def reg_name(message):
    global name
    name = message.text


#index message
@bot.message_handler(commands=['index'])
def mass(message):
    bot.send_message(message.chat.id, 'Insert your data')
    bot.send_message(message.chat.id, 'Your weight (kg):')
    bot.register_next_step_handler(message, reg_weight)



def reg_weight(message):
    global weight1
    weight1 = message.text
    bot.send_message(message.chat.id, 'Your height (cm):')
    bot.register_next_step_handler(message, reg_height)

def reg_height(message):
    global height1
    height1 = message.text
    try:
        height2 = float(height1.replace(',', '.')) / 100
        index = float(weight1.replace(',', '.')) / (float(height2) ** 2)
        index = round(index, 2)
        if index < 16:
            a = 'Острый дефицит массы'
        elif 16 <= index <= 18.5  :
            a = 'Недостаточная масса тела'
        elif 18.6 <=index <=25:
            a = 'Норма'
        elif 25.1 <= index <= 30:
            a = 'Избыточная масса тела'
        elif 30.1 <= index <= 35:
            a = 'Ожирение первой степени'
        elif 35.1 <= index <= 40:
            a = 'Ожирение второй степени'
        elif index > 40.1:
            a = 'ООжирение третьей степени'
        bot.send_message(message.chat.id, 'Your weight (kg): ' + weight1.replace(',', '.') + '\n' + 'Your height (cm): ' + str(height1.replace(',', '.')) + '\n' + str(index) + ' ' + a +
                         '\n' + '' '\n' + 'Острый дефицит массы < 16' + '\n' + 'Недостаточная масса тела 16 - 18.5' + '\n' + 'Норма 18.6 - 25'  + '\n' + 'Избыточная масса тела 25.1 - 30' +
                         '\n' + 'Ожирение первой степени 30.1 - 35' + '\n' + 'Ожирение второй степени	35.1 - 40' + '\n' + 'Ожирение третьей степени > 40.1')
    except:
        bot.send_message(message.chat.id, 'Error: Please input correct data')
#parser
def parse(message):
    HEADERS1 = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.310'}
    response1 = requests.get(name, headers=HEADERS1)
    soup1 = BeautifulSoup(response1.content, 'html.parser')
    items1 = soup1.findAll('div', class_='col-1-1 bg-white extra-offers-offer')
    comps1 = []
    for item in items1:
        comps1.append({
            'shop': item.find('a', 'regular-link').get_text().upper(),
            'price': item.find('p',
                               'bold roboto red text-24 extra-offers-price nomargin curr_change').get_text().replace(
                u'\xa0', ''),
            'link': item.find('a', 'btn blue-bg white rounded roboto bold').get('href')
        })
    for title in comps1:
        bot.send_message(message.chat.id, title['shop'] + ' - ' + title['price'] + '  ' + title['link'], disable_web_page_preview=True)


#flags
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
world = types.KeyboardButton('🌎')
est = types.KeyboardButton('🇪🇪')
rus = types.KeyboardButton('🇷🇺')
fin = types.KeyboardButton('🇫🇮')
lv = types.KeyboardButton('🇱🇻') #97
usa = types.KeyboardButton('🇺🇸') #177
fr = types.KeyboardButton('🇫🇷')#63
es = types.KeyboardButton('🇪🇸')#161
it = types.KeyboardButton('🇮🇹')#86
uk = types.KeyboardButton('🇬🇧')#181
de = types.KeyboardButton('🇩🇪')#67
lt = types.KeyboardButton('🇱🇹')
markup.add(world, est, rus, fin, lv, usa, fr, es, it, uk, de, lt)




def cov(id, x, message):
    covid = Covid()
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.310'}
    response = requests.get(x, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='info_blk stat_block confirmed')
    comps = []
    location = covid.get_status_by_country_id(id)
    try:
        for item in items:
            comps.append({
                'cases': item.find('sup').get_text()
            })
        for title in comps:
            a = (title['cases'])



        bot.send_message(message.chat.id, str(location['country']) + '\n' + "Confirmed: " + str(
            location['confirmed']) + '\n' + 'Active: '
                         + str(location['active']) + '\n' + 'Recovered: ' + str(
            location['recovered']) + '\n' + 'Deaths: ' + str(
            location['deaths']) + '\n' + 'New cases: ' + a)
    except AttributeError:
        bot.send_message(message.chat.id, str(location['country']) + '\n' + "Confirmed: " + str(
            location['confirmed']) + '\n' + 'Active: '
                         + str(location['active']) + '\n' + 'Recovered: ' + str(
            location['recovered']) + '\n' + 'Deaths: ' + str(
            location['deaths']) + '\n' + 'New cases: ' + 'no data yet')




#flag function
@bot.message_handler(content_types=['text'])
def messages(message):
    if message.text == '🌎':
        active = covid.get_total_active_cases()
        confirmed = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()

        bot.send_message(message.chat.id, 'World:' + '\n' + "Confirmed: " + str(confirmed) + '\n' + 'Active: '
                         + str(active) + '\n' + 'Recovered: ' + str(recovered) + '\n' + 'Deaths: ' + str(
            deaths) + '\n')

    elif message.text == '🇪🇪':
        cov(58, 'https://coronavirus-monitor.info/country/estonia/', message)

    elif message.text == '🇱🇹':
        cov(103, 'https://coronavirus-monitor.info/country/lithuania/', message)

    elif message.text.lower() == 'lithuania':
        cov(103, 'https://coronavirus-monitor.info/country/lithuania/', message)

    elif message.text == '🇷🇺':
        cov(142, 'https://coronavirus-monitor.info/country/russia/', message)

    elif message.text == '🇫🇮':
        cov(62, 'https://coronavirus-monitor.info/country/finland/', message)

    elif message.text == '🇱🇻':
        cov(97, 'https://coronavirus-monitor.info/country/latvia/', message)

    elif message.text == '🇺🇸':
       cov(178, 'https://coronavirus-monitor.info/country/usa/', message)

    elif message.text == '🇫🇷':
       cov(63, 'https://coronavirus-monitor.info/country/france/', message)

    elif message.text == '🇪🇸':
        cov(162, 'https://coronavirus-monitor.info/country/spain/', message)

    elif message.text == '🇮🇹':
        cov(86, 'https://coronavirus-monitor.info/country/italy/', message)

    elif message.text == '🇬🇧':
        cov(182, 'https://coronavirus-monitor.info/country/uk/', message)

    elif message.text == '🇩🇪':
        cov(67, 'https://coronavirus-monitor.info/country/germany/', message)

    elif message.text.lower() == 'world':

        active = covid.get_total_active_cases()
        confirmed = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()

        bot.send_message(message.chat.id, 'World:' + '\n' + "Confirmed: " + str(confirmed) + '\n' + 'Active: '
                             + str(active) + '\n' + 'Recovered: ' + str(recovered) + '\n' + 'Deaths: ' + str(
                deaths) + '\n')


    elif message.text.lower() == 'estonia':
        cov(58, 'https://coronavirus-monitor.info/country/estonia/', message)

    elif message.text.lower() == 'russia':
        cov(142, 'https://coronavirus-monitor.info/country/russia/', message)

    elif message.text.lower() == 'finland':
        cov(62, 'https://coronavirus-monitor.info/country/finland/', message)

    elif message.text.lower() == 'latvia':
        cov(97, 'https://coronavirus-monitor.info/country/latvia/', message)

    elif message.text.lower() == 'usa':
        cov(178, 'https://coronavirus-monitor.info/country/usa/', message)

    elif message.text.lower() == 'france':
        cov(63, 'https://coronavirus-monitor.info/country/france/', message)

    elif message.text.lower() == 'spain':
        cov(162, 'https://coronavirus-monitor.info/country/spain/', message)

    elif message.text.lower() == 'italy':
        cov(86, 'https://coronavirus-monitor.info/country/italy/', message)

    elif message.text.lower() == 'united kingdom':
        cov(182, 'https://coronavirus-monitor.info/country/uk/', message)

    elif message.text.lower() == 'germany':
        cov(67, 'https://coronavirus-monitor.info/country/germany/', message)




#mass index


#start bot
if  __name__ == '__main__':
    bot.polling(none_stop=True)







