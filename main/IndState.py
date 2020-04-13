from enum import Enum
'''
Helper Class
'''
class IndState:
    BOOK_NF = -4
    DUPLICATE_ERR = -3
    TERMINATE_CONN = -2
    INCORRECT_INPUT = -1
    LOGIN = 0
    A_MENU = 1
    S_MENU = 2
    P_MENU = 3

    def breakData(rData):
        re = [] # We are always sending a list back
        if ',' in rData:
            re =rData.split(',')
        else:
            re.append(rData.strip())
        return re