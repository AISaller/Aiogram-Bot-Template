import logging
from loader import dp, bot, db
from aiogram import types
from keyboards.inline.close_btn import close_btn
from keyboards.inline.admin_btn import block_user
from filters.admin import IsAdmin, SelectAdmin
from aiogram.fsm.context import FSMContext
from function.translator import translator
from states.admin_state import AdminState


@dp.message(AdminState.check_user, IsAdmin())
async def attach_user(msg: types.Message, state: FSMContext):
    try:
        cid = msg.from_user.id
        mid = msg.message_id
        lang = msg.from_user.language_code
        is_admin = SelectAdmin(cid=cid)
        user_id = int(msg.text)
        btn = close_btn()
        text = translator(text="🔴 Something went wrong!\n",
                          dest=lang)
        if is_admin.block_user():
            data_state = await state.get_data()
            try:
                user = await bot.get_chat(chat_id=user_id)
                check = db.check_user_ban(cid=user_id)
                check1 = db.check_user(cid=user_id)
                if check1 is not None:
                    btn = block_user(cid=cid, user_id=user_id, lang=lang)
                    if check is None:
                        check2 = db.select_admin(cid=user_id)
                        select_user = db.check_user(cid)
                        if check2 is None:
                            text = "✅ User unblocked!"
                            text += translator(text=f'\n\nUsername: @',
                                               dest=lang)
                            text += user.username
                            text += translator(text='\nLanguage code: ',
                                               dest=lang)
                            text += f'{select_user[3]}'
                        else:
                            tx = "✅ User blocked!\n" \
                                 "👮‍♂️ User is in the list of admins!</b>"
                            text = translator(text=f'{tx}\n\nUsername: @',
                                              dest=lang)
                            text += user.username
                            text += translator(text='<b>\nLanguage code:</b> ',
                                               dest=lang)
                            text += f'<i>{select_user[3]}</i>'
                    else:
                        tx = "✅ User blocked!\n Date:"
                        text = translator(text=f'{tx} {check[3]}\n\nUsername: @',
                                          dest=lang)
                        text += user.username
                else:
                    text = (translator(text="🔴 User not found!\n"
                                            "The user may not be in the bot's list..",
                                       dest=lang))
            except Exception as err:
                logging.error(err)
                text = translator(text="🔴 User not found!\n"
                                       "The bot may not have found the user..",
                                  dest=lang)
            finally:
                await bot.edit_message_text(chat_id=cid,
                                            message_id=data_state['message_id'],
                                            text=f'<b><i>{text}</i></b>',
                                            reply_markup=btn)
        else:
            text = translator(text='❌ Unfortunately, you do not have this right!',
                              dest=lang)
        await bot.edit_message_text(chat_id=cid,
                                    message_id=mid,
                                    text=f'<b><i>{text}</i></b>',
                                    reply_markup=btn)
        await state.update_data({
            "message_id": mid
        })
        await bot.delete_message(chat_id=cid,
                                 message_id=mid)
    except Exception as err:
        logging.error(err)
