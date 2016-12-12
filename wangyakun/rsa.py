RSA2_FlAG = 1


class Rsa2:

    try:
        from Crypto.PublicKey import RSA
        global RSA
    except ImportError, e:
        global RSA2_FlAG
        RSA2_FlAG = 0
    if RSA2_FlAG:

        @classmethod
        def import_key(self, key, passphrase=None, file_flag=True):
            '''
            externKey:string or file
            '''
            if file_flag:
                externKey = open(key, 'rb').read()
            else:
                externKey = key
            return RSA.importKey(externKey=externKey, passphrase=passphrase)

        @classmethod
        def encrypt(self, message, pub_key, algo='PKCS1_v1_5'):
            key = pub_key
            if algo == 'PKCS1_v1_5':
                from Crypto.Cipher import PKCS1_v1_5
                from Crypto.PublicKey import RSA
                from Crypto.Hash import SHA
                h = SHA.new(message)
                cipher = PKCS1_v1_5.new(key)
                ciphertext = cipher.encrypt(message + h.digest())

            elif algo == 'PKCS1_OAEP':
                from Crypto.Cipher import PKCS1_OAEP
                if len(message) > 214:
                    return Exception('message is more than 214 with algorithm "PKCS1_OAEP"!!')
                cipher = PKCS1_OAEP.new(key)
                ciphertext = cipher.encrypt(message)
            else:
                raise Exception(
                    'encrypt algorithm "%s" is not  supported' % algo)
            return ciphertext

        @classmethod
        def decrypt(self, ciphertext, pri_key, algo='PKCS1_v1_5'):
            key = pri_key
            if algo == 'PKCS1_v1_5':
                from Crypto.Cipher import PKCS1_v1_5
                from Crypto.PublicKey import RSA
                from Crypto.Hash import SHA
                from Crypto import Random
                dsize = SHA.digest_size
                # Let's assume that average data length is 15
                sentinel = Random.new().read(15 + dsize)
                cipher = PKCS1_v1_5.new(key)
                message = cipher.decrypt(ciphertext, sentinel)

                digest = SHA.new(message[:-dsize]).digest()
                # Note how we DO NOT look for the sentinel
                if digest == message[-dsize:]:
                    return message[:len(message) - dsize]
                else:
                    raise Exception("Encryption was not correct.")
            elif algo == 'PKCS1_OAEP':
                from Crypto.Cipher import PKCS1_OAEP
                cipher = PKCS1_OAEP.new(key)
                message = cipher.decrypt(ciphertext)
                return message

import base64
pub_key = Rsa2.import_key(key='/Users/TIGER/test.pub')
pri_key = Rsa2.import_key(key='/Users/TIGER/test')
ciphertext = Rsa2.encrypt('dba' * 10, pub_key=pub_key)
print base64.b64encode(ciphertext)
print Rsa2.decrypt(ciphertext, pri_key)
