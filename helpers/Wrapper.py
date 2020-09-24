from .Singleton import Singleton
from .Logger import Logger
import json
import os
from os import path, mkdir
class Wrapper(metaclass=Singleton):
    def __init__(self):
        self.contentFolder              = 'Content'
        self.postsJson                  = 'posts.json'
        self.BlacklistJson              = 'Blacklists.json'
        self.EditedJson                 = 'Editor.json'

        self.postsPath        = path.join(self.contentFolder, self.postsJson)
        self.BlacklistPath    = path.join(self.contentFolder, self.BlacklistJson)
        self.EditedPath       = path.join(self.contentFolder, self.EditedJson)
        
        # Create nescessary folders and files
        if (not path.exists(self.contentFolder)):
            mkdir(self.contentFolder)
            Logger.log(self,f'Created folder {self.contentFolder}')

        ## posts json
        if (not path.exists(self.postsPath)):
            with open(self.postsPath, 'w+') as f:
                f.write(json.dumps({
                    "total": 0,
                    "posts": []
                }))
                Logger.log(self, f'Created JSON {self.postsPath}')

        ## Json for blacklisted posts
        if (not path.exists(self.BlacklistPath)):
            with open(self.BlacklistPath, 'w+') as f:
                f.write('[]')
                Logger.log(self, f'Created JSON {self.BlacklistPath}')

        ## Edit json cache
        if (not path.exists(self.EditedPath)):
            with open(self.EditedPath, 'w+') as f:
                f.write(json.dumps({
                    "increment":    0,
                    "blacklisted":  0
                }))
                Logger.log(self, f'Created JSON {self.EditedPath}')
    
    def append_post(self, obj):
        _json = self.read_json(self.postsPath)
        _json['total'] += 1
        _json['posts'].append({
            'id': obj.id,
            'title': obj.title,
            'body': obj.body
        })
        self.write_json(self.postsPath, _json)

    def read_json(self, file):
        with open(file, 'r', encoding='utf8') as f:
            Logger.log(self, f'Read JSON {file}')
            return json.load(f);

    def write_json(self, file, data):
        with open (file, 'w+', encoding='utf8') as f:
            Logger.log(self, f'Wrote JSON Object {file}', 2)
            f.write(json.dumps(data, indent=4, ensure_ascii=False))




