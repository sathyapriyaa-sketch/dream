from mongoengine import connect

from core.transform_config import DB_HOST, DB_NAME
state_storage = connect(host=DB_HOST, db=DB_NAME)
