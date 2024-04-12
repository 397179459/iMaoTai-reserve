"""
Personal information protection
from: https://github.com/397179459/iMaoTai-reserve/pull/52
"""

def shadow(mobile: str):
    length = len(mobile)
    hidden_length = (length+1)//3
    first_length = (length - hidden_length)//2
    last_length = length - first_length - hidden_length

    return mobile[:first_length]+'*'*hidden_length+mobile[-last_length:]