
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import user_panel.user_keys as uskey
from settings.config import info_string, main_text
import database.requests as rq


user_router = Router()


class Reg(StatesGroup):
    name = State()
    phone = State()
    update_name = State()
    update_phone = State()

class Service(StatesGroup):
    comment = State()
    update_comment = State()
    service_id = State()


def time_format(item_data):
    time_parts = item_data.split(':')  # ['2', '15'] или ['0', '30']
    hours = int(time_parts[0])
    minutes = int(time_parts[1])

    if hours == 0:
        # Только минуты
        item_time = f'от {minutes} мин'
    elif hours > 0 and minutes == 0:
        # Только часы, без минут
        # Склонение для часов
        if hours == 1:
            hour_word = 'час'
        elif 2 <= hours <= 4:
            hour_word = 'часа'
        else:
            hour_word = 'часов'
        item_time = f'от {hours} {hour_word}'
    else:
        # И часы и минуты
        # Склонение для часов
        if hours == 1:
            hour_word = 'час'
        elif 2 <= hours <= 4:
            hour_word = 'часа'
        else:
            hour_word = 'часов'

        # Склонение для минут
        if minutes == 1:
            minute_word = 'минута'
        elif 2 <= minutes <= 4:
            minute_word = 'минуты'
        else:
            minute_word = 'минут'

        item_time = f'от {hours} {hour_word} {minutes} {minute_word}'

    return item_time


@user_router.message(CommandStart())
@user_router.message(F.text.lower() == 'запустить бота')
async def cmd_start(message: Message):
    """Запускает бота."""
    await rq.set_user(message.from_user.id)
    await message.answer('Привет!', reply_markup=uskey.main_user_keys)



@user_router.callback_query(F.data == 'reg_usr')
async def registration(callback: CallbackQuery, state: FSMContext):
    """Регистрирует клиента."""
    await state.set_state(Reg.name)
    await callback.message.answer('Введите ваше имя.')
    await callback.answer()  # Заглушка для кнопки.


@user_router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    """Сохраняет имя клиента в базу."""
    await state.update_data(name=message.text)
    await state.set_state(Reg.phone)
    await message.answer('Введите ваш номер телефона.')


def phone_verify(number):
    """Проверяет номер телефона."""
    # Пример введенного номера +0(000)000-00-00.
    number_correctness = number.translate(
        {ord(i): None for i in ' -()+'})  # Удаляем лишние символы
    # Если количество цифр в номере 11, номер проходит проверку.
    if len(number_correctness) == 11:
        return number
    return False


@user_router.message(Reg.phone)
async def reg_phone(message: Message, state: FSMContext):
    """Сохраняет номер телефона в базу."""
    phone = message.text  # Ввод номера телефона.
    if phone_verify(phone):
        await state.update_data(phone=phone)
        # Сохраняем введенную информацию в словарь.
        data = await state.get_data()
        await rq.update_user(message.from_user.id, data["name"], data["phone"])
        user_info = await rq.get_user_info(message.from_user.id)
        user_date_created = user_info.date_created.strftime('%d.%m.%Y')
        await message.answer(
            f'👤 <b>Ваше имя:</b> {user_info.name}\n'
            f'📞 <b>Ваш номер:</b> {user_info.phone}\n'
            f'📌 <b>Профиль создан: {user_date_created}</b>',
            reply_markup=uskey.profile_btn,
            parse_mode='HTML')
    else:  # Иначе сообщаем об ошибке.
        await message.answer(f'Ошибка. Неправильный номер.\nНомер не сохранен')
    await state.clear()  # Очищаем состояние.


@user_router.callback_query(F.data == 'change_name')
async def change_name(callback: CallbackQuery, state: FSMContext):
    """Обработка изменения имени клиента."""
    await state.set_state(Reg.update_name)
    await callback.message.answer('Введите ваше имя:')
    await callback.answer()  # Заглушка для кнопки.


@user_router.message(Reg.update_name)
async def reg_name(message: Message, state: FSMContext):
    """Обновляет имя клиента."""
    await state.update_data(name=message.text)

    data = await state.get_data()  # Сохраняем введенную информацию в словарь.
    await rq.update_name(message.from_user.id, data["name"])
    await message.answer('Имя изменено')

    tg_id = message.from_user.id
    user_info = await rq.get_user_info(tg_id)
    user_date_created = user_info.date_created.strftime('%d.%m.%Y')
    await message.answer(
        f'👤 <b>Ваше имя:</b> {user_info.name}\n'
        f'📞 <b>Ваш номер:</b> {user_info.phone}\n'
        f'📌 <b>Профиль создан: {user_date_created}</b>',
        reply_markup=uskey.profile_btn,
        parse_mode='HTML')


