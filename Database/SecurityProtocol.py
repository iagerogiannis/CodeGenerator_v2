from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import bcrypt


class SecurityProtocol:
    bcrypt_cost = 10
    padding_character = bytes(chr(7).encode('utf-8'))
    aes_block_size = 16
    aes_mode = AES.MODE_CBC

    @staticmethod
    def en_hash(password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    @staticmethod
    def hkey(key):
        return hashlib.sha256(key.encode("utf-8")).digest()

    @classmethod
    def generate_salt(cls):
        return bcrypt.gensalt(cls.bcrypt_cost)

    @classmethod
    def en_bcrypt(cls, password, salt=None):
        if not salt:
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(cls.bcrypt_cost)).decode('utf-8')
        else:
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @classmethod
    def protected_key_1(cls, password, salt=None):
        return cls.en_bcrypt(cls.en_hash(password), salt)

    @classmethod
    def protected_key_2(cls, password, salt=None):
        return cls.protected_key_1(cls.en_hash(password), salt)

    @classmethod
    def bcrypt_is_correct(cls, password, hashed):
        return hashed == bcrypt.hashpw(password.encode('utf-8'), hashed.encode('utf-8')).decode('utf-8')

    @classmethod
    def key1_is_correct(cls, password_given, hashed_password):
        return hashed_password == bcrypt.hashpw(cls.en_hash(password_given).encode('utf-8'),
                                                hashed_password.encode('utf-8')).decode('utf-8')

    @classmethod
    def key2_is_correct(cls, password_given, hashed_password):
        return hashed_password == bcrypt.hashpw(cls.en_hash(cls.en_hash(password_given)).encode('utf-8'),
                                                hashed_password.encode('utf-8')).decode('utf-8')

    @classmethod
    def aes_encrypt(cls, data, key):
        def pad(s):
            return s + cls.padding_character * (cls.aes_block_size - len(s) % cls.aes_block_size)
        iv = Random.new().read(cls.aes_block_size)
        cipher = AES.new(cls.hkey(key), cls.aes_mode, iv)
        if isinstance(data, str):
            return iv + cipher.encrypt(pad(data.encode("utf-8")))
        elif isinstance(data, bytes):
            return iv + cipher.encrypt(pad(data))

    @classmethod
    def aes_decrypt(cls, data, key, decode=True):
        def unpad(s):
            return s.rstrip(cls.padding_character)
        iv = data[:cls.aes_block_size]
        decipher = AES.new(cls.hkey(key), cls.aes_mode, iv)
        if decode:
            return unpad(decipher.decrypt(data[cls.aes_block_size:])).decode('utf-8')
        else:
            return unpad(decipher.decrypt(data[cls.aes_block_size:]))
