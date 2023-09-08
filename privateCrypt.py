import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import config
import logging


def get_aes_key():
    """
    获取config中你的AES私钥
    :return:
    """
    private_key = config.PRIVATE_AES_KEY  # 你的私钥
    if private_key is None:
        logging.error("!!!!请配置config.py中PRIVATE_AES_KEY(AES的私钥)")
        raise ValueError
    private_key_b = sha256(private_key.encode()).digest()  # 使用SHA-256算法生成一个32字节的密钥
    return private_key_b


def encrypt_aes_ecb(plain_str, key):
    """
    无偏移的AES加密
    :param plain_str: 需要加密的明文
    :param key: AES私钥
    :return: base64后的密文
    """
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plain_str.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode()


def decrypt_aes_ecb(ciphertext, key):
    """
    无偏移的AES解密
    :param ciphertext: 需要解密的密文
    :param key: AES私钥
    :return: 解密后的明文
    """
    ciphertext = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_ECB)
    plain_str = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plain_str.decode()


'''
def encrypt_aes_cbc(plain_str, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plain_str, AES.block_size))
    iv = cipher.iv
    return base64.b64encode(iv + ciphertext).decode()


def decrypt_aes_cbc(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_str = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plain_str
'''
