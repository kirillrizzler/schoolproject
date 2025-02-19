import telebot
import json
from datetime import datetime
def get_state(user_id):
    f = open('statements.json', "r")
    user_id = str(user_id)
    # Reading from file
    data = json.loads(f.read())
    print(data)
    if user_id in data:
        return data[user_id]
    else:
        return None
def get_all_reports():
    f = open('reports.json', "r")
    data = json.loads(f.read())
    reports_normal = []
    for key in data:
        reports_normal.append(data[key])
    s = "\n"
    for i in range(len(reports_normal)):
        for el in reports_normal[i]:
            if el[3] == 1:
                s += str(el[0]) + ' ' + str(el[1]) + " " + str(el[2]) + '\n'
    return s
def delete_reports(message_text):
    f = open('reports.json', "r")
    data = json.loads(f.read())
    f.close()
    print(data)
    Ids = [int(i) for i in message_text.split()]
    for i in data:
        for j in data[i]:
            print("report j == ", j)
            if j[0] in Ids:
                j[3] = 0
    data_d = json.dumps(data)
    with open("reports.json", "w") as my_file:
        print(data_d)
        my_file.write(data_d)
    print(data)
    print("Ids == ", Ids)
    print(Ids)
def get_max_id():
    f = open('reports.json', "r")
    data = json.loads(f.read())
    reports_normal = []
    max_id = 0
    for key in data:
        reports_normal.append(data[key])
    print('PIDOROK')
    print(reports_normal)
    for i in range(len(reports_normal)):
        for el in reports_normal[i]:
            max_id = max(max_id,el[0])
            print(el)
    return max_id + 1
def processing_report(report_text, report_date, user_id, type):
    f = open('reports.json', "r")
    data = json.loads(f.read())
    user_id = str(user_id)
    if user_id in data:
        data[user_id].append([get_max_id(),report_date,report_text,1, type])
    else:
        data[user_id] = [[get_max_id(),report_date,report_text,1, type]]
    f.close()
    print("data ==",data)
    data_d = json.dumps(data)

    with open("reports.json", "w") as my_file:
        print(data_d)
        my_file.write(data_d)
def report_iscorrect(reporttext):
    if len(reporttext) > 7 and reporttext.count("хуй") == 0 and reporttext.count("гандон") == 0 and reporttext.count("пизда") == 0 and reporttext.count("шлюха") == 0 and reporttext.count("сучка") == 0and reporttext.count("долбоеб") == 0 and reporttext.count("хуесос") == 0 and reporttext.count("хуйло") == 0 and reporttext.count("пидор") == 0 and reporttext.count("пидорас") == 0 and reporttext.count("пизда") == 0:
        return True
    else:
        return False


def update_state(user_id, new_state):
    f = open('statements.json', "r")
    data = json.loads(f.read())
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = new_state
    else:
        data[user_id] = new_state
    f.close()
    print(data)
    data_d = json.dumps(data)

    with open("statements.json", "w") as my_file:
        print(data_d)
        my_file.write(data_d)


# Создаем экземпляр бота
bot = telebot.TeleBot('6900227471:AAE-FTu6635wK2YB4sAEo3Q4pb10DCVbnGk')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    print(get_state(message.from_user.id))
    bot.reply_to(message, 'Приветствую, что вас интересует?')
    update_state(message.from_user.id, 'start')
@bot.message_handler(commands=['all_reports'])
def all_reports(message):
    state = get_state(message.from_user.id)
    print(state)
    if state != 'authorized' and state != 'delete_report':
        bot.reply_to(message, 'У вас нет прав доступа')
    else:
        reports = get_all_reports()
        if reports != '\n':
            bot.reply_to(message, f"список жалоб: {str(reports)}")
        else:
            bot.reply_to(message,"На данный момент активных жалоб нет")


@bot.message_handler(commands=['my_reports'])
def my_reports(message):
    bot.reply_to(message, 'Вот список твоих жалоб:')
    update_state(message.from_user.id, 'my_reports')
@bot.message_handler(commands=['send_personal_report'])
def send_personal_report(message):
    bot.reply_to(message, 'Выберите номер преподавателя, которому вы хотите отправить сообщение:\n 1) Александр Маркович \n 2)Анна Николаевна')
    update_state(message.from_user.id, 'send_personal_report')
@bot.message_handler(commands=['delete_report'])
def delete_report(message):
    state = get_state(message.from_user.id)
    if state != 'authorized' and state != 'delete_report':
        bot.reply_to(message, 'У вас нет доступа к этой команде')
    else:
        bot.reply_to(message, 'Введите id жалобы, которую вы хотите удалить:')
        update_state(message.from_user.id, 'delete_report')
@bot.message_handler(commands=['send_report'])
def send_report(message):
    bot.reply_to(message, 'Введите жалобу')
    update_state(message.from_user.id, 'send_report')
@bot.message_handler(commands=['auth'])
def auth(message):
    bot.reply_to(message, 'Если у вас особые права доступа, введите пароль:')
    update_state(message.from_user.id, 'auth')
# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    print(dir(message))


    state = get_state(message.from_user.id)
    current_date = datetime.now().date()
    print(current_date)
    print(state)
    if state == 'send_personal_report':
        pass
    elif state == 'send_report':
        if report_iscorrect(message.text):
            bot.reply_to(message, 'Ваша жалоба принята')
            processing_report(message.text,str(current_date), message.from_user.id, 'common')
            update_state(message.from_user.id,'report_received')
        else:
            bot.reply_to(message, 'К сожалению, Ваша жалоба не может быть принята. Возможные причины: \n 1) Меньше 7 символов в тексте жалобы (подозрение на спам) \n 2) Использование обсценной лексики \n 3) Оскорбления \n Попробуйте отправить жалобу снова')
    elif state == 'delete_report':
        delete_reports(message.text)
        bot.reply_to(message, 'Жалоба успешно удалена!')
    elif state == 'auth':
        if message.text == 'umshdirectorpam':
            update_state(message.from_user.id, 'authorized')
            bot.reply_to(message,
                         f"{message.from_user.first_name}, Вам доступны следующие команды:\n all_reports — посмотреть все жалобы\n delete_report — удалить жалобу ")

        else:
            bot.reply_to(message, f"Неверный пароль, {message.from_user.first_name}, попробуйте снова")
    else:
        bot.reply_to(message,'Неизвестная команда, попробуйте снова')


#    print('State ==', State)
# Запускаем бота
bot.polling()
