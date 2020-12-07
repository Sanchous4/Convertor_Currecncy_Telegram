
import tokens_cnfg
import telebot
from fxcmpy import fxcmpy
from binance.client import Client

from telebot import types

try:
    print("Please, wait for the connection to FXCM.")
    client_FXCM = fxcmpy(access_token=tokens_cnfg.API_KEY_FXCM, server="demo")
    print("Is connected to FXCM: ", client_FXCM.is_connected())
except Exception as e:
    lst_bnb = 0
    print(e)

lst_fxcm = list(client_FXCM.get_instruments())
for x in lst_fxcm:
    if x == ("TYU" + "/USD"):
        print(x == ("TYU" + "/USD"), lst_fxcm[i])




# client_FXCM.subscribe_market_data('EUR/USD')
# str_ = str(client_FXCM.get_prices('EUR/USD')
#            ).replace('Bid      Ask     High      Low\n', '')

# i = 0
# while str_[i] != '.':
#     i += 1

# while str_[i] != ' ':
#     i += 1

# str_ = str_[i:]

# str_2 = ""
# bid = 0
# ask = 0
# high = 0
# low = 0
# for x in (str_+"  "):
#     if x == '.' or x.isdigit():
#         str_2 += x
#     else:
#         if str_2 != "":
#             if bid == 0:
#                 bid = float(str_2)
#             elif ask == 0:
#                 ask = float(str_2)
#             elif high == 0:
#                 high = float(str_2)
#             elif low == 0:
#                 low = float(str_2)
#         str_2 = ""

# print(str_)
# print(bid, ask, high, low)
client_FXCM.close()

# try:
#     print("Please, wait for the connection to Binance.")
#     client_BNB = Client(tokens_cnfg.API_KEY_BNB, tokens_cnfg.SECRET_API_KEY_BNB)
#     print("Is connected to Binance: ", len(client_BNB.get_account()) > 0)
# except Exception as e:
#     print(e)


