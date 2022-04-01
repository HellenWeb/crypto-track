# Modules

import requests
from aiogram import types, executor
from dispatcher import bot, dp, db

"""Welcome Message"""


@dp.message_handler(commands=["start", "help"])
async def welcome(message: types.Message):
    mark = types.InlineKeyboardMarkup(row_width=2)
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
    try:
        await message.answer(f"ID - {message.from_user.id}\nName - {db.show_info(message.from_user.id)[0][2]}\nCurrency - {db.show_info(message.from_user.id)[0][3]}")
    except IndexError:
        await message.answer(f"ID - {message.from_user.id}\nName - not entered\nCurrency - not entered\n\nTo make the data visible you need to fill them all in")


"""Callbacks"""


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


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
