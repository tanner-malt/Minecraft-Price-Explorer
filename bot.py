from javascript import require, On, off
mineflayer = require('mineflayer')
movePlugin = require('mineflayer-pathfinder')
vec3 = require('vec3')
Entity = require("prismarine-entity")('1.19')
enums = require('minecraft-data')

MCVersionData = enums("1.19")


class MCbot:
    def __init__(self, bot_name):
        self.bot_args = {
            "host": "localhost",
            "port": 3000,
            "username": bot_name,
            "hiddenErrors": False,
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
        def messagestr(this, message: str, messageposition, *args):            
            """
            This will look in chat whenever there is a message, and look for the token #BOTCMDWARP, and then parse the message accordingly
            """
            if messageposition == "chat" and "#BOTCMDWARP" in message and "oujiderebf" in message:
                words = message.split(" ")
                last_wrd = words[-1]
                self.bot.chat(f"warp {last_wrd}")
                #BOTCMDWARP WARP <LOCATION>
                #bot types in chat 
                #"/warp <LOCATION>"
    
        
        @On(self.bot, "health")
        def health(this):
            if self.bot.food < 6:
                #Hold any foot item
                self.bot.consume()

        @On(self.bot, "entityMoved")
        def entityMoved(this, entity):
            """
            This will check for when entitites move, we will check if it is the desired player, if so the bot will follow like a good puppy.
            """
            follow_leaders = ["oujiderebf"]
            if entity.type == "player":
                if entity.username in follow_leaders:
                    #entity.position

                    pass


        @On(self.bot, "end")
        def end(this, reason):
            print(f"Disconnected: {reason}")

            # Turning Off listeners
            off(self.bot, "login", login)
            off(self.bot, "kicked", kicked)
            off(self.bot, "messagestr", messagestr)
            off(self.bot, "health",health)
            off(self.bot, "end", end)

            if self.reconnect:
                print("RESTARTING")
                self.start_bot()


    #Reads a sign with plain text

    def read_sign(block):
        return block.getSignText()
    
    def find_signs(self):
        #might need to use block ID
        signs = self.bot.findBlocks(match = "sign")

        for sign in signs:
            print(self.read_sign(sign))

    def chestShopParser(sign_text):
        # Chest Shop format
        # 1st Line Name
        # 2nd Line amount of item
        # 3rd Line, B 10 : S 5 is buy for 10, sell for 5
        # 4th line, item name
        pass