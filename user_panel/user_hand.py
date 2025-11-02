
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


@user_router.message(Command('reg'))
async def registration(message: Message, state: FSMContext):
    '''Функция регистрации клиента.'''
    await state.set_state(Reg.name)
    await message.answer('Введите ваше имя.')


@user_router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    '''Функция обработки имени клиента'''
    await state.update_data(name=message.text)
    await state.set_state(Reg.phone)
    await message.answer('Введите ваш номер телефона.')


@user_router.message(Reg.phone)
async def reg_phone(message: Message, state: FSMContext):
    '''Функция обработки номера телефона'''
    await state.update_data(phone=message.text)
    # Пример введенного номера +0(000)000-00-00.
    number_correctness = message.text.translate({ord(i): None for i in ' -()+'})  # Удаляем лишние символы
    if len(number_correctness) == 11:  # Если количество цифр в номере 11, номер проходит проверку.
        data = await state.get_data()  # Сохраняем введенную информацию в словарь.
        await message.answer(f'Ваше имя {data["name"]}\nВаш номер {data["phone"]}')
    else:  # Иначе сообщаем об ошибке.
        await message.answer(f'Ошибка. Неправильный номер.\nНомер не сохранен')
    await state.clear()  # Очищаем состояние.


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привет!', reply_markup=uskey.main_user_keys)


@user_router.message(F.text.lower() == 'на главную')
async def show_info(message: Message):
    await message.answer(main_text, reply_markup=uskey.main_user_keys)



@user_router.message(F.text.lower() == 'мой профиль')
async def show_info(message: Message):
    await message.answer('Мой профиль')


@user_router.message(F.text.lower() == 'услуги')
async def show_info(message: Message):
    await message.answer('Выберите для кого услуга', reply_markup=uskey.categories_user_keys)


@user_router.message(F.text.lower() == 'женские')
async def show_info(message: Message):
    await message.answer('Для женщин', reply_markup=await uskey.female_categories())

@user_router.callback_query(F.data.startswith('female_category_') or F.data.startswith('to_female_categories'))
async def female_category(callback: CallbackQuery):
    await callback.message.answer('Выберите услуги',
                                  reply_markup=await uskey.female_items(callback.data.split('_')[2]))

@user_router.callback_query(F.data.startswith('female_item_'))
async def female_category(callback: CallbackQuery):
    item_data = await rq.get_female_item(callback.data.split('_')[2])
    await callback.message.answer(f'Услуга: {item_data.name}\n{item_data.description}\n'
                                  f'Время: {item_data.time}\nЦена: {item_data.price}',
                                  reply_markup=uskey.female_keys)


@user_router.message(F.text.lower() == 'мужские')
async def show_info(message: Message):
    await message.answer('Для мужчин', reply_markup=await uskey.male_categories())


@user_router.callback_query(F.data.startswith('male_category_'))
async def male_category(callback: CallbackQuery):
    await callback.message.answer('Выберите услугу',
                                  reply_markup=await uskey.male_items(callback.data.split('_')[2]))

@user_router.callback_query(F.data.startswith('male_item_'))
async def male_category(callback: CallbackQuery):
    item_data = await rq.get_male_item(callback.data.split('_')[2])
    await callback.message.answer(f'Услуга: {item_data.name}\n{item_data.description}\n'
                                  f'Время: {item_data.time}\nЦена: {item_data.price}',
                                  reply_markup=uskey.male_keys)


@user_router.message(F.text.lower() == 'детские')
async def show_info(message: Message):
    await message.answer('Для детей', reply_markup=await uskey.child_categories())

@user_router.callback_query(F.data.startswith('child_category_'))
async def child_category(callback: CallbackQuery):
    await callback.message.answer('Выберите услугу',
                                  reply_markup=await uskey.child_items(callback.data.split('_')[2]))

@user_router.callback_query(F.data.startswith('child_item_'))
async def child_category(callback: CallbackQuery):
    item_data = await rq.get_child_item(callback.data.split('_')[2])
    await callback.message.answer(f'Услуга: {item_data.name}\n{item_data.description}\n'
                                  f'Время: {item_data.time}\nЦена: {item_data.price}',
                                  reply_markup=uskey.child_keys)


@user_router.message(F.text.lower() == 'акции')
async def show_info(message: Message):
    await message.answer('Акции')


@user_router.message(F.text.lower() == 'информация')
async def show_info(message: Message):
    await message.answer(info_string, reply_markup=uskey.info_keys)
