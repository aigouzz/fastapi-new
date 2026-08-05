import dbm
FILE_DB = "file_db"
SHARE_DB = "share_db"

class FileDB:
    def __init__(self):
        # self.db_path = db_path
        pass

    def create_file(self, file_local: str, file_name: str ):
        db = dbm.open(FILE_DB, 'c')
        db[file_local] = file_name
        db.close()

    def get_file(self, file_local):
        db = dbm.open(FILE_DB, 'r')
        files = db.keys()
        file_name = bytes(file_local.encode('utf-8'))
        if file_name in files:
            return db[file_name].decode('utf-8')
        else:
            return None

    def get_all_files(self):
        files = dbm.open(FILE_DB, 'r')
        codes = dbm.open(SHARE_DB, 'r')
        allfiles = []
        for key in files.keys():
            file = {
                "file_name": files[key].decode('utf-8'),
                "file_local": str(key.decode('utf-8')),
                "code": str(codes.get(key, b"").decode('utf-8'))
            }
            allfiles.append(file)
        return allfiles

    def create_share_code(self, file_local, code):
        db = dbm.open(SHARE_DB, 'c')
        db[file_local] = code
        db.close()

    def get_share_code(self, file_local):
        db = dbm.open(SHARE_DB, 'r')
        codes = db.keys()
        file_name = bytes(file_local.encode('utf-8'))
        if file_name in codes:
            return db[file_name].decode('utf-8')
        else:
            return None

file_db = FileDB()