@user_router.callback_query(F.data == 'change_phone')
async def change_name(callback: CallbackQuery, state: FSMContext):
    """Обработка изменения номера клиента."""
    await state.set_state(Reg.update_phone)
    await callback.message.answer('Введите ваш номер:')
    await callback.answer()  # Заглушка для кнопки.


@user_router.message(Reg.update_phone)
async def reg_name(message: Message, state: FSMContext):
    """Обновляет номер клиента."""
    await state.update_data(phone=message.text)  # Сохраняем введеный номер

    data = await state.get_data()  # Сохраняем введенную информацию в словарь.
    await rq.update_phone(message.from_user.id, data["phone"])
    await message.answer('Номер изменен')

    tg_id = message.from_user.id
    user_info = await rq.get_user_info(tg_id)
    user_date_created = user_info.date_created.strftime('%d.%m.%Y')

    await message.answer(
        f'👤 <b>Ваше имя:</b> {user_info.name}\n'
        f'📞 <b>Ваш номер:</b> {user_info.phone}\n'
        f'📌 <b>Профиль создан: {user_date_created}</b>',
        reply_markup=uskey.profile_btn,
        parse_mode='HTML')

@user_router.callback_query(F.data == 'delete_user')
async def delete_user(callback: CallbackQuery, state: FSMContext):
    """Удаляет клиента."""

    # Удаляем услуги клиента по id.
    tg_id = callback.from_user.id
    services = await rq.get_user_services(tg_id)
    for service in services:
        await rq.delete_service(service.id)

    # Сообщаем клиенту об удалении профиля.
    await callback.message.answer('Ваш профиль удален.',
                            reply_markup=uskey.start_btn)
    await callback.answer()  # Заглушка для кнопки.
    await rq.delete_user(callback.from_user.id)  # Удаляем клиента из базы.
    await state.clear()  # Очищаем состояние.


@user_router.message(F.text.lower() == 'информация ℹ️')
async def show_info(message: Message):
    """Выводит информацию о мастере."""
    await message.answer(info_string, reply_markup=uskey.info_keys)


@user_router.message(F.text.lower() == 'на главную ↪️')
async def to_main(message: Message):
    """Открывает главное меню."""
    await message.answer(main_text, reply_markup=uskey.main_user_keys)


@user_router.message(F.text.lower() == 'мой профиль 👤')
async def profile(message: Message):
    """Выводит информацию о клиенте."""
    user_info = await rq.get_user_info(message.from_user.id)
    user_date_created = user_info.date_created.strftime('%d.%m.%Y')
    if user_info.name is None or user_info.phone is None:
        keyboard = uskey.reg_btn  # Кнопки для регистрации
    else:
        keyboard = uskey.profile_btn  # Кнопки для профиля

    await message.answer(
        f'👤 <b>Ваше имя:</b> {user_info.name}\n'
        f'📞 <b>Ваш номер:</b> {user_info.phone}\n'
        f'📌 <b>Профиль создан: {user_date_created}</b>',
        reply_markup=keyboard,
        parse_mode='HTML')


@user_router.message(F.text.lower() == 'услуги 🛒')
async def services(message: Message):
    """Выводит меню услуг."""
    await message.answer('Выберите для кого услуга',
                        reply_markup=uskey.categories_user_keys)


@user_router.message(F.text.lower() == 'мои услуги 📋')
async def service_list(message: Message):
    """Выводит список зарегестрированных услуг клиента."""
    tg_id = message.from_user.id
    list_service = await rq.get_user_services(tg_id)
    if len(list_service.all()) == 0:
        await message.answer('📋 Ваш список услуг пуст')
        return
    await message.answer('📋 Ваши услуги',
                                reply_markup=await uskey.user_services(tg_id))


@user_router.callback_query(F.data.startswith('service_list'))
async def service_list(callback: CallbackQuery):
    """Выводит список зарегестрированных услуг клиента."""
    tg_id = callback.from_user.id
    await callback.message.answer('📋 Список услуг',
                                reply_markup=await uskey.user_services(tg_id))
    await callback.answer()  # Заглушка для кнопки.


