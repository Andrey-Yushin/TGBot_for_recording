
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import (get_female_categories, get_female_items,
                               get_male_categories, get_male_items,
                               get_child_categories, get_child_items,
                               get_user_services, get_users)
import database.requests as rq


admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Клиенты 👥'),
     KeyboardButton(text='Мои услуги 🛒')],
    [KeyboardButton(text='Создать объявление 📢'),
     KeyboardButton(text='Записи 📝')]
],
    resize_keyboard=True, #  Меняем размер кнопок.
    input_field_placeholder='Выберите пункт меню...'  # Подставляем placeholder.
)


notification_keys = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить ✅', callback_data="send_notification"),
     InlineKeyboardButton(text='Отмена ❌', callback_data="cancel_notification")]
])


async def back_client_list(tg_id):
    """Возвращает кнопки управления клиента."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data='userlist_0_8'))
    keyboard.add(InlineKeyboardButton(
        text="⛔ Удалить",
        callback_data=f'delete_{tg_id}'))
    return keyboard.adjust(1).as_markup()


async def delete_user(tg_id):
    """Подтверждение удаления клиента."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="⬅️ Отмена",
        callback_data='userlist_0_8'))
    keyboard.add(InlineKeyboardButton(
        text="⛔ Удалить клиента ⛔",
        callback_data=f'accept_delete_{tg_id}'))
    return keyboard.adjust(1).as_markup()


async def user_list(start=0, end=8):
    """Выводит страничный список клиентов."""
    users = await get_users()
    users = users.all()

    keyboard = InlineKeyboardBuilder()
    for user in users[start:end]:
        keyboard.add(InlineKeyboardButton(
            text=user.name,
            callback_data=f'user_{user.tg_id}'))

    user_page = 8  # Количество клиентов на странице.
    # Высчитываем end на последней странице.
    lastpage = len(users) - len(users) % user_page + user_page

    if len(users) > user_page:
        if end >= lastpage:  # Отображаем кнопку "Назад" (последняя страница).
            keyboard.add(InlineKeyboardButton(
                text='⬅️ Назад',
                callback_data=f'userlist_{start-user_page}_{end-user_page}'
            ))
        elif start == 0:  # Отображаем кнопку "Далее" (Первая страница).
            keyboard.add(InlineKeyboardButton(
                text='Далее ➡️',
                callback_data=f'userlist_{start+user_page}_{end+user_page}'
            ))
        else:  # Отображаем обе кнопки (Страницы между первой и последней)
            keyboard.add(InlineKeyboardButton(
                text='⬅️ Назад',
                callback_data=f'userlist_{start-user_page}_{end-user_page}'
            ))
            keyboard.add(InlineKeyboardButton(
                text='Далее ➡️',
                callback_data=f'userlist_{start+user_page}_{end+user_page}'
            ))

    return keyboard.adjust(2).as_markup()
