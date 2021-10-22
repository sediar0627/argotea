import jwt
from datetime import datetime, timedelta
from utils import leer_json

responses = leer_json('config/status_api.json')

class Auth:

    def __init__(self, config_auth):
        self.secret_key = config_auth["secret_key"]
        self.algorithm = config_auth["algorithm"]
        self.format_date = config_auth["format_date"]
        self.days_expire = config_auth["days_expire"]
        self.hours_expire = config_auth["hours_expire"]
        self.minutes_expire = config_auth["minutes_expire"]
        self.seconds_expire = config_auth["seconds_expire"]

    def encode(self, obj):
        obj["token_create_at"] = str(datetime.now())
        return jwt.encode(obj, self.secret_key, algorithm=self.algorithm)

    def decode(self, token):
        return jwt.decode(token, self.secret_key, algorithms=self.algorithm)
    
    def auth_rol(self, token):
        decode_token = self.decode(token)
        return int(decode_token["rol"])

    def is_auth(self, token):
        
        decode_token = self.decode(token)
        
        date_create = decode_token["token_create_at"]
        date_create = datetime.strptime(date_create, self.format_date)
        
        date_expire = date_create + timedelta(
            days=self.days_expire,
            hours=self.hours_expire,
            minutes=self.minutes_expire,
            seconds=self.seconds_expire)
        
        if(datetime.now() < date_expire):
            return {
                    "status": responses["auth"]["is_auth___ok"]["status"],
                    "message": responses["auth"]["is_auth___ok"]["message"],
                    "usuario": decode_token
                }
        else:
            return {
                    "status": responses["auth"]["is_auth___unauthorized"]["status"],
                    "message": responses["auth"]["is_auth___unauthorized"]["message"]
                }
    
