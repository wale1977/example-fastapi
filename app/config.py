# from pydantic_settings import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=".env")
    # model_config = SettingsConfigDict(env_file="os.path.expanduser('~/.env')", env_file_encoding='utf-8', extra='ignore')
    
    # database_hostname: str
    # database_port: str
    # database_password: str
    # database_name: str
    # database_username: str
    # secret_key:str
    # algorithm: str
    # access_token_expire_minutes:int
    
    # model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8', extra='ignore')
    
    database_hostname: str='localhost'
    database_port: str='5432'
    database_password: str='Password'
    database_name: str='fastapi'
    database_username: str='postgres'
    secret_key:str='Thisisasecr3tkeyformyjasonwebt0ken'
    algorithm: str='HS256'
    access_token_expire_minutes:int=30
    
settings = Settings()

   
# print('settings are as follows:\n',settings)