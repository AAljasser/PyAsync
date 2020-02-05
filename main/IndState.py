from enum import Enum

class IndState:
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
            re = [x.strip() for x in re]
        else:
            re.append(rData.strip())
        return re