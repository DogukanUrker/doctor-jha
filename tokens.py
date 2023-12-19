account_sid = "ACd343473d794bb7afea2f149fc4d18de5"
auth_token = "0e18b7c5846422040ee94f011d71e41f"

import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

print(carrier._is_mobile(number_type(phonenumbers.parse("+90 551 185 85 36"))))