@user_router.callback_query(F.data.startswith('services_'))
async def show_service(callback: CallbackQuery):
    """Выводит услугу клиента."""
    service_id = callback.data.split('_')[1]
    service_data = await rq.get_service_info(service_id)
    await callback.answer()  # Заглушка для кнопки.

    if service_data:
        await callback.message.edit_text(
            f'📝{service_data.service_category}: {service_data.service_item}'
            f'🕒 Время: {service_data.time} \n'
            f'💳 Стоимость: {service_data.price}'
            f'✏️ Комментарий:\n {service_data.user_comment}',
            reply_markup= await uskey.service_btn(service_id))
    else:
        await callback.message.answer('❌ Записи не существует.')


@user_router.callback_query(F.data.startswith('delete_service_'))
async def delete_user_service(callback: CallbackQuery):
    """Удаляет услугу клиента."""
    tg_id = callback.from_user.id
    service_id = callback.data.split('_')[2]

    await rq.delete_service(service_id)  # Удаляем услугу клиента из базы.
    await callback.answer()  # Заглушка для кнопки.
    await callback.message.delete()  # Удаляем сообщение.

    list_service = await rq.get_user_services(tg_id)
    if len(list_service.all()) == 0:
        await callback.message.answer('📋 Ваш список услуг пуст')
        return
    await callback.message.answer('📋 Список услуг',
                    reply_markup=await uskey.user_services(tg_id))


@user_router.callback_query(F.data.startswith('record'))
async def start_booking(callback: CallbackQuery, state: FSMContext):
    """Запись услуги в базу."""

    # Проверяем регистрацию пользователя.
    tg_id = callback.from_user.id
    user = await rq.get_user_info(tg_id)
    if user.name is None:
        await callback.message.answer('Для записи пройдите регистрацию.')
        await registration(callback, state)
        return

    item_id = int(callback.data.split('_')[2])
    gender = callback.data.split('_')[1]

    # Получаем данные услуги
    if gender == 'female':
        item_data = await rq.get_female_item(item_id)
    elif gender == 'male':
        item_data = await rq.get_male_item(item_id)
    elif gender == 'child':
        item_data = await rq.get_child_item(item_id)

    # Сохраняем состояние в data
    await state.update_data(
        item_id=item_id,
        gender=gender,
        service_name=item_data.name,
        price=item_data.price,
        time=item_data.time
    )

    await callback.message.answer(
        f"🤝 Комментарий будет передан мастеру.\n"
        f"✏️ Напишите в комментарий удобный для вас день и время:",
        reply_markup=uskey.comment_btn)
    await callback.answer()  # Заглушка для кнопки.
    await state.set_state(Service.comment)


@user_router.message(Service.comment)
async def save_service(message: Message, state: FSMContext):
    """Сохраняет запись с комментарием."""

    user_comment = message.text
    data = await state.get_data()
    tg_id = message.from_user.id
    service_record = True

    # Получаем информацию о пользователе
    user_info = await rq.get_user_info(tg_id)

    # Получаем полную информацию об услуге по сохраненному ID
    if not data:
        service_record = False
    elif data['gender'] == 'female':
        item_data = await rq.get_female_item(data['item_id'])
        category = await rq.get_female_category(item_data.category)
        gender = 'Женская'
    elif data['gender'] == 'male':
        item_data = await rq.get_male_item(data['item_id'])
        category = await rq.get_male_category(item_data.category)
        gender = 'Мужская'
    elif data['gender'] == 'child':
        item_data = await rq.get_child_item(data['item_id'])
        category = await rq.get_child_category(item_data.category)
        gender = 'Детская'

    # Сохраняем запись в БД
    if service_record:
        await rq.add_service(
            tg_id=tg_id,
            client_name=user_info.name,
            client_phone=user_info.phone,
            user_comment=user_comment,  # Комментарий клиента.
            gender=gender,
            service_category=category.name,
            service_item=data['service_name'],
            price=data['price'],
            time=data['time']
        )

        await message.answer("✅ Запись сохранена.")
        await message.answer('📋 Список услуг',
                                reply_markup=await uskey.user_services(tg_id))
    else:
        await message.answer()  # Заглушка для кнопки.
    await state.clear()  # Очистка состояния.


