import telebot
import json
import os

# Создаём экземпляр бота
bot = telebot.TeleBot('7331481429:AAG9NA11OFHddox7s3c8mfSqxm8GXCxkeAc')

# Файл для хранения данных
DATA_FILE = "data.json"

# Функция для загрузки данных из файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Функция для сохранения данных в файл
def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(commands, file)

# Загружаем данные при старте
commands = load_data()

@bot.message_handler(commands=['start', 'help'])
# Функция приветствия и помощи
def start_help(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для тегания людей из команд.\n"
        "Доступные команды:\n"
        "/add_team [имя команды] [@участник1 @участник2 ...] - Добавить команду\n"
        "/delete_team [имя команды] - Удалить команду\n"
        "/tag [имя команды] - Упомянуть всех участников команды\n"
        "/list_teams - Показать все команды"
    )

# Добавление команд
@bot.message_handler(commands=['add_team'])
def add_team(message):
    try:
        # Получаем текст команды
        text = message.text.split(maxsplit=2)
        if len(text) < 3:
            bot.reply_to(message, "Использование: /add_team [имя команды] [@участник1 @участник2 ...]")
            return

        team_name, members = text[1], text[2].split()
        commands[team_name] = members
        save_data()
        bot.reply_to(message, f"Команда {team_name} добавлена с участниками: {', '.join(members)}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

#Удаление команд
@bot.message_handler(commands=['delete_team'])
def delete_team(message):
    try:
        # Получаем текст команды
        text = message.text.split(maxsplit=1)
        if len(text) < 2:
            bot.reply_to(message, "Использование: /delete_team [имя команды]")
            return

        team_name = text[1]
        if team_name in commands:
            del commands[team_name]
            save_data()
            bot.reply_to(message, f"Команда {team_name} удалена.")
        else:
            bot.reply_to(message, f"Команда {team_name} не найдена.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

#Тэг команды
@bot.message_handler(commands=['tag'])
def tag_team(message):
    try:
        # Разделяем команду на части
        text = message.text.split(maxsplit=2)
        if len(text) < 2:
            bot.reply_to(message, "Использование: /tag [имя команды] [сообщение]")
            return

        team_name = text[1]
        custom_message = text[2] if len(text) > 2 else "Привет, команда!"

        if team_name in commands:
            members = commands[team_name]
            bot.reply_to(message, f"Упоминаю команду {team_name}: {' '.join(members)}\nСообщение: {custom_message}")
        else:
            bot.reply_to(message, f"Команда {team_name} не найдена.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

#Список команд
#Тут также выводятся и участники команд
@bot.message_handler(commands=['list_teams'])
def list_teams(message):
    if commands:  # Проверяем, есть ли команды в словаре
        response = "Список команд:\n"
        for team, members in commands.items():
            response += f"Команда {team}: {', '.join(members)}\n"
    else:
        response = "Список команд пуст."
    bot.reply_to(message, response)

# Запускаем бота
bot.infinity_polling()
