import functools
import base64
import socket
from tkinter.tix import Tree
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES

RSA_PEM_LEN = 4096
RSA_PEM_WIDTH = len(hex(RSA_PEM_LEN)[2:])

AES_KEY_LEN = 1024
AES_KEY_WIDTH = len(hex(AES_KEY_LEN)[2:])

PACKAGE_MAX_LEN = 4096


def _serverProcedure(pipe):
    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)

    rsa_cipher = PKCS1_v1_5.new(RSA.import_key(rsa.exportKey()))
    rsa_public_pem = rsa.publickey().exportKey()
    rsa_public_pem = base64.b64encode(rsa_public_pem)
    pipe.send(hex(len(rsa_public_pem))[2:].rjust(RSA_PEM_WIDTH, '0').encode())
    pipe.send(rsa_public_pem)

    aes_key_len = int(pipe.recv(AES_KEY_WIDTH), 16)
    encrypted_aesKey = pipe.recv(aes_key_len)
    encrypted_aesKey = base64.b64decode((encrypted_aesKey))
    aes_key = rsa_cipher.decrypt(
        encrypted_aesKey, random_generator)

    aes_cipher = AES.new(aes_key, AES.MODE_ECB)
    return aes_cipher


def _clientProcedure(pipe):
    rsa_pem_len = int(pipe.recv(RSA_PEM_WIDTH), 16)
    rsa_public_pem = pipe.recv(rsa_pem_len)
    rsa_public_pem = base64.b64decode((rsa_public_pem))
    rsa_cipher = PKCS1_v1_5.new(RSA.import_key(rsa_public_pem))

    aes_key = Random.get_random_bytes(16)

    encrypted_aesKey = rsa_cipher.encrypt(aes_key)
    encrypted_aesKey = base64.b64encode(encrypted_aesKey)
    pipe.send(hex(len(encrypted_aesKey))[
              2:].rjust(AES_KEY_WIDTH, '0').encode())
    pipe.send(encrypted_aesKey)

    aes_cipher = AES.new(aes_key, AES.MODE_ECB)
    return aes_cipher


def _aesPipeOUT(content, writer, aes_cipher, max_len=4096):
    ''' Communicate through a AES pipe. max_len=4096 as defaut.
        Return:
            length for 'Success'
            -1 for 'out of lenght'
    '''
    data = content.encode()
    msg_length = len(content)
    data = _align_bytes(data)
    encrypted_data = aes_cipher.encrypt(data)
    #encrypted_data = base64.b64encode(encrypted_data)
    if (align_length := len(encrypted_data)) > max_len:
        return -1
    width = len(hex(max_len)[2:])
    format_data = hex(align_length)[2:].rjust(width, '0').encode()
    format_data += hex(msg_length)[2:].rjust(width, '0').encode()
    format_data += encrypted_data
    writer(format_data)
    return msg_length


def _aesPipeIN(reader, aes_cipher, max_len=4096):
    ''' Communicate through a AES pipe. max_len=4096 as defaut.
        Return:
            content 'decrypt'
    '''
    width = len(hex(max_len)[2:])
    align_length = reader(width)
    if align_length == b'':
        # connection closed
        raise ConnectionError
    align_length = int(align_length, 16)
    msg_length = reader(width)
    msg_length = int(msg_length, 16)
    encrypted_data = reader(align_length)
    #encrypted_data = base64.b64decode(encrypted_data)
    data = aes_cipher.decrypt(encrypted_data)
    content = data.decode()[:msg_length]
    return content


def block_at_first(keyAgreement):
    @functools.wraps(keyAgreement)
    def wrapper(pipe: socket.socket):
        pipe.setblocking(True)
        ret = keyAgreement(pipe)
        pipe.setblocking(False)
        return ret
    return wrapper

# SECTION for insecure channel


@block_at_first
def keyAgreementServer(pipe):
    aes_cipher = _serverProcedure(pipe)

    aesPipeIN = functools.partial(
        _aesPipeIN, reader=pipe.recv, aes_cipher=aes_cipher, max_len=PACKAGE_MAX_LEN)
    aesPipeOUT = functools.partial(
        _aesPipeOUT, writer=pipe.send, aes_cipher=aes_cipher, max_len=PACKAGE_MAX_LEN)

    return aesPipeIN, aesPipeOUT


@block_at_first
def keyAgreementClient(pipe):
    aes_cipher = _clientProcedure(pipe)

    aesPipeIN = functools.partial(
        _aesPipeIN, reader=pipe.recv, aes_cipher=aes_cipher, max_len=PACKAGE_MAX_LEN)
    aesPipeOUT = functools.partial(
        _aesPipeOUT, writer=pipe.send, aes_cipher=aes_cipher, max_len=PACKAGE_MAX_LEN)

    return aesPipeIN, aesPipeOUT
# !SECTION


# SECTION if we agree with a key through a secure channel
# So, setting up a new secure channel will be eazy
def sendNewAesKey(aesPipeOUT):
    aes_key = Random.get_random_bytes(16)
    aes_key_b64 = base64.b64encode(aes_key)
    aesPipeOUT(aes_key_b64.decode())
    return aes_key


def recvNewAesKey(aesPipeIN):
    aes_key_b64 = aesPipeIN().encode()
    aes_key = base64.b64decode(aes_key_b64)
    return aes_key


def newSecureChannel(aes_key, pipe):
    aes_cipher = AES.new(aes_key, AES.MODE_ECB)

    aesPipeIN = functools.partial(
        _aesPipeIN, reader=pipe.recv, aes_cipher=aes_cipher, max_len=PACKAGE_MAX_LEN)
    aesPipeOUT = functools.partial(
        _aesPipeOUT, writer=pipe.send, aes_cipher=aes_cipher, max_len=PACKAGE_MAX_LEN)

    return aesPipeIN, aesPipeOUT
# !SECTION


def _align_bytes(data):
    align = (16 - len(data) % 16) + len(data)
    return data.ljust(align, b'\0')
