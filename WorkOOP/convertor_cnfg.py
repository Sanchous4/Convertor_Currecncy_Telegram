import tokens_cnfg
from fxcmpy import fxcmpy
from binance.client import Client


class convertor():
    """
    The class for connection to brokers
    """

    def __init__(self, curr_1="0", curr_2="0"):
        """
        The empty constructor
        """
        self.curr_1 = curr_1
        self.curr_2 = curr_2

    def convertor(self):
        """
        The function for connection to brokers
        """

        # ?CONNECTION
        con_bnb = 1
        con_fxcm = 1

        try:
            print("Please, wait for the connection to FXCM.")
            client_FXCM = fxcmpy(
                access_token=tokens_cnfg.API_KEY_FXCM, server="demo")
            print("Is connected to FXCM: ", client_FXCM.is_connected())
        except Exception as e:
            con_bnb = 0
            print(e)

        try:
            print("Please, wait for the connection to Binance.")
            client_BNB = Client(tokens_cnfg.API_KEY_BNB,
                                tokens_cnfg.SECRET_API_KEY_BNB)
            print("Is connected to Binance: ", len(
                client_BNB.get_account()) > 0)
        except Exception as e:
            con_fxcm = 0
            print(e)

        if con_bnb == 0 or con_fxcm == 0:
            print("Error of connection.")
            client_FXCM.close()
            return "-1", "-1"

        # ?LISTS' GETTING
        lst_bnb = list(client_BNB.get_all_tickers())
        lst_fxcm = list(client_FXCM.get_instruments())

        if (self.curr_1 == "USD" or self.curr_1 == "USDT") and (self.curr_2 == "USD" or self.curr_2 == "USDT"):
            client_FXCM.close()
            return "-2", "-2"

        i = 0
        fiat_request_ = True
        crypto_request_ = True
        lst_prices = [self.curr_1, self.curr_2]

        while i < 2 and (fiat_request_ or crypto_request_):
            fiat_request_ = True
            crypto_request_ = True

            # ?BINANCE

            if lst_prices[i] == "USD" or lst_prices[i] == "USDT":
                if lst_prices[i] == "USD":
                    lst_prices[i] = "1"
                else:
                    lst_prices[i] = "0"
                i += 1
                continue

            elif fiat_request_ == True and crypto_request_ == True:
                crypto_request_ = False

                for x in lst_bnb:
                    if (lst_prices[i]+"USDT") in x["symbol"]:
                        crypto_request_ = True

                print()

                if crypto_request_:
                    lst_prices[i] = dict(client_BNB.get_symbol_ticker(
                        symbol=(lst_prices[i]+"USDT")))["price"]

            # ?FXCM
            if crypto_request_ == False:
                fiat_request_ = False

                for x in lst_fxcm:
                    if x == (lst_prices[i] + "/USD"):
                        fiat_request_ = True

                if fiat_request_ == False:
                    print("The fiat currency doesn't exist.")

                else:
                    client_FXCM.subscribe_market_data(lst_prices[i] + "/USD")
                    str_ = str(client_FXCM.get_prices(lst_prices[i] + "/USD")
                               ).replace('Bid      Ask     High      Low\n', '')

                    i = 0
                    while str_[i] != '.':
                        i += 1

                    while str_[i] != ' ':
                        i += 1

                    str_ = str_[i:]

                    str_2 = ""
                    bid = 0
                    ask = 0
                    high = 0
                    low = 0
                    for x in (str_+"  "):
                        if x == '.' or x.isdigit():
                            str_2 += x
                        else:
                            if str_2 != "":
                                if bid == 0:
                                    bid = float(str_2)
                                elif ask == 0:
                                    ask = float(str_2)
                                elif high == 0:
                                    high = float(str_2)
                                elif low == 0:
                                    low = float(str_2)
                            str_2 = ""

                    print(str_)
                    print(bid, ask, high, low)
                    client_FXCM.unsubscribe_market_data(lst_prices[i] + "/USD")
                    lst_prices[i] = str((bid+ask)/2)

            i += 1

        if fiat_request_ == False and crypto_request_ == False:
            client_FXCM.close()
            return "-3", "-3"

        self.curr_1 = lst_prices[0]
        self.curr_2 = lst_prices[1]

        client_FXCM.close()
        return self.curr_1, self.curr_2

    class usdt():
        def __init__(self, usdt_1=0.0):
            self.usdt_1 = usdt_1
    
        def __add__(self, cm_usdt):
            '''
            Overloading adding up
            '''
            return self.usdt_1 + self.usdt_1*cm_usdt
    
        def __mul__(self, cm_usdt):
            '''
            Multiplication adding up
            '''
            return self.usdt_1*cm_usdt
