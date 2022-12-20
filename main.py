import ast
import sqlite3
import logging
from datetime import datetime
import random
import requests
from bs4 import BeautifulSoup

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import BOT_TOKEN, id_admin
from keyboards import kb_user_main, kb_admin_main, ikb_user_catalog, kb_user_recipes, recipes_info

API_TOKEN = BOT_TOKEN
id_admin = id_admin

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(_):
    print('Bot has been started!')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    hello = ["Привіт", "Hello", "Hi", "Ciao", "Chin-Chin", "Ehi"]
    random_index = random.randint(0, len(hello) - 1)
    if message.from_user.id == id_admin:
        await message.answer(f"{hello[random_index]}, {message.from_user.first_name}!\n"
                             f"/start", reply_markup=kb_admin_main)
    else:
        con = sqlite3.connect('bonta_db.db')
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users")
        db_users = cur.fetchall()
        if message not in db_users:
            cur.execute('INSERT or IGNORE INTO users\n'
                        '(user_id, username, first_name, last_name, date)\n'
                        'VALUES (?, ?, ?, ?, ?)', (message.from_user.id,
                                                   message.from_user.username,
                                                   message.from_user.first_name,
                                                   message.from_user.last_name,
                                                   datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        con.commit()
        cur.close()
        await message.answer(f"{hello[random_index]}, {message.from_user.full_name}!\n"
                             f"Раді бачити тебе в армії шанувальників смачної кухні.\n"
                             f"bonta.com.ua\n"
                             f"/start", reply_markup=kb_user_main)


@dp.message_handler(Text(equals="Хто заходив 🕺"))
async def delete_data_list(message: types.Message):
    if message.from_user.id == id_admin:
        with sqlite3.connect('bonta_db.db', check_same_thread=False) as db:
            cur = db.cursor()
            cur.execute("SELECT user_id, username, first_name, last_name, date FROM users")
            data = cur.fetchall()
            num = 0
            for i in data:
                await message.answer(text=f'<b>{i[4]}</b>\n'
                                          f'user_id: {i[0]}\n'
                                          f'username: @{i[1]}\n'
                                          f'first_name: {i[2]}\n'
                                          f'last_name: {i[3]}\n',
                                     parse_mode="HTML", reply_markup=kb_admin_main)
                num += 1
            await message.answer(text=f'Всього в базі <b>{num}</b> людей!', parse_mode="HTML")
    else:
        await message.answer(text="Потрібні права адміністратора!", reply_markup=kb_user_main)


# Розсилка
class FormSupport(StatesGroup):
    mailing = State()


@dp.message_handler(Text(equals='Розсилка 📨'))
async def mailing(message: types.Message):
    await FormSupport.mailing.set()
    await message.answer(text="<b>Текст розсилки:</b>",
                         parse_mode="HTML",
                         reply_markup=kb_admin_main)


@dp.message_handler(state=FormSupport.mailing)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mailing'] = message.text
    with sqlite3.connect('bonta_db.db', check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute("SELECT user_id FROM users")
        user_id = cur.fetchall()
        num_y = 0
        num_n = 0
    for i in user_id:
        try:
            await bot.send_message(i[0], md.text(data['mailing']), disable_notification=True)
            num_y += 1
        except:
            num_n += 1
    await message.answer(md.text(f'<b>{num_y}</b> користувачів <b>ОТРИМАЛИ</b> ✅\n'
                                 f'<b>{num_n}</b> користувачів <b>НЕ ОТРИМАЛИ</b> ⛔️\n'
                                 f'\n'
                                 f'<b>Повідомлення:</b>\n',
                                 data['mailing']),
                         parse_mode="HTML",
                         reply_markup=kb_admin_main)
    await state.finish()


# Перехід в меню покупця з режиму адміністратора
@dp.message_handler(Text(equals="Меню покупця 👤"))
async def mailing(message: types.Message):
    await message.answer(text="Меню покупця:",
                         reply_markup=kb_user_main)


# Каталог товарів
@dp.message_handler(Text(equals="Каталог товарів  🗂"))
async def mailing(message: types.Message):
    await message.answer(text="Каталог товарів <b>bonta.com.ua</b>:",
                         parse_mode="HTML",
                         reply_markup=ikb_user_catalog)


# Контактна інформація / Графік роботи
@dp.message_handler(Text(equals="Контакти  📍"))
async def mailing(message: types.Message):
    await message.answer(text="<b>Італійські Смаколики!</b>\n"
                              "<em>Контактна особа:</em> Якубович Кирило\n"
                              "<em>Адреса:</em> вул. Філософська 86, оф. 208Б, Дніпро, Україна\n"
                              "<em>Телефон:</em> <b>+380 (67) 643-30-30 - Гаряча лінія</b>\n"
                              "<em>Телефон:</em> <b>+380 (96) 896-93-98 - Доставка по місту Дніпро</b>\n"
                              "<em>Email:</em> store1.bonta@gmail.com\n"
                              "<em>Сайт компанії:</em> <b>bonta.com.ua/ua</b>\n"
                              "\n"
                              "<b>Графік роботи:</b>\n"
                              "09:00 - 17:00 Понеділок\n"
                              "09:00 - 17:00 Вівторок\n"
                              "09:00 - 17:00 Середа\n"
                              "09:00 - 17:00 Четвер\n"
                              "09:00 - 17:00 Пʼятниця\n"
                              "10:00 - 14:00 Субота\n"
                              "Неділя - Вихідний",
                         parse_mode="HTML",
                         reply_markup=kb_user_main)


# Рецепти
@dp.message_handler(Text(equals="Рецепти  📚"))
async def mailing(message: types.Message):
    await message.answer(text=recipes_info,
                         parse_mode="HTML",
                         reply_markup=kb_user_recipes)


# Інлайн кнопка під кожним смаколиком
def kb(el):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(f'Замовити за {str(el[2])}', url=el[1])
    keyboard.add(button)
    return keyboard


# Парсінг / section = лінк на розділ для парсингу
def get_pars(section):
    r = requests.get(f"{section}")
    soup = BeautifulSoup(r.text, 'lxml')
    items = soup.findAll('li', class_='cs-product-gallery__item cs-online-edit js-productad')
    data = []
    for item in items:
        name = item.find('a', class_='cs-goods-title').text
        link = 'https://bonta.com.ua/' + item.find('a', class_='cs-goods-title').get('href')
        price = item.find('span', class_='cs-goods-price__value cs-goods-price__value_type_current').text
        data.append([name, link, price])
    return data


@dp.callback_query_handler()
async def cbd_sauces(callback: types.CallbackQuery):
    if callback.data == 'sauces':
        data = get_pars('https://bonta.com.ua/ua/g108597487-sousy?product_items_per_page=48')
        for el in data:
            await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    if callback.data == 'groceries_and_condiments':
        data = get_pars('https://bonta.com.ua/ua/g108622037-bakaleya-pripravy')
        for el in data:
            await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    if callback.data == 'flour':
        data = get_pars('https://bonta.com.ua/ua/g112060733-muka')
        for el in data:
            await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    if callback.data == 'olive_oil':
        data = get_pars('https://bonta.com.ua/ua/g108693005-olivkovoe-maslo')
        for el in data:
            await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    if callback.data == 'canned_food':
        data = get_pars('https://bonta.com.ua/ua/g108618569-konservy')
        for el in data:
            await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    if callback.data == 'olives':
        data = get_pars('https://bonta.com.ua/ua/g112332508-olivki')
        for el in data:
            await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    if callback.data == 'sweet':
        data = get_pars('https://bonta.com.ua/ua/g108618568-sladosti')
        for el in data:
            await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    if callback.data == 'novelty':
        data = get_pars('https://bonta.com.ua/ua/g111149831-novinki')
        for el in data:
            await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    if callback.data == 'ready_sets':
        data = get_pars('https://bonta.com.ua/ua/g112064021-gotovye-nabory')
        for el in data:
            await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    if callback.data == 'gift_sets':
        data = get_pars('https://bonta.com.ua/ua/g112451341-podarochnye-nabory')
        for el in data:
            await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    if callback.data == 'pasta_and_risotto':
        r = requests.get("https://bonta.com.ua/ua/g108600624-pasta-rizotto")
        soup = BeautifulSoup(r.text, 'lxml')
        section = soup.findAll('li', class_='cs-product-groups-gallery__item cs-online-edit')
        for i in section:
            title = i.find('a', class_='cs-product-groups-gallery__title').text
            href = 'https://bonta.com.ua/' + i.find('a', class_='cs-product-groups-gallery__title').get('href')
            await callback.message.answer(text=f"<b>{title} 👇</b>", parse_mode="HTML")
            r = requests.get(f"{href}")
            soup = BeautifulSoup(r.text, 'lxml')
            items = soup.findAll('li', class_='cs-product-gallery__item cs-online-edit js-productad')
            data = []
            for item in items:
                name = item.find('a', class_='cs-goods-title').text
                link = 'https://bonta.com.ua/' + item.find('a', class_='cs-goods-title').get('href')
                price = item.find('span', class_='cs-goods-price__value cs-goods-price__value_type_current').text
                data.append([name, link, price])
            for el in data:
                await callback.message.answer(text=f'{el[1]}', reply_markup=kb(el))

    await callback.answer(text='Готово!')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Вибач, я тебе не розумію..")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

#     question = State()  # Запитати

# @dp.message_handler(Text(equals='Залишити повідомлення 📜'))
# async def mailing(message: types.Message):
#     await FormSupport.mailing.set()
#     await message.answer(text="<b>Текст повідомлення:</b>",
#                          parse_mode="HTML",
#                          reply_markup=kb_user_main)
#
#
# @dp.message_handler(state=FormSupport.mailing)
# async def process_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['mailing'] = message.text
#     await message.answer(text='Ваше повідомлення було успішно відправлено, дякуємо що обрали нас.',
#                          disable_notification=True)
#     await bot.send_message(id_admin, md.text(f'<b>@{message.from_user.username}\n'
#                                              f'{message.from_user.first_name} {message.from_user.last_name}\n'
#                                              f'Залишив наступне повідомлення:</b>\n',
#                                              data['mailing']),
#                            parse_mode="HTML",
#                            reply_markup=kb_user_main)
#     await state.finish()