@user_router.callback_query(F.data.startswith('skip_comment'))
async def skip_comment(callback: CallbackQuery, state: FSMContext):
    """Запись услуги без комментария."""

    # Получаем все данные из состояния
    data = await state.get_data()

    # Получаем информацию о пользователе
    tg_id = callback.from_user.id
    user_info = await rq.get_user_info(tg_id)

    service_record = True

    # Получаем полную информацию об услуге по сохраненному ID
    if not data:
        service_record = False
    elif data['gender'] == 'female':
        item_data = await rq.get_female_item(data['item_id'])
        category = await rq.get_female_category(item_data.category)
        gender='Женские'
    elif data['gender'] == 'male':
        item_data = await rq.get_male_item(data['item_id'])
        category = await rq.get_male_category(item_data.category)
        gender='Мужские'
    elif data['gender'] == 'child':
        item_data = await rq.get_child_item(data['item_id'])
        category = await rq.get_child_category(item_data.category)
        gender='Детские'

    # Сохраняем запись в БД с пустым комментарием
    if service_record:
        await rq.add_service(
            tg_id=tg_id,
            client_name=user_info.name,
            client_phone=user_info.phone,
            user_comment='Без комментария',  # Без комментария.
            gender=gender,
            service_category=category.name,
            service_item=data['service_name'],
            price=data['price'],
            time=data['time']
        )

        await callback.message.answer("✅ Запись сохранена.")
        await callback.message.answer('📋 Список услуг',
                                reply_markup=await uskey.user_services(tg_id))
    else:
        await callback.answer()  # Заглушка для кнопки.
    await state.clear()  # Очистка состояния.


@user_router.callback_query(F.data.startswith('change_comment_'))
async def change_comment(callback: CallbackQuery, state: FSMContext):
    """Обработка изменения комментария клиента."""
    service_id = callback.data.split('_')[2]
    # Сохраняем id услуги для изменения.
    await state.update_data(service_id=service_id)

    await callback.message.answer(
        f"🤝 Комментарий будет передан мастеру.\n"
        f"✏️ Напишите в комментарий удобный для вас день и время:",
        reply_markup=uskey.change_comment_btn)
    await callback.answer()  # Заглушка для кнопки.
    await state.set_state(Service.update_comment)


@user_router.message(Service.update_comment)
async def update_comment(message: Message, state: FSMContext):
    """Обновляет комментарий клиента в выбранной услуге."""
    # Сохраняем введеный комментарий.
    await state.update_data(new_comment=message.text)

    data = await state.get_data()  # Достаем сохраненную информацию.
    await rq.update_comment(data["new_comment"], data["service_id"])
    await message.answer('✅ Комментарий изменен.')
    await state.clear()

    service_data = await rq.get_service_info(data["service_id"])

    if service_data:
        await message.answer(
            f'📝{service_data.service_category}: {service_data.service_item}\n'
            f'🕒 Время: {service_data.time} \n'
            f'💳 Стоимость: {service_data.price}\n'
            f'✏️ Комментарий:\n {service_data.user_comment}',
            reply_markup= await uskey.service_btn(data["service_id"])
            )
    else:
        await message.answer('❌ Записи не существует.')


@user_router.callback_query(F.data.startswith('cancle_comment_change'))
async def comment_cancle(callback: CallbackQuery, state: FSMContext):
    """Отмена изменения комментария."""
    await state.clear()  # Очистка состояния.
    await callback.message.answer("✅ Изменения отменены.")
    await callback.answer()  # Заглушка для кнопки.


@user_router.callback_query(F.data.startswith('service_cancle'))
async def service_cancle(callback: CallbackQuery, state: FSMContext):
    """Отменена записи."""
    await state.clear()  # Очистка состояния.
    await callback.message.delete()  # Удаляем сообщение.
    await callback.message.answer("✅ Регистрация записи отменена.")
    await callback.answer()  # Заглушка для кнопки.


@user_router.message(F.text.lower() == 'женские 💇‍♀️')
async def females(message: Message):
    """Выводит женские категории услуги."""
    await message.answer('Для женщин',
                                reply_markup=await uskey.female_categories())


@user_router.callback_query(F.data.startswith('to_female_categories'))
async def back_to_female_categories(callback: CallbackQuery):
    """Выводит женские категории услуг."""
    await callback.answer()  # Заглушка для кнопки.
    await callback.message.edit_text('Для женщин',
                                reply_markup=await uskey.female_categories())


@user_router.callback_query(F.data.startswith('female_category_'))
async def female_category(callback: CallbackQuery):
    """Выводит женские услуги."""
    await callback.answer()  # Заглушка для кнопки.
    await callback.message.edit_text('Выберите услугу',
        reply_markup=await uskey.female_items(callback.data.split('_')[2]))


