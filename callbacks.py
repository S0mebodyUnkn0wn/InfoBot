"""
**Description**
===============

callbacks.py - Custom action callbacks go in this file.

To attach a custom action to a page - add <button> element containing the name of your callback function

callback functions should be asynchronous (declared using async keyword)
and should accept a two arguments - the callback query as defined in aiogram, and a dictionary of globals 

**Examples**
===========

**Callback function**::

    async def example_callback(query: CallbackQuery):
        t = time.time()
        await query.message.answer(f\"time on server {t}!\")

**HTML file**::

    <page>
        ...
        <button title="example button">
            example_callback
        </button>
    </page>

"""
import asyncio
import time

from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from page import Unit



async def example_callback(query: CallbackQuery, globals):
    pages_lookup = globals["pages_lookup"]
    BACK_TEXT = globals["BACK_TEXT"]

    t = time.time()
    req = pages_lookup[int(query.data)]
    await query.message.edit_text(f"Action taken! Current time on server: {t}")
    builder = InlineKeyboardBuilder()
    for i in req.children:
        i: Unit
        builder.button(text=f"{i.title}", callback_data=f"{i.id}")
    if req.parent_id!=-1:
        builder.button(text=f"{BACK_TEXT}", callback_data=f"{req.parent_id}")
    builder.adjust(1,True)
    await query.message.edit_reply_markup(reply_markup=builder.as_markup())
