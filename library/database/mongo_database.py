from pathlib import Path
import pymongo
from app.core.library import BaseFunctionLibrary, FileOperationLibrary
from os import environ

class MongoDataBase:
    """
        Mongo class consists of CRUD operations of MongoDB \n
    """
    def __init__(self):
         
        
        self.base,self.file = (BaseFunctionLibrary(), FileOperationLibrary())
        self.db_config = self.file.load_json_files(self.base.load_absolute_path("../../config/database_config.json"))
        conf = self.db_config
        self.client= pymongo.MongoClient(self.settings.MONGODB_CONN_URL)
        self.auth = self.client[conf['auth_db']]
        self.signup, self.login = (self.auth[conf['signup_col']],self.auth[conf['login_col']])
               
        
    def insert_data(self,col,data):
        
        try:
            res = col.insert_one(data)
            return 200
        except Exception as e:
            return 500
        
    
    def find_data(self,col,data):
        
        try:
            res = col.find(dict(data))
            res_list = []
            for ele in res: res_list.append(ele)
            if len(res_list) > 0:
                return res_list
            else: return 400 
            
        except Exception as e:
            return 500
        
    def delete_data(self,col,data):
        
        try:
            if self.find_data(col=col,data=data) != 400:
                res = col.delete_many(dict(data))
                if res.deleted_count >= 1:
                    return 200
                else:
                    return 400
            else:
                return 404
            
        except Exception as e:
            return 500
        
    def update_data(self,col,data,new_data):
        
        try:
            res = col.update_many(dict(data),{"$set":dict(new_data)})
            if res.modified_count >= 1:
                return 200
            else: 
                return 400
        except Exception as e:
            return 500