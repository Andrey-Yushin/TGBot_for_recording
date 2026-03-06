
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import (get_female_categories, get_female_items,
                               get_male_categories, get_male_items,
                               get_child_categories, get_child_items,
                               get_user_services)


admin_keys = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Услуги 🛒'),
     KeyboardButton(text='Клиенты')]
],
    resize_keyboard=True, #  Меняем размер кнопок.
    input_field_placeholder='Выберите пункт меню...'  # Подставляем placeholder.
)
