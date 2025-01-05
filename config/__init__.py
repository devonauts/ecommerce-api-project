import os
from .settings import jwtConfig

class Config:
    #'mysql+mysqlconnector://root:<092560928Mu*>@localhost/ecommerce_api'
    #SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:09256092Mu*@localhost/ecommerce_api"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:092560928Mu*@localhost/ecommerce_api"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    
