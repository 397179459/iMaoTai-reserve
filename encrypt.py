from Crypto.Cipher import AES
import base64


class Encrypt:
    def __init__(self, key, iv):
        self.key = key.encode('utf-8')
        self.iv = iv.encode('utf-8')

    # @staticmethod
    def pkcs7padding(self, text):
        """明文使用PKCS7填充 """
        bs = 16
        length = len(text)
        bytes_length = len(text.encode('utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        self.coding = chr(padding)
        return text + padding_text

    def aes_encrypt(self, content):
        """ AES加密 """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # 处理明文
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def aes_decrypt(self, content):
        """AES解密 """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        content = base64.b64decode(content)
        text = cipher.decrypt(content).decode('utf-8')
        return text.rstrip(self.coding)


# if __name__ == '__main__':
#     key = 'ONxYDyNaCoyTzsp83JoQ3YYuMPHxk3j7'
#     iv = 'yNaCoyTzsp83JoQ3'
#
#     ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     p_json = {
#         "CompanyName": "testmall",
#         "UserId": "test",
#         "Password": "grasp@101",
#         "TimeStamp": "2019-05-05 10:59:26"
#     }
#     a = Encrypt(key=key, iv=iv)
#     e = a.aes_encrypt(json.dumps(p_json))
#     d = a.aes_decrypt(e)
#     print("加密:", e)
#     print("解密:", d)
