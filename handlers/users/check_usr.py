import logging
from loader import dp, bot, db
from aiogram import types
from middlewares.check_user import User_Check
from function.translator import translator
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.inline.button import MainCallback
from data.config import yil_oy_kun, soat_minut_sekund


@dp.message(User_Check())
async def start_handler(msg: types.Message):
    try:
        cid = msg.from_user.id
        lang = msg.from_user.language_code
        ruyxat = db.select_channels()
        btn = InlineKeyboardBuilder()
        text = translator(text="🛑 You are not join the channel!:\n\n",
                          dest=lang)
        son = 0
        for x in ruyxat:
            ids = str(-100) + str(x[1])
            kanals = await bot.get_chat(ids)
            try:
                res = await bot.get_chat_member(chat_id=ids, user_id=cid)
            except:
                continue
            if res.status == 'member' or res.status == 'administrator' or res.status == 'creator':
                pass
            else:
                son += 1
                btn.button(text='➕ ' + kanals.title,
                           url=f"{await kanals.export_invite_link()}")

                text += f"\n{son}<b><i></i>. ⭕ {kanals.full_name}</b> <i>@{kanals.username} ❓</i>\n"

        btn.button(text=translator(text='♻ Check!',
                                   dest=lang),
                   callback_data=MainCallback(action="check_join",
                                              q='').pack())
        btn.adjust(1)
        await msg.answer(text=f"<b>{text}</b>",
                         reply_markup=btn.as_markup())
        cid = msg.from_user.id
        if db.check_user(cid=cid) is None:
            db.add_user(cid=cid,
                        date=str(yil_oy_kun) + ' / ' + str(soat_minut_sekund))
    except Exception as err:
        logging.error(err)


@dp.callback_query(User_Check())
async def start_callback_query(call: types.CallbackQuery):
    try:
        cid = call.from_user.id
        lang = call.from_user.language_code
        ruyxat = db.select_channels()
        btn = InlineKeyboardBuilder()
        text = translator(text="🛑 You are not join the channel!:\n\n",
                          dest=lang)
        text1 = translator(text="🛑 You are not join the channel!:\n\n",
                           dest=lang)
        son = 0
        for x in ruyxat:
            ids = str(-100) + str(x[1])
            channels = await bot.get_chat(ids)
            try:
                res = await bot.get_chat_member(chat_id=ids, user_id=cid)
            except:
                continue
            if res.status == 'member' or res.status == 'administrator' or res.status == 'creator':
                pass
            else:
                son += 1
                text += f"\n{son}<b><i></i>. ⭕ {channels.full_name}</b> <i>@{channels.username} ❓</i>\n"
                btn.button(text='➕ ' + channels.title,
                           url=f"{await channels.export_invite_link()}")
        btn.button(text=translator(text='♻  Check!',
                                   dest=lang),
                   callback_data=MainCallback(action="check_join",
                                              q='').pack())
        btn.adjust(1)
        await call.answer(text=text1,
                          reply_markup=btn.as_markup())
        await bot.send_message(chat_id=cid,
                               text=f"<b>{text}</b>",
                               reply_markup=btn.as_markup())
        await call.answer('You are not join channel')
    except Exception as err:
        logging.error(err)
