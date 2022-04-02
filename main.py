# Modules

import requests
from aiogram import types, executor
from dispatcher import bot, dp, db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

"""State Class"""


class FSMSettings(StatesGroup):
    currency = State()
    name = State()


"""Save in memory"""


@dp.message_handler(state=FSMSettings.name)
async def upload_name(message: types.message, state: FSMContext):
    """Detected data"""
    async with state.proxy() as data:
        data["name"] = message.text
    await message.answer("Name saved")
    """Checking in the database"""
    if db.show_info(message.from_user.id):
        db.update_name(message.from_user.id, data["name"])
    else:
        db.inster_name(message.from_user.id, data["name"])
    await state.finish()


@dp.message_handler(state=FSMSettings.currency)
async def upload_name(message: types.message, state: FSMContext):
    """Detected data"""
    async with state.proxy() as data:
        data["currency"] = message.text
    await message.answer("Currency saved")
    """Checking in the database"""
    if db.show_info(message.from_user.id):
        db.update_currency(message.from_user.id, data["currency"])
    else:
        db.inster_currency(message.from_user.id, data["currency"])
    await state.finish()


"""Welcome Message"""


@dp.message_handler(commands=["start", "help"])
async def welcome(message: types.Message):
    mark = types.InlineKeyboardMarkup(row_width=2)
    mark2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark2.row("Settings 📎", "Course 💹")
    mark.add(
        types.InlineKeyboardButton(text="Help", callback_data="help"),
        types.InlineKeyboardButton(
            text="Repository", url="https://github.com/HellenWeb/crypto-track"
        ),
    )
    await message.answer(
        f"Hello <strong>{message.from_user.first_name}</strong>\n\n<strong> - This bot will help you save your time and will send you messages about raising and lowering the rate of cryptocurrency</strong>\n\n - The bot will be useful for passive earnings on cryptocurrency without constant monitoring of the course\n\nCreator: @YungHellen",
        reply_markup=mark,
        parse_mode="html",
    )


"""Settings"""


@dp.message_handler(commands=["settings"])
async def settings(message: types.Message):
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark.row("Currency", "Name")
    mark.row("🏠")
    try:
        await message.answer(
            f"ID - {message.from_user.id}\nName - {db.show_info(message.from_user.id)[0][2]}\nCurrency - {db.show_info(message.from_user.id)[0][3]}",
            reply_markup=mark,
        )
    except IndexError:
        await message.answer(
            f"ID - {message.from_user.id}\nName - not entered\nCurrency - not entered\n\nTo make the data visible you need to fill them all in",
            reply_markup=mark,
        )


@dp.message_handler(commands=["course"])
async def course(message: types.Message):
    try:
        if db.show_info(message.from_user.id)[0][3]:
            mark = types.InlineKeyboardMarkup(row_width=2)
            mark.add(
                types.InlineKeyboardButton(text="SELL", callback_data="sell"),
                types.InlineKeyboardButton(text="BUY", callback_data="buy"),
            )

            await message.answer(f"Select:", reply_markup=mark)
    except IndexError:
        await message.answer("Profile not filled 🚫")


"""Callbacks Inline"""


@dp.callback_query_handler(lambda r: r.data == "help")
async def help(callback_data: types.CallbackQuery):
    mark = types.InlineKeyboardMarkup(row_width=2)
    mark.add(
        types.InlineKeyboardButton(text="Back", callback_data="back"),
        types.InlineKeyboardButton(
            text="Repository", url="https://github.com/HellenWeb/crypto-track"
        ),
    )
    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=f"<strong>/start</strong> or <strong>/help</strong> = Start Message\n<strong>/settings</strong> = Your Profile\n<strong>/course</strong> = Course cryptocurrencies",
        reply_markup=mark,
        parse_mode="html",
    )


