import logging

from PyCharacterAI import get_client
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile

# HOW TO GET TOKEN: https://github.com/Xtr4F/PyCharacterAI#about-tokens-and-how-to-get-them
CHARACTER_AI_TOKEN = "123"
CHARACTER_AI_WEB_NEXT_AUTH = "123"

character_id = "123"
voice_id = "123"

BOT_TOKEN = "123"
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


@dp.message(Command(commands="vova"))
async def cmd_vova(m: Message, bot: Bot):
    char_client = await get_client(token=CHARACTER_AI_TOKEN)

    msg_parts = m.text.split()

    if len(msg_parts) < 2:
        await m.answer(
            "Будь ласка, напишіть своє повідомлення після команди. Наприклад:\n\n"
            "<code>/vova Мене сьогодні не буде на парах</code>"
        )
        return

    await bot.send_chat_action(chat_id=m.chat.id, action=ChatAction.RECORD_VOICE)

    message_text = " ".join(msg_parts[1:])
    message_text = f"Добрий день, я {m.from_user.full_name} {message_text}"
    chat, greeting_message = await char_client.chat.create_chat(character_id)

    answer = await char_client.chat.send_message(character_id, chat.chat_id, message_text)
    # answer_text = answer.get_primary_candidate().text

    await bot.send_chat_action(chat_id=m.chat.id, action=ChatAction.RECORD_VOICE)

    speech = await char_client.utils.generate_speech(
        chat.chat_id,
        answer.turn_id,
        answer.primary_candidate_id,
        voice_id
    )

    await m.answer_voice(
        BufferedInputFile(speech, filename="Відповідь Володимира Васильовича.mp3"),
        reply_to_message_id=m.message_id
    )


def main():
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
