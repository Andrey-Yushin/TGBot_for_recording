
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from settings.config import VK_LINK, YANDEX_MAPS, TWOGIS, VIDEO_LINK
from database.requests import (get_female_categories, get_female_items,
                               get_male_categories, get_male_items,
                               get_child_categories, get_child_items)

main_user_keys = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Мой профиль')],
    [KeyboardButton(text='Услуги'), KeyboardButton(text='Акции')],
    [KeyboardButton(text='Информация')],
],
    resize_keyboard=True, #  Меняем размер кнопок.
    input_field_placeholder='Выберите пункт меню...'  # Подставляем placeholder.
)

categories_user_keys = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Женские'), KeyboardButton(text='Мужские')],
    [KeyboardButton(text='Детские'), KeyboardButton(text='Общие')],
    [KeyboardButton(text='На главную')]
],
    resize_keyboard=True, #  Меняем размер кнопок.
    input_field_placeholder='Выберите для кого услуга...'  # Подставляем placeholder.
)

info_keys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Группа ВК', url=VK_LINK)],
    [InlineKeyboardButton(text='Видео как меня найти', url=VIDEO_LINK)],
    [InlineKeyboardButton(text='ЯндексКарты', url=YANDEX_MAPS),
    InlineKeyboardButton(text='2ГИС', url=TWOGIS)],
])


async def female_categories():
    all_categories = await get_female_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'female_category_{category.id}'))
    return keyboard.adjust(1).as_markup()

async def female_items(category_id):
    all_items = await get_female_items(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'female_item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_female_categories'))
    return keyboard.adjust(1).as_markup()

female_keys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записаться', callback_data='...')],
    [InlineKeyboardButton(text='Назад', callback_data='...')],
])


async def male_categories():
    all_categories = await get_male_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'male_category_{category.id}'))
    return keyboard.adjust(1).as_markup()

async def male_items(category_id):
    all_items = await get_male_items(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'male_item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_male_categories'))
    return keyboard.adjust(1).as_markup()

male_keys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записаться', callback_data='...')],
    [InlineKeyboardButton(text='Назад', callback_data='...')],
])


async def child_categories():
    all_categories = await get_child_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'child_category_{category.id}'))
    return keyboard.adjust(1).as_markup()

async def child_items(category_id):
    all_items = await get_child_items(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'child_item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_child_categories'))
    return keyboard.adjust(1).as_markup()

child_keys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записаться', callback_data='...')],
    [InlineKeyboardButton(text='Назад', callback_data='...')],
])
