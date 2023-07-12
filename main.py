from gin_rummy import GinRummy
from player import Bot

if __name__ == '__main__':
    # Create a Gin Rummy game instance
    game = GinRummy()

    # Create a bot player and add it to the game
    bot = Bot(game)
    game.set_bot(bot)

    # Start the game
    game.play()
