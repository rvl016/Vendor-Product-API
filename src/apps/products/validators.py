from helpers.validatorsMsg import *

# name validation
NAME_MAX_LEN = 50
NAME_MAX_LEN_MSG = maxLenMsg( NAME_MAX_LEN)

NAME_MIN_LEN = 3
NAME_MIN_LEN_MSG = minLenMsg( NAME_MIN_LEN)

NAME_NULL_CHAR_MSG = NULL_CHAR_MSG

# code validation
CODE_REGEX = r'^(?=.*0)[0-9]{12}$'
CODE_REGEX_MSG = "Product code should follow the UPC-A standard format."
