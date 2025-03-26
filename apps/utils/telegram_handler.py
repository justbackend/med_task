import logging
import os

import requests

telegram_bot_token = os.environ.get("BUGS_BOT_TOKEN")
telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")


class TelegramErrorHandler(logging.Handler):
    def emit(self, record):
        """Custom logging handler that sends error logs to a specified Telegram chat.

        This handler captures log records at specified logging levels and sends them
        as formatted messages to a Telegram chat using a Telegram bot. The bot is
        configured via environment variables containing the bot token and chat ID.
        """

        if not telegram_chat_id or not telegram_bot_token:
            return

        log_entry = self.format(record)
        message = f"*Your_Project_Name* Error 500*\n\n```\n{log_entry}\n```"

        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        data = {"chat_id": telegram_chat_id, "text": message, "parse_mode": "html"}

        try:
            response = requests.post(url, data=data, timeout=5)

            response_data = response.json()

            if not response_data.get("ok"):
                logging.error("Telegram API error: %s", response_data.get("description"))

        except requests.exceptions.RequestException:
            logging.exception("Failed to send error log to Telegram")
