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
                self.bot.chat(f"/warp {last_wrd}")
                #BOTCMDWARP WARP <LOCATION>
                #bot types in chat 
                #"/warp <LOCATION>"
    
        
        @On(self.bot, "health")
        def health(this):
            if self.bot.food < 6:
                #Hold any foot item
                try:
                    self.bot.consume()
                except Exception as e:
                    print(f"Error consuming food: {e}")

        @On(self.bot, "entityMoved")
        def entityMoved(this, entity):
            """
            This will check for when entitites move, we will check if it is the desired player, if so the bot will follow like a good puppy.
            """
            follow_leaders = ["oujiderebf"]
            if entity.type == "player":
                if entity.username in follow_leaders:
                    self.bot.pathfinder.setGoal(movePlugin.goals.GoalFollow(entity, 1))


        @On(self.bot, "end")
        def end(this, reason):
            print(f"Disconnected: {reason}")

            # Turning Off listeners
            events = ["login", "kicked", "messagestr", "health", "end"]
            for event in events:
                off(self.bot, event, locals()[event])

            if self.reconnect:
                print("RESTARTING")
                self.start_bot()


    #Reads a sign with plain text

    def find_signs(self):
        #might need to use block ID
        signs = self.bot.findBlocks(match=lambda block: block.name.endswith("sign"))

        for sign in signs:
            sign_val = self.read_sign(sign)
            if sign_val ==  None:
                parsed_sign = self.chestShopParser(sign_val)
                if parsed_sign is not None:
                    print(f"Parsed sign: {parsed_sign}")
                else:
                    print("Invalid sign format")

    def chestShopParser(sign_text):
        lines = sign_text.split("\n")
        if len(lines) != 4:
            return None  # Invalid format

        name = lines[0].strip()
        amount = lines[1].strip()
        prices = lines[2].strip()
        item = lines[3].strip()

        # Validate amount (must be a positive integer)
        if not amount.isdigit() or int(amount) <= 0:
            return None

        # Validate prices (must follow "B <buy_price>:<sell_price> S" or similar)
        buy_price = None
        sell_price = None
        if "B" in prices:
            try:
                buy_price = float(prices.split("B")[1].split(":")[0].strip())
            except (IndexError, ValueError):
                return None
        if "S" in prices:
            try:
                sell_price = float(prices.split("S")[1].strip())
            except (IndexError, ValueError):
                return None

        # Validate item (must not be empty)
        if not item:
            return None

        return {
            "name": name,
            "amount": int(amount),
            "buy_price": buy_price,
            "sell_price": sell_price,
            "item": item
        }