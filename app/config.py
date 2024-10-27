import os

EUREKA_SERVER = "http://localhost:8761/eureka"
USER_ROLES = {
    'ROLE_ADMIN': ['read', 'write', 'delete'],
    'ROLE_USER': ['read', 'write'],
}


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1@localhost:1978/microAdvertisements'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
