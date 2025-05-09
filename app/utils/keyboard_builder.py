from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()

buttons = {
    ""
}

for index in range(1, 11):
    builder.button(text=f"Set {index}", callback_data=f"set:{index}")
