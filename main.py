from javascript import require, On, off


mineflayer = require('mineflayer')

bot_args =     {
        "username": "Simple-Bot",
        "host": "localhost",
        "port": 3000,
        "version": "1.19.4",
        "hiddenErrors": False
    }
bot = mineflayer.createBot(bot_args)

@On(bot, "login")
def login(this):
    bot_socket = bot._client.socket
    print(f"Logged in to {bot_socket.server if bot_socket.server else bot_socket.host}")

@On(bot, "kicked")
def kicked(this, reason, loggedIn):
    if loggedIn:
        print(f"Kicked from server: {reason}")
    else:
        print(f"Kicked from server while connecting: {reason}")

@On(bot, "messagestr")
def messagestr(this, message, messageposition):
    if messageposition == "chat" and "quit" in message:
        this.quit()

@On(bot, "end")
def end(this, reason):
    print(f"Disconnected: {reason}")

    #Turning Off listeners
    off(bot, "login",login)
    off(bot, "kicked", kicked)
    off(bot, "end", end)
    off(bot, "messagestr", messagestr)