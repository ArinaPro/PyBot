import json
import os
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ParseMode

# TOKEN = os.getenv("TOKEN")
TOKEN = "6266545260:AAH3YVuWNxf8nPqHU3ko8HAEbwWga3mDj38"
ADMINS = [0000000000]
img_dir = r"resources\\"
lang_dir = r"lang\\"

keys = []
test_step = 0
faculties = {
    "Griffindor": 0,
    "Slytherin": 0,
    "Ravenclau": 0,
    "Huffelpuf": 0
}


async def on_start_bot(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand(command="go", description="start quis"),
            types.BotCommand(command="setlang", description="Set language.")
        ]
    )

def setlang(file_name: str):
    with open(lang_dir + file_name, "r", encoding="utf-8") as f:
        data = f.read()
    return json.loads(data)


langFiles = os.listdir(lang_dir)
__lang = setlang("ua.txt")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# @dp.message_handler(commands="go")
# async def start(message: types.Message):
#     for q, a in test.items():
#         faculty_choise = InlineKeyboardMarkup()
#         for i in a:
#             button = InlineKeyboardButton(text=i, callback_data=i)
#             faculty_choise.add(button)
#         await message.answer(
#             text=q,
#             reply_markup=faculty_choise)


@dp.message_handler(commands="go")
async def start(message: types.Message):
    global test_step
    global faculties
    global __lang
    test_step = 0
    faculties = {
        "Gryffindor": 0,
        "Slytherin": 0,
        "Ravenclaw": 0,
        "Hufflepuff": 0
    }
    question = __lang["test"]["q" + str(test_step + 1)]

    await bot.send_photo(message.chat.id, photo=open(img_dir + question["img"], 'rb'))

    faculty_choise = InlineKeyboardMarkup()
    ind = 0
    for i in question["opt"]:
        button = InlineKeyboardButton(text=i, callback_data=str(ind) + "_0")
        faculty_choise.add(button)
        ind += 1
    await message.answer(text=question["q"], reply_markup=faculty_choise)


@dp.callback_query_handler()
async def testQuiz(callback_query: types.CallbackQuery, state: FSMContext):
    global test_step
    global faculties

    question = __lang["test"]["q" + str(test_step + 1)]

    p = question["p"]
    ind = int(callback_query.data.split("_")[0])
    indQ = int(callback_query.data.split("_")[1])
    if indQ == test_step:
        if p[ind] == '1':
            faculties["Ravenclaw"] += 1
        if p[ind] == '2':
            faculties["Gryffindor"] += 1
        if p[ind] == '3':
            faculties["Hufflepuff"] += 1
        if p[ind] == '4':
            faculties["Slytherin"] += 1

        test_step += 1

        if test_step == len(__lang["test"]):
            await callback_query.message.answer(text=__lang["resault"]["1"][0])
            await callback_query.message.answer(text=__lang["resault"]["1"][1])
            time.sleep(2.5)
            res = [faculties["Gryffindor"], faculties["Slytherin"], faculties["Ravenclaw"], faculties["Hufflepuff"]]
            max_value = max(res)
            max_count = res.count(max_value)

            if max_count > 1:
                global keys
                keys = []
                text = ""
                for i, v in faculties.items():
                    if v == max_value:
                        keys.append(i)
                        if text != "":
                            text += __lang["answers"][3] + i
                        else:
                            text += i
                await callback_query.message.answer(text=f"{__lang['answers'][2]} {text}")
                time.sleep(3)

                faculty_choice = InlineKeyboardMarkup(one_time_keyboard=True)
                button = InlineKeyboardButton(text=__lang["answers"][4] + keys[0] + __lang["answers"][5],
                                              callback_data="0")
                faculty_choice.add(button)
                button = InlineKeyboardButton(text=__lang["answers"][4] + keys[1] + __lang["answers"][5],
                                              callback_data="1")
                faculty_choice.add(button)
                if max_count > 2:
                    button = InlineKeyboardButton(text=__lang["answers"][4] + keys[2] + __lang["answers"][5],
                                                  callback_data="2")
                    faculty_choice.add(button)
                if max_count == 4:
                    button = InlineKeyboardButton(text=__lang["answers"][4] + keys[3] + __lang["answers"][5],
                                                  callback_data="3")
                    faculty_choice.add(button)
                await state.set_state("final_result")
                await callback_query.message.answer(text=__lang["answers"][6], reply_markup=faculty_choice,
                                                    parse_mode=ParseMode.HTML)

            else:
                if max(res) == res[0]:
                    await bot.send_photo(callback_query.message.chat.id,
                                         photo=open(img_dir + __lang["resault"]["img"][0], 'rb'))
                    await callback_query.message.answer(text=__lang["resault"]["text"][0])

                elif max(res) == res[1]:
                    await bot.send_photo(callback_query.message.chat.id,
                                         photo=open(img_dir + __lang["resault"]["img"][1], 'rb'))
                    await callback_query.message.answer(text=__lang["resault"]["text"][1])

                elif max(res) == res[2]:
                    await bot.send_photo(callback_query.message.chat.id,
                                         photo=open(img_dir + __lang["resault"]["img"][2], 'rb'))
                    await callback_query.message.answer(text=__lang["resault"]["text"][2])

                elif max(res) == res[3]:
                    await bot.send_photo(callback_query.message.chat.id,
                                         photo=open(img_dir + __lang["resault"]["img"][3], 'rb'))
                    await callback_query.message.answer(text=__lang["resault"]["text"][3])

        else:
            question = __lang["test"]["q" + str(test_step + 1)]

            await bot.send_photo(callback_query.message.chat.id, photo=open(img_dir + question["img"], 'rb'))

            faculty_choice = InlineKeyboardMarkup()
            ind = 0
            for i in question["opt"]:
                text_on_b = i
                button = InlineKeyboardButton(text=text_on_b, callback_data=str(ind) + "_" + str(test_step))
                faculty_choice.add(button)
                ind += 1
            await callback_query.message.answer(text=question["q"], reply_markup=faculty_choice)


