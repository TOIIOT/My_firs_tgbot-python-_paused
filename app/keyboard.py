from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="случайные картинки животных")],
                                      [KeyboardButton(text="помощь"),
                                       KeyboardButton(text="о проекте")]],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите команду")


catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="котики", callback_data="cat")],
                                                [InlineKeyboardButton(text="лисы", callback_data="fox")],
                                                [InlineKeyboardButton(text="собаки", callback_data="dog")]])


get_gender = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="мужской")],
                                        [KeyboardButton(text="женский")]],
                                        resize_keyboard=True)