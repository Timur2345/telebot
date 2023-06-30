def main():
    from core import bot

    TOKEN = '6021833536:AAF8QImHwLutniT8TW9UgoFUA17Nqgh6cMg'
    bot = bot.Bot(TOKEN)
    bot.infinity_polling()


if __name__ == '__main__':
    main()
