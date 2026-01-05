from db import sql_utils

class Kullanici:
    def __init__(self, kullanici_adi):
        self._id = sql_utils.yeni_kullanici(kullanici_adi)
        self.ad = kullanici_adi



