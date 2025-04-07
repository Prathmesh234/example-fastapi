from passlib.context import CryptContext
pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

##hashing our password using the becrypt algorithm 
##this is the default hashing algorithm used by passlib

def hash_password(password:str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
