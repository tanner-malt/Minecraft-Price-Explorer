import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from javascript import require, On, off
from bot import MCbot
from helper import clone_MCData
mineflayer = require('mineflayer')


if __name__ == "__main__":
    clone_MCData("1.19")

    bot = MCbot('tester')
