import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import config


private_key = config.PRIVATE_AES_KEY  # 你的密钥
private_key_b = sha256(private_key.encode()).digest()  # 使用SHA-256算法生成一个32字节的密钥


def encrypt_aes_ebc(plain_str, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plain_str.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode()


def decrypt_aes_ebc(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_ECB)
    plain_str = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plain_str.decode()


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


# 要加密的明文
t_plain_str = '666'
t_plain_str1 = '888'

# 加密
t_ciphertext = encrypt_aes_ebc(t_plain_str, private_key_b)
print(t_plain_str + "加密后的密文:", t_ciphertext)

t_ciphertext1 = encrypt_aes_ebc(t_plain_str1, private_key_b)
print(t_plain_str1 + "加密后的密文:", t_ciphertext1)

# 解密
t_decrypted_plain_str = decrypt_aes_ebc(t_ciphertext, private_key_b)
print("解密后的明文:", t_decrypted_plain_str)

t_decrypted_plain_str1 = decrypt_aes_ebc(t_ciphertext1, private_key_b)
print("解密后的明文:", t_decrypted_plain_str1)



