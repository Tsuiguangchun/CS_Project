# encoding:utf-8
# @CreateTime: 2022/6/20 17:28
# @Author: Xuguangchun
# @FlieName: rsa_encode.py
# @SoftWare: PyCharm

import base64, os
from common.get_data import *
try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
    from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
except ImportError:
    print("请安装加解密库:pip install PyCryptodome")


"""
# 私钥
private_key = '''-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----
'''
"""

# 公钥

public_key = ReadAndWrite().load_data(r"data\initApiData.yaml")
public_key = public_key["rsaKey"]
public_key1 = "".join(public_key.split())
public_key2 = "-----BEGIN PUBLIC KEY-----\n" + public_key1 + "\n-----END PUBLIC KEY-----"
# print("public_key", public_key2)


def rsa_encrypt(message):
    """校验RSA加密 使用公钥进行加密"""
    cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(public_key2))
    cipher_text = base64.b64encode(cipher.encrypt(message.encode())).decode()
    # print("我是rsa加密：", cipher_text)
    return cipher_text


def rsa_decrypt(text):
    """校验RSA加密 使用私钥进行解密"""
    cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(public_key))
    retval = cipher.decrypt(base64.b64decode(text), 'ERROR').decode('utf-8')
    # print("我是rsa解密：", retval)
    return retval


#
# if __name__ == '__main__':
#     rsa_encrypt(message="Wpn2nMDKWY4M56Psks2dY7ZmJdfvqzSSz9DQK4oXRWFI5IeCbgiV6cPrBNRqtpld")
