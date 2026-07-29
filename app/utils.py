from passlib.context import CryptContext
from passlib.exc import UnknownHashError


pwd_context = CryptContext(schemes=['bcrypt_sha256', 'bcrypt'], deprecated='auto')


def hash(password:str):
    return pwd_context.hash(password)



def verify(plain_pass,hash_pass):
    try:
        return pwd_context.verify(plain_pass,hash_pass)
    except UnknownHashError:
        return False
