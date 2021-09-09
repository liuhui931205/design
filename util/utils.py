import base64
import json
from Crypto.Cipher import AES
from uuid import uuid4
class WXBizDataCrypt():
	def __init__(self, appId, sessionKey):
		self.appId = appId
		self.sessionKey = sessionKey

	def decrypt(self, encryptedData, iv):
		# base64 decode
		sessionKey = base64.b64decode(self.sessionKey)
		encryptedData = base64.b64decode(encryptedData)
		iv = base64.b64decode(iv)

		cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

		decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)).decode())

		if decrypted['watermark']['appid'] != self.appId:
			raise Exception('Invalid Buffer')

		return decrypted

	def _unpad(self, s):
		return s[:-ord(s[len(s)-1:])]


def get_short_uuid():
	uuidChars = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
				 "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B",
				 "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
				 "V", "W", "X", "Y", "Z")

	uuid = str(uuid4()).replace('-', '')
	result = ''
	for i in range(0, 8):
		sub = uuid[i * 4:i * 4 + 4]
		x = int(sub, 16)
		result += uuidChars[x % 0x3E]
	return result