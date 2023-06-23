def main():
    from core import bot 

    TOKEN = '5963564841:AAF1HMsgUWQ-NTXxW1aFAd-gk6Jm8sn9epM'
    bot = bot.Bot(TOKEN)
    bot.infinity_polling()

if __name__ == '__main__':
    main() 
