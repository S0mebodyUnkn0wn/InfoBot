import asyncio
import logging
import sys
import pathlib

from aiogram.enums import ParseMode

from page import *
from parser import build_pages_from_file
from callbacks import *

from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

token = pathlib.Path("token").read_text() # Put your bot's token into `token` file

BACK_TEXT = "Back" #allows you to customise the label used for the "back" button

root_page: Page
pages_lookup: dict[int,Unit]

dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    global root_page, pages_lookup
    builder = InlineKeyboardBuilder()

    for i in root_page.children:
        i: Unit
        builder.button(text=f"{i.title}", callback_data=f"{i.id}")

    builder.adjust(1,True)
    await message.answer(f"{root_page.content}",reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN_V2)

@dp.callback_query()
async def callback_handler(query: CallbackQuery) -> None:
    r = int(query.data)
    req = pages_lookup[r]
    if isinstance(req, Page):
        builder = InlineKeyboardBuilder()
        for i in req.children:
            i: Unit
            builder.button(text=f"{i.title}", callback_data=f"{i.id}")
        if req.parent_id!=-1:
            builder.button(text=f"{BACK_TEXT}", callback_data=f"{req.parent_id}")
        builder.adjust(1,True)
        await query.message.edit_text(f"{req.content}", parse_mode=ParseMode.MARKDOWN_V2)
        await query.message.edit_reply_markup(reply_markup=builder.as_markup())
        await query.answer()
    if isinstance(req, Button):
        await req.callback(query,globals())
        await query.answer()


async def main () -> None:
    bot = Bot(token=token)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    root_page, pages_lookup = build_pages_from_file(pathlib.Path("pages.xml"))
    asyncio.run(main())
