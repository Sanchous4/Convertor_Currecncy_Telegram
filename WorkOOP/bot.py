#!/usr/bin/env python3.8

import tokens_cnfg
from checker_cnfg import checker
from convertor_cnfg import convertor
import telebot
from telebot import types


class bot:
    """
    The class for discusion and  
    show results of checking class and converting class
    """

    # *THE CONSTRUCTOR
    def __init__(self, starter=False, lst_commands=["Start a conversion.", "Give some examples.", "Turn off the bot."]):
        """
        The constructor sets bool value for the bot starting  and the list of commands
        """
        self.starter = starter
        self.lst_commands = lst_commands

    # *THE BOT MAIN FUNCTION FOR CHATTING
    def start_bot(self):
        """
        The main function for the bot controlling 
        """

        # ?RESETTING FOR THE STARTER
        def ask_starter(x): return x == "y"

        self.starter = ask_starter(
            input("Are you sure to launch the bot?[y/n]"))
        print("Does it work:", self.starter)

        # ?BOT
        bot = telebot.TeleBot(tokens_cnfg.TOKEN)

        # ?/START - a command for greeting
        @bot.message_handler(commands=['start'])
        def welcome(message):

            # keyboard
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Start a conversion.")
            item2 = types.KeyboardButton("Give some examples.")

            markup.add(item1, item2)

            bot.send_message(
                message.chat.id,
                "Welcome, {0.first_name}!\nI'm <b>{1.first_name}</b>, a bot for currency conversions.".format(
                    message.from_user, bot.get_me()),
                parse_mode='html', reply_markup=markup)

        # ?/HELP - a command for displaying the instruction
        @bot.message_handler(commands=['help'])
        def welcome(message):

            # keyboard
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Start a conversion.")
            item2 = types.KeyboardButton("Turn off the bot.")

            markup.add(item1, item2)

            bot.send_message(
                message.chat.id,
                ("The bot have three commands:\n" +
                 "/start - greeting.\n" +
                 "/help  - displaying the instruction.\n" +
                 "/end   - the bot deactivation").format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

            bot.send_message(
                message.chat.id,
                ("If you want to make a conversation" +
                 " you should chat amount and symbol.").format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

            bot.send_message(
                message.chat.id,
                ("Some examples:\n100 USDT/BTC.\n250 BTC/USD\n400 EUR/USD").format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

        # ?/END - a command for the bot deactivation
        @bot.message_handler(commands=['end'])
        def end(message):

            markup = types.ReplyKeyboardRemove(selective=False)

            bot.send_message(
                message.chat.id,
                "The bot has <b>turned off</b>.".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

            bot.stop_polling()
            self.starter = False

        # ?Processing other requests
        @bot.message_handler(content_types=['text'])
        def answer(message):

            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "Roger that, I'm processing your request.".format(
                message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

            if message.text in self.lst_commands:  # ?if it is command the suitable handler is activated
                if message.text == "Start a conversion.":
                    bot.send_message(message.chat.id, "Okay, you should chat an amount and a currency pair.".format(message.from_user,
                                                                                                                    bot.get_me()), parse_mode='html')

                elif message.text == "Turn off the bot.":
                    bot.send_message(message.chat.id, "The bot has <b>turned off</b>".format(message.from_user,
                                                                                             bot.get_me()), parse_mode='html')

                    bot.stop_polling()
                    self.starter = False

                else:  # "Give some examples."
                    # keyboard
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("Start a conversion.")
                    item2 = types.KeyboardButton("Turn off the bot.")

                    markup.add(item1, item2)

                    bot.send_message(message.chat.id,
                                     ("Some examples:\n100 USDT/BTC.\n250 BTC/USD\n400 EUR/USD").format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

                    bot.send_message(message.chat.id,
                                     ("More detail information - /help").format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

            else:
                bot.send_message(message.chat.id, "Got it, now I'm checking and converting.".format(message.from_user,
                                                                                                    bot.get_me()), parse_mode='html')

                obj_checker = checker(0, "", "")
                amount, curr_1, curr_2 = obj_checker.checker(message.text)

                if amount == "0" and curr_1 == "0" and curr_2 == "0":
                    bot.send_message(message.chat.id, "<b>Error</b>, you've chatted improper request, pls, repeat it.".format(message.from_user,
                                                                                                                              bot.get_me()), parse_mode='html')

                else:
                    obj_convertor = convertor(curr_1, curr_2)
                    res_1, res_2 = obj_convertor.convertor()

                    if res_1 == "-1" and res_2 == "-1":
                        bot.send_message(message.chat.id, "<b>Error</b> of connection".format(message.from_user,
                                                                                              bot.get_me()), parse_mode='html')

                    elif res_1 == "-3" and res_2 == "-3":
                        bot.send_message(message.chat.id, "<b>The pair</b> hasn't looked for.".format(message.from_user,
                                                                                                      bot.get_me()), parse_mode='html')

                    elif res_1 == "-2" and res_2 == "-2":
                        bot.send_message(message.chat.id, f"<b>The good joke</b>, answer = {amount} :)".format(message.from_user,
                                                                                                               bot.get_me()), parse_mode='html')

                    elif (res_1 == "0" or res_1 == "1") and res_2 != "0" and res_2 != "1":
                        result_ = str(1/float(res_2)*float(amount))

                        if res_1 == "0":
                            obj_usdt = obj_convertor.usdt(1)
                            print(result_)
                            result_ = str(((obj_usdt*0.01)+1) /
                                          float(res_2)*float(amount))
                            print(result_)

                        str_ = curr_1 + "/" + curr_2 + " = " + result_
                        bot.send_message(message.chat.id, str_.format(message.from_user,
                                                                      bot.get_me()), parse_mode='html')
                    elif res_1 != "0" and res_1 != "1" and (res_2 == "0" or res_2 == "1"):
                        result_ = str(float(res_1)*float(amount))

                        if res_2 == "0":
                            obj_usdt = obj_convertor.usdt(float(result_))
                            print(result_)
                            result_ = str(obj_usdt + 0.01)
                            print(result_)

                        str_ = curr_1 + "/" + curr_2 + " = " + result_
                        bot.send_message(message.chat.id, str_.format(message.from_user,
                                                                      bot.get_me()), parse_mode='html')
                    else:
                        result_ = str(float(res_1)/float(res_2)*float(amount))
                        str_ = curr_1 + "/" + curr_2 + " = " + result_
                        bot.send_message(message.chat.id, str_.format(message.from_user,
                                                                      bot.get_me()), parse_mode='html')

                    del obj_convertor
                    
                del obj_checker
        # LAUNCH
        if (self.starter):
            bot.polling()
        else:
            bot.stop_polling()

    def end_bot(self):
        print("A value of the starter:", self.starter)


bot_obj = bot()

bot_obj.start_bot()
bot_obj.end_bot()

del bot_obj
