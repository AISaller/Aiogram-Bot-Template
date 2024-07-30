import logging
from loader import dp
from aiogram import types
from keyboards.inline.button import AdminCallback
from keyboards.inline.close_btn import close_btn
from aiogram import F
from aiogram.fsm.context import FSMContext
from states.admin_state import AdminState
from filters.admin import SelectAdmin, IsAdmin
from function.translator import translator


@dp.callback_query(AdminCallback.filter(F.action == "send_advertisement"), IsAdmin())
async def send_ads(call: types.CallbackQuery, state: FSMContext):
    try:
        user_id = call.from_user.id
        message_id = call.message.message_id
        language = call.from_user.language_code
        is_admin = SelectAdmin(cid=user_id)

        if is_admin.send_message():
            await state.set_state(AdminState.send_ads)
            text = translator(
                text="<b><i>Send the advertisement...</i></b>",
                dest=language
            )
            await state.update_data({"message_id": call.message.message_id})
        else:
            text = translator(
                text="<b>❌ Unfortunately, you do not have this permission!</b>",
                dest=language
            )

        await call.message.edit_text(
            text=text,
            reply_markup=close_btn()
        )
        await state.update_data({"message_id": message_id})

    except Exception as err:
        logging.error(err)

