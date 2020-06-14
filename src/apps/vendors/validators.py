from helpers.validators_msg import *

# name validation
NAME_MAX_LEN = 50
NAME_MAX_LEN_MSG = max_len_msg( NAME_MAX_LEN)

NAME_MIN_LEN = 3
NAME_MIN_LEN_MSG = min_len_msg( NAME_MIN_LEN)

NAME_NULL_CHAR_MSG = NULL_CHAR_MSG

# CNPJ validation
CNPJ_REGEX = r'^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$'
CNPJ_REGEX_MSG = "CNPJ should be in the standard format."

# city validation
CITY_MAX_LEN = 50
CITY_MAX_LEN_MSG = max_len_msg( CITY_MAX_LEN)

CITY_MIN_LEN = 3
CITY_MIN_LEN_MSG = min_len_msg( CITY_MIN_LEN)

CITY_NULL_CHAR_MSG = NULL_CHAR_MSG