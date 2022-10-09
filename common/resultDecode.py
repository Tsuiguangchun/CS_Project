# encoding:utf-8
# @CreateTime: 2022/6/15 15:34
# @Author: Xuguangchun
# @FlieName: resultDecode.py
# @SoftWare: PyCharm


# 偏移量：String AES_KEY_PARAMETER = ""; 秘钥：""
import base64
from common.get_environment import *
import json

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    print('请安装加解密库:pip install PyCryptodome')


# ApiInit("releaseEnvironment").get_env()

class AesSample(object):
    def __init__(self, env):
        self.getEnv = ApiInit(env).get_env()    # 获取环境配置内容
        self.key = self.getEnv[3].encode('utf-8')
        self.iv = self.getEnv[4].encode('utf-8')
        self.mode = AES.MODE_CBC

    def encode(self, data):
        cipher = AES.new(self.key, self.mode, self.iv)
        pad_pkcs7 = pad(data.encode('utf-8'), AES.block_size, style='pkcs7')
        result = base64.encodebytes(cipher.encrypt(pad_pkcs7))
        encrypted_text = str(result, encoding='utf-8').replace('\n', '')
        return encrypted_text

    def decode(self, data):
        cipher = AES.new(self.key, self.mode, self.iv)
        base64_decrypted = base64.decodebytes(data.encode('utf-8'))
        una_pkcs7 = unpad(cipher.decrypt(base64_decrypted), AES.block_size, style='pkcs7')
        decrypted_text = str(una_pkcs7, encoding='utf-8')
        decrypted_text = json.loads(decrypted_text)
        return decrypted_text


# if __name__ == '__main__':
#
#     dec = AesSample(env="releaseEnvironment")
# #     dec.encode(data="我是徐光春")
# #     dec.decode(data="f65nCEl5YbtMBX2LR2UVRA==")