from javascript import require, On, off
from src.bot import MCbot
from src.helper import clone_MCData
mineflayer = require('mineflayer')


if __name__ == "__main__":
    clone_MCData("1.19")

    bot = MCbot('tester')
