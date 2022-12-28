from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


but_menu = KeyboardButton('Мои запросы')
only_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_menu)