@dp.callback_query_handler(state="final_result")
async def want1(query: types.CallbackQuery, state: FSMContext):
    faculties[keys[int(query.data)]] += 1
    res = [faculties["Gryffindor"], faculties["Slytherin"], faculties["Ravenclaw"], faculties["Hufflepuff"]]
    if max(res) == res[0]:
        await bot.send_photo(query.message.chat.id,
                             photo=open(img_dir + __lang["resault"]["img"][0], 'rb'))
        await query.message.answer(text=__lang["resault"]["text"][0])

    elif max(res) == res[1]:
        await bot.send_photo(query.message.chat.id,
                             photo=open(img_dir + __lang["resault"]["img"][1], 'rb'))
        await query.message.answer(text=__lang["resault"]["text"][1])

    elif max(res) == res[2]:
        await bot.send_photo(query.message.chat.id,
                             photo=open(img_dir + __lang["resault"]["img"][2], 'rb'))
        await query.message.answer(text=__lang["resault"]["text"][2])

    elif max(res) == res[3]:
        await bot.send_photo(query.message.chat.id,
                             photo=open(img_dir + __lang["resault"]["img"][3], 'rb'))
        await query.message.answer(text=__lang["resault"]["text"][3])
    await state.finish()


@dp.message_handler(commands="setLang")
async def start(message: types.Message, state=FSMContext):
    global __lang
    getLangs()
    lang_choice = InlineKeyboardMarkup()
    for i in langFiles:
        if i.find('.txt') != -1:
            i = i.replace('.txt', '')
            button = InlineKeyboardButton(text=i, callback_data=i + '.txt')
            lang_choice.add(button)
    await state.set_state("change_lang")
    await message.reply(text=__lang["answers"][7], reply_markup=lang_choice)


@dp.callback_query_handler(lambda query: query.data.endswith(".txt"), state="change_lang")
async def change_lang(query: types.CallbackQuery, state: FSMContext):
    global __lang
    file_name = query.data
    with open(lang_dir + file_name, "r", encoding="utf-8") as f:
        data = f.read()
    __lang = json.loads(data)
    await state.finish()
    await query.answer(__lang.get("answers")[0] + file_name.split(".")[0])


def getLangs():
    global langFiles
    langFiles = os.listdir(lang_dir)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_start_bot)
