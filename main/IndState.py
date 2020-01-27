from enum import Enum

class IndState:
    TERMINATE_CONN = -2
    INCORRECT_INPUT = -1
    LOGIN = 0
    A_MENU = 1
    S_MENU = 2
    P_MENU = 3