@user_router.callback_query(F.data.startswith('female_item_'))
async def female_item(callback: CallbackQuery):
    """Выводит информацию об услуге."""
    item_id = int(callback.data.split('_')[2])
    item_data = await rq.get_female_item(item_id)
    time_data = time_format(item_data.time)
    await callback.answer()  # Заглушка для кнопки.
    if item_data.description == 'Пусто':  # Пустое описание не выводить.
        await callback.message.edit_text(
            f'💇‍♀️ <b>Услуга:</b> {item_data.name}\n'
            f'🕒 <b>Время:</b> {time_data}\n'
            f'💳 <b>Цена:</b> от {item_data.price} руб.',
                reply_markup=await uskey.item_info('female', item_id),
                parse_mode='HTML')
    else:
        await callback.message.edit_text(
            f'💇‍♀️ <b>Услуга:</b> {item_data.name}\n'
            f'📝{item_data.description}\n'
            f'🕒 <b>Время:</b> {time_data}\n'
            f'💳 <b>Цена:</b> от {item_data.price} руб.',
                reply_markup=await uskey.item_info('female', item_id),
                parse_mode='HTML')


@user_router.message(F.text.lower() == 'мужские 💇‍♂️')
async def males(message: Message):
    """Выводит мужские категории услуг."""
    await message.answer('Для мужчин',
                                reply_markup=await uskey.male_categories())


@user_router.callback_query(F.data.startswith('to_male_categories'))
async def back_to_male_categories(callback: CallbackQuery):
    await callback.answer()  # Заглушка для кнопки.
    await callback.message.edit_text('Для мужчин',
                                reply_markup=await uskey.male_categories())


@user_router.callback_query(F.data.startswith('male_category_'))
async def male_category(callback: CallbackQuery):
    await callback.answer()  # Заглушка для кнопки.
    await callback.message.edit_text('Выберите услугу',
            reply_markup=await uskey.male_items(callback.data.split('_')[2]))


@user_router.callback_query(F.data.startswith('male_item_'))
async def male_item(callback: CallbackQuery):
    """Выводит информацию об услуге."""
    item_id = int(callback.data.split('_')[2])
    item_data = await rq.get_male_item(item_id)
    time_data = time_format(item_data.time)
    await callback.answer()  # Заглушка для кнопки.
    if item_data.description == 'Пусто':  # Пустое описание не выводить.
        await callback.message.edit_text(
            f'💇‍♂️ <b>Услуга:</b> {item_data.name}\n'
            f'🕒 <b>Время:</b> {time_data}\n'
            f'💳 <b>Цена:</b> от {item_data.price} руб.',
                reply_markup=await uskey.item_info('male', item_id),
                parse_mode='HTML')
    else:
        await callback.message.edit_text(
            f'💇‍♂️ <b>Услуга:</b> {item_data.name}\n'
            f'📝 {item_data.description}\n'
            f'🕒 <b>Время:</b> {time_data}\n'
            f'💳 <b>Цена:</b> от {item_data.price} руб.',
                reply_markup=await uskey.item_info('male', item_id),
                parse_mode='HTML')


@user_router.message(F.text.lower() == 'детские 👶')
async def childish(message: Message):
    """Выводит детские категории услуг."""
    await message.answer('Для детей',
                                reply_markup=await uskey.child_categories())


@user_router.callback_query(F.data.startswith('to_child_categories'))
async def back_to_child_categories(callback: CallbackQuery):
    await callback.answer()  # Заглушка для кнопки.
    await callback.message.edit_text('Для детей',
                                reply_markup=await uskey.child_categories())


@user_router.callback_query(F.data.startswith('child_category_'))
async def child_category(callback: CallbackQuery):
    await callback.answer()  # Заглушка для кнопки.
    await callback.message.edit_text('Выберите услугу',
            reply_markup=await uskey.child_items(callback.data.split('_')[2]))


@user_router.callback_query(F.data.startswith('child_item_'))
async def child_item(callback: CallbackQuery):
    """Выводит информацию об услуге."""
    item_id = int(callback.data.split('_')[2])
    item_data = await rq.get_child_item(item_id)
    time_data = time_format(item_data.time)
    await callback.answer()  # Заглушка для кнопки.
    if item_data.description == 'Пусто':  # Пустое описание не выводить.
        await callback.message.edit_text(
            f'💇 <b>Услуга:</b> {item_data.name}\n'
            f'🕒 <b>Время:</b> {time_data}\n'
            f'💳 <b>Цена:</b> от {item_data.price} руб.',
                reply_markup=await uskey.item_info('child', item_id),
                parse_mode='HTML')
    else:
        await callback.message.edit_text(
            f'💇 <b>Услуга:</b> {item_data.name}\n'
            f'📝 {item_data.description}\n'
            f'🕒 <b>Время:</b> {time_data}\n'
            f'💳 <b>Цена:</b> от {item_data.price} руб.',
                reply_markup=await uskey.item_info('child', item_id),
                parse_mode='HTML')