@dp.callback_query_handler(lambda r: r.data == "back")
async def back(callback_data: types.CallbackQuery):
    mark = types.InlineKeyboardMarkup(row_width=2)
    mark.add(
        types.InlineKeyboardButton(text="Help", callback_data="help"),
        types.InlineKeyboardButton(
            text="Repository", url="https://github.com/HellenWeb/crypto-track"
        ),
    )
    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=f"Hello <strong>{callback_data.message.from_user.first_name}</strong>\n\n<strong> - This bot will help you save your time and will send you messages about raising and lowering the rate of cryptocurrency</strong>\n\n - The bot will be useful for passive earnings on cryptocurrency without constant monitoring of the course\n\nCreator: @YungHellen",
        reply_markup=mark,
        parse_mode="html",
    )


@dp.callback_query_handler(lambda t: t.data == "sell")
async def sell(callback_data: types.CallbackQuery):
    req = requests.get(
        f"https://yobit.net/api/3/trades/{db.show_info(callback_data.from_user.id)[0][3]}_usd"
    )

    total_trade_ask = 0
    amount_ask = 0

    for item in req.json()[f"{db.show_info(callback_data.from_user.id)[0][3]}_usd"]:
        if item["type"] == "ask":
            total_trade_ask = item["price"]
            amount_ask += item["amount"]

    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=f"PRICE: <strong>{round(total_trade_ask, 2)} $</strong>\nAMOUNT: {round(amount_ask)}",
        parse_mode="html",
    )


@dp.callback_query_handler(lambda t: t.data == "buy")
async def buy(callback_data: types.CallbackQuery):
    req = requests.get(
        f"https://yobit.net/api/3/trades/{db.show_info(callback_data.from_user.id)[0][3]}_usd"
    )

    total_trade_bid = 0
    amount_dis = 0

    for item in req.json()[f"{db.show_info(callback_data.from_user.id)[0][3]}_usd"]:
        if item["type"] == "bid":
            total_trade_bid = item["price"]
            amount_dis += item["amount"]

    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=f"PRICE: <strong>{round(total_trade_bid, 2)} $</strong>\nAMOUNT: {round(amount_dis)}",
        parse_mode="html",
    )


"""Reply Callbacks"""


@dp.message_handler(content_types=["text"], state=None)
async def reply(message: types.Message):
    if message.chat.type == "private":
        if message.text == "Currency":
            await FSMSettings.currency.set()
            await message.answer(
                "Enter the tracked cryptocurrency, in abbreviated form (eth)"
            )
        if message.text == "Name":
            await FSMSettings.name.set()
            await message.answer("Enter your name")
        if message.text == "Course 💹":
            try:
                if db.show_info(message.from_user.id)[0][3]:
                    mark = types.InlineKeyboardMarkup(row_width=2)
                    mark.add(
                        types.InlineKeyboardButton(text="SELL", callback_data="sell"),
                        types.InlineKeyboardButton(text="BUY", callback_data="buy"),
                    )

                    await message.answer(f"Select:", reply_markup=mark)
            except IndexError:
                await message.answer("Profile not filled 🚫")
        if message.text == "Settings 📎":
            mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mark.row("Currency", "Name")
            mark.row("🏠")
            try:
                await message.answer(
                    f"ID - {message.from_user.id}\nName - {db.show_info(message.from_user.id)[0][2]}\nCurrency - {db.show_info(message.from_user.id)[0][3]}",
                    reply_markup=mark,
                )
            except IndexError:
                await message.answer(
                    f"ID - {message.from_user.id}\nName - not entered\nCurrency - not entered\n\nTo make the data visible you need to fill them all in",
                    reply_markup=mark,
                )
        if message.text == "🏠":
            mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mark.row("Settings 📎", "Course 💹")
            await message.answer(
                f"Hello <strong>{message.from_user.first_name}</strong>\n\n<strong> - This bot will help you save your time and will send you messages about raising and lowering the rate of cryptocurrency</strong>\n\n - The bot will be useful for passive earnings on cryptocurrency without constant monitoring of the course\n\nCreator: @YungHellen",
                reply_markup=mark,
                parse_mode="html",
            )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
