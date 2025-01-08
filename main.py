from javascript import require, On, off
from bot import MCbot
mineflayer = require('mineflayer')


if __name__ == "__main__":
    bot = MCbot("tester")

    bot_args = {
            "host": "localhost",
            "port": 3000,
            "version": "1.19.4",
            "username": "hater",
            "hiddenErrors": False
        }
    bot2 = mineflayer.createBot(bot_args)
    bot.start_bot()
