from javascript import require, On, off
mineflayer = require('mineflayer')


class MCbot:
    def __init__(self, bot_name):
        self.bot_args = {
            "host": "localhost",
            "port": 3000,
            "version": "1.19.4",
            "username": bot_name,
            "hiddenErrors": False
        }
        self.reconnect = True
        self.bot_name = bot_name
        self.bot = mineflayer.createBot(self.bot_args)
        self.start_bot()

    # Event Listeners
    def start_bot(self):
        # Create the bot instance
        print("starting bot")
        self.start_events()

    def start_events(self):
        @On(self.bot, "login")
        def login(this):
            self.bot_socket = self.bot._client.socket
            print(f"Logged in to {self.bot_socket.server if self.bot_socket.server else self.bot_socket.host}")

        @On(self.bot, "spawn")
        def spawn(bot):
            print("Has spawned")

        @On(self.bot, "kicked")
        def kicked(bot, reason, loggedIn):
            if loggedIn:
                print(f"Kicked from server: {reason}")
            else:
                print(f"Kicked from server while connecting: {reason}")

        @On(self.bot, "messagestr")
        def messagestr(this, message, messageposition):
            if messageposition == "chat" and "quit" in message:
                self.reconnect = False
                this.quit()
        
        @On(self.bot, "death")
        def death(this):
            self.respawn()

        @On(self.bot, "end")
        def end(this, reason):
            print(f"Disconnected: {reason}")

            # Turning Off listeners
            off(self.bot, "login", login)
            off(self.bot, "kicked", kicked)
            off(self.bot, "messagestr", messagestr)
            off(self.bot, "end", end)

            if self.reconnect:
                print("RESTARTING")
                self.start_bot()
