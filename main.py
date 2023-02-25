import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# Telegram bot tokenini girin
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

# OpenAI API anahtarını girin
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"

# OpenAI engine adını girin
OPENAI_ENGINE = "davinci"

# OpenAI engine yardım metnini girin
OPENAI_HELP_TEXT = (
    "I am a language model created by OpenAI. I can answer many types of questions, "
    "write creative stories and poems, and even translate between languages! "
    "Just type your question or prompt and I will do my best to provide a helpful response."
)

# Telegram bot günlüklerinin seviyesini ayarlayın
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI API anahtarını ayarlayın
openai.api_key = OPENAI_API_KEY

# OpenAI motorunu ayarlayın
engine = openai.CompletionEngine(api_key=OPENAI_API_KEY, engine=OPENAI_ENGINE)


def start(update: Update, context: CallbackContext) -> None:
    """Telegram botu başlatma komutunu işleyin"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=OPENAI_HELP_TEXT)


def message(update: Update, context: CallbackContext) -> None:
    """Telegram mesajlarını işleyin"""
    message = update.effective_message
    text = message.text
    chat_id = message.chat_id

    # OpenAI API'ye sorgu gönderin
    response = engine.complete(prompt=text, max_tokens=1024)
    message_text = response.choices[0].text.strip()

    # Yanıtı kullanıcıya gönderin
    context.bot.send_message(chat_id=chat_id, text=message_text)


def main() -> None:
    """Telegram botunu başlatın"""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Telegram komutlarını işleyin
    dispatcher.add_handler(CommandHandler("start", start))

    # Telegram mesajlarını işleyin
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))

    # Telegram botunu başlatın
    updater.start_polling()

    # Botu çalışır durumda tutun
    updater.idle()


if __name__ == '__main__':
    main()
