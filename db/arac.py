from db import sql_utils
from db.kullanici import Kullanici

class Arac:

    def __init__(self, plaka, marka, model, ucret):
        tip_id = sql_utils.yeni_arac_tip(marka, model)

        self._id = sql_utils.yeni_arac(plaka, tip_id, ucret)
        self._plaka = plaka.strip().upper()
        self._marka = marka.strip().upper()
        self._model = model.strip().upper()
        self._ucret = ucret
        self._musait_mi = True
        self.baslangic_tarihi = None
        self.bitis_tarihi = None
    
    @property
    def plaka(self):
        return self._plaka;

    @plaka.setter
    def plaka(self, p):
        sql_utils.arac_guncelle_plaka(self._id, p)
        self._plaka = p.strip().upper()
        
    @property
    def marka(self):
        return self._marka; 

    @marka.setter
    def marka(self, m):
        tip_id = sql_utils.yeni_arac_tip(m, self._model)
        sql_utils.arac_guncelle_tip_id(self._id, tip_id)
        self._marka = m.strip().upper()

    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, m):
        tip_id = sql_utils.yeni_arac_tip(self._marka, m)
        sql_utils.arac_guncelle_tip_id(self._id, tip_id)
        self._model = m.strip().upper()
    
    @property
    def ucret(self):
        return self._ucret;

    @ucret.setter
    def ucret(self, u):
        sql_utils.arac_guncelle_ucret(self._id, u)
        self._ucret = u

    @property
    def musait_mi(self):
        return self._musait_mi

    def sil(self):
        sql_utils.arac_sil(self._id)
        self._plaka = None
        self._marka = None
        self._model = None
        self._ucret = None
        self._musait_mi = None
    
    def kira_ucreti_hesapla(self, baslangic_tarihi, bitis_tarihi):
        return sql_utils.kira_ucreti_hesapla(self.ucret, baslangic_tarihi, bitis_tarihi);
        
    def ucret_hesapla(self, baslangic_tarihi, bitis_tarihi):
        return sql_utils.ucret_hesapla(self.ucret, baslangic_tarihi, bitis_tarihi);

    def kirala(self, kullanici, baslangic_tarihi, bitis_tarihi):
        if(not self._musait_mi):
            return None

        self._musait_mi = False
        result = sql_utils.arac_kirala(self._id, self._ucret, kullanici._id, baslangic_tarihi, bitis_tarihi)

        self.baslangic_tarihi = baslangic_tarihi
        self.bitis_tarihi = bitis_tarihi
        return result

    def iade_ucreti_hesapla(self):
        if self._musait_mi:
            return None

        return sql_utils.iade_ucreti_hesapla(self.ucret, self.baslangic_tarihi, self.bitis_tarihi);


    def iade(self, kullanici):
        result = sql_utils.arac_iade(self._id, kullanici._id)
        self.baslangic_tarihi = None
        self.bitis_tarihi = None

        return result


    @staticmethod
    def bul(plaka):
        arac = Arac.__new__(Arac)

        result = sql_utils.arac_bul(plaka)
        if result is None:
            return None
    
        arac._plaka = plaka
        arac._id, arac._marka, arac._model, arac._ucret, arac._musait_mi, arac.baslangic_tarihi, arac.bitis_tarihi = result
        arac._musait_mi = arac._musait_mi != 0
        return arac

    @staticmethod
    def listele(marka = None, model = None, min_ucret = None, max_ucret = None,
                musait_mi = None):
        results = sql_utils.arac_listele(marka, model, min_ucret, max_ucret, musait_mi)

        arac_list = []
        for result in results:
            arac = Arac.__new__(Arac)
            arac._id, arac._plaka, arac._marka, arac._model, arac._ucret, arac._musait_mi, arac.baslangic_tarihi, arac.bitis_tarihi = result
            arac._musait_mi = arac._musait_mi != 0

            arac_list.append(arac)

        return arac_list

    
    def __str__(self):
        return f'{self.plaka} | {self.marka} | {self.model} | {self.ucret} | {self.musait_mi} | {self.baslangic_tarihi} | {self.bitis_tarihi}'
