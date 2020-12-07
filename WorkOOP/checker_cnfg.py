class checker():
    """
    The class for requests' checking and their formating 
    """

    # *THE CONSTRUCTOR
    def __init__(self, amount=0, curr_pair_1="", curr_pair_2=""):
        """
        The constructor sets an amount, a 1-st currency to USD/USDT and, the 2-nd one 
        """
        self.amount = amount
        self.curr_pair_1 = curr_pair_1
        self.curr_pair_2 = curr_pair_2

    def checker(self, message):
        """
        The function for the checking
        """

        str_digit = ""
        message = message.upper()

        i_alpha = 0

        for x in message:
            if x.isdigit():
                str_digit += x
            elif x == "." or x == ",":
                str_digit += "."
            elif x.isalpha() or x == "/":
                self.curr_pair_1 += x
                if x == "/":
                    i_alpha += 1

        try:
            self.amount = float(str_digit)
        except Exception as e:
            self.amount = -1

        if self.amount == -1 or len(self.curr_pair_1) < 7 or len(self.curr_pair_1) > 9 or i_alpha != 1 or self.curr_pair_1[0] == "/" or self.curr_pair_1[-1] == "/":
            return "0", "0", "0"

        else:
            str_1 = ""
            str_2 = ""

            i = 0
            while i < len(self.curr_pair_1):
                if self.curr_pair_1[i] != "/" and i < 4:
                    str_1 += self.curr_pair_1[i]
                elif self.curr_pair_1[i] != "/":
                    str_2 += self.curr_pair_1[i]
                i += 1

            self.curr_pair_1 = str_1
            self.curr_pair_2 = str_2

            print(len(self.curr_pair_1), len(self.curr_pair_2))
            return str_digit, self.curr_pair_1, self.curr_pair_2
