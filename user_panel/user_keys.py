
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from settings.config import VK_LINK, YANDEX_MAPS, TWOGIS, VIDEO_LINK
from database.requests import (get_female_categories, get_female_items,
                               get_male_categories, get_male_items,
                               get_child_categories, get_child_items,
                               get_user_services)

main_user_keys = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Акции 🎁'),
     KeyboardButton(text='Услуги 🛒')],
    [KeyboardButton(text='Информация ℹ️'),
     KeyboardButton(text='Мой профиль 👤')],
],
    resize_keyboard=True, #  Меняем размер кнопок.
    input_field_placeholder='Выберите пункт меню...'  # Подставляем placeholder.
)

categories_user_keys = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Женские 💇‍♀️'),
     KeyboardButton(text='Мужские 💇‍♂️'),
     KeyboardButton(text='Детские 👶')],
    [KeyboardButton(text='На главную ↪️'),
     KeyboardButton(text='Мои услуги 📋')]
],
    resize_keyboard=True, #  Меняем размер кнопок.
    input_field_placeholder='Выберите для кого услуга...'  # Подставляем placeholder.
)

info_keys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Группа ВКонтакте 📱', url=VK_LINK)],
    [InlineKeyboardButton(text='Видео как меня найти 📸', url=VIDEO_LINK)],
    [InlineKeyboardButton(text='ЯндексКарты 🗺', url=YANDEX_MAPS),
    InlineKeyboardButton(text='2ГИС 🗺', url=TWOGIS)],
])


reg_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Регистрация',
                          callback_data='reg_usr')],
    [InlineKeyboardButton(text='Удалить профиль',
                          callback_data='delete_user')],
])


profile_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить имя',
                          callback_data='change_name')],
    [InlineKeyboardButton(text='Изменить номер',
                          callback_data='change_phone')],
    [InlineKeyboardButton(text='Удалить профиль',
                          callback_data='delete_user')],
])

# Кнопка запуска бота, после удаления профиля.
start_btn = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Запустить бота')]
],
    resize_keyboard=True, #  Меняем размер кнопок.
)

comment_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Без комментария',
                          callback_data='skip_comment')],
    [InlineKeyboardButton(text='Отменить запись',
                          callback_data='service_cancle')]
])


async def service_btn(service_id):
    """Выводи кнопки списка услуг."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад',
                            callback_data='service_list'))
    keyboard.add(InlineKeyboardButton(text='Удалить',
                            callback_data=f'delete_service_{service_id}'))
    keyboard.add(InlineKeyboardButton(text='Изменить комментарий',
                            callback_data='change_service_comment'))

    return keyboard.adjust(2, 1).as_markup()


async def user_services(tg_id):
    """Выводит услуги клиента."""
    all_services = await get_user_services(tg_id)
    keyboard = InlineKeyboardBuilder()
    for service in all_services:
        keyboard.add(InlineKeyboardButton(text=service.service_item,
                            callback_data=f'services_{service.id}'))
    return keyboard.adjust(1).as_markup()


async def female_categories():
    """Выводит кнопки женских категорий."""
    all_categories = await get_female_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                            callback_data=f'female_category_{category.id}'))
    return keyboard.adjust(1).as_markup()


async def female_items(category_id):
    """Выводит женские услуги."""
    all_items = await get_female_items(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name,
                                callback_data=f'female_item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад ↪️',
                                callback_data='to_female_categories'))
    return keyboard.adjust(1).as_markup()


async def item_info(gender, item_id):
    """Выводи кнопки записи."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Записаться ✏️",
                                callback_data=f'record_{gender}_{item_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад ↪️',
                                callback_data='to_female_categories'))
    return keyboard.adjust(1).as_markup()


async def male_categories():
    all_categories = await get_male_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                                callback_data=f'male_category_{category.id}'))
    return keyboard.adjust(1).as_markup()


async def male_items(category_id):
    all_items = await get_male_items(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name,
                                callback_data=f'male_item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад ↪️',
                                callback_data='to_male_categories'))
    return keyboard.adjust(1).as_markup()

# male_keys = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Записаться ✏️', callback_data='male_record')],
#     [InlineKeyboardButton(text='Назад ↪️', callback_data='to_male_categories')],
# ])


async def child_categories():
    all_categories = await get_child_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                                callback_data=f'child_category_{category.id}'))
    return keyboard.adjust(1).as_markup()

async def child_items(category_id):
    all_items = await get_child_items(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name,
                                callback_data=f'child_item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад ↪️',
                                callback_data='to_child_categories'))
    return keyboard.adjust(1).as_markup()

# child_keys = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Записаться ✏️', callback_data='child_record')],
#     [InlineKeyboardButton(text='Назад ↪️', callback_data='to_child_categories')],
# ])
