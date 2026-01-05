import sqlite3
from db import db_con
from db import hatalar
import datetime

def yeni_arac_tip(marka, model):
    marka = marka.strip().upper()
    model = model.strip().upper()

    if marka == '' or model == '':
        raise hatalar.BosStringHatasi

    cur = db_con.cursor()
    cur.execute("INSERT OR IGNORE INTO arac_tip(marka, model) VALUES(?, ?)",
                (marka, model));

    cur.execute("SELECT id FROM arac_tip WHERE marka = ? AND model = ?",
                (marka, model));
    
    tip_id = cur.fetchone()[0]

    db_con.commit()
    cur.close()

    return tip_id


def yeni_arac(plaka, tip_id, ucret):
    plaka = plaka.strip().upper()

    if plaka == '':
        raise hatalar.BosStringHatasi

    if ucret <= 0:
        raise hatalar.GecersizUcretHatasi

    arac_id = 0
    
    try:
        cur = db_con.cursor()
        cur.execute("INSERT INTO arac(plaka, tip_id, ucret) VALUES(?, ?, ?)"
                    "ON CONFLICT(plaka) DO UPDATE SET tip_id = ?, ucret = ?"
                    "RETURNING id", (plaka, tip_id, ucret, tip_id, ucret));
        
        arac_id = cur.fetchone()[0]

        db_con.commit()
        cur.close()
    except sqlite3.IntegrityError as err:
        hatalar.reraise_sqlite_err(err)

    return arac_id


def arac_guncelle_plaka(arac_id, deger):
    deger = deger.strip().upper()

    if deger == '':
        raise hatalar.BosStringHatasi
    
    try:
        cur = db_con.cursor()
        cur.execute("UPDATE arac SET plaka = ? WHERE id = ?", (deger, arac_id));
    
        db_con.commit()
        cur.close()
    except sqlite3.IntegrityError as err:
        hatalar.reraise_sqlite_err(err)


def arac_guncelle_tip_id(arac_id, tip_id):
    try:
        cur = db_con.cursor()
        cur.execute("UPDATE arac SET tip_id = ? WHERE id = ?",
                    (tip_id, arac_id));
    
        db_con.commit()
        cur.close()
    except sqlite3.IntegrityError as err:
        hatalar.reraise_sqlite_err(err)



def arac_guncelle_ucret(arac_id, deger):
    if deger <= 0:
        raise hatalar.GecersizUcretHatasi
    
    try:
        cur = db_con.cursor()
        cur.execute("UPDATE arac SET ucret = ? WHERE id = ?", (deger, arac_id));
        
        db_con.commit()
        cur.close()
    except sqlite3.IntegrityError as err:
        hatalar.reraise_sqlite_err(err)


def arac_sil(arac_id):
    cur = db_con.cursor()
    cur.execute("DELETE FROM arac WHERE id = ?", (arac_id,))

    db_con.commit()
    cur.close()


def arac_bul(plaka):
    cur = db_con.cursor()
    cur.execute("SELECT id, marka, model, ucret, musait_mi, "
                    "baslangic_tarihi, bitis_tarihi "
                "FROM arac_view "
                "WHERE plaka = ?", (plaka,))

    result = cur.fetchone()
    if result is None:
        return None
    
    return result


def arac_listele(marka = None, model = None, min_ucret = None,
                 max_ucret = None, musait_mi = None):
    query = "SELECT id, plaka, marka, model, ucret, musait_mi, baslangic_tarihi, bitis_tarihi FROM arac_view "
    conds = []
    bindings = []

    if marka != None and marka.strip() != '':
        conds.append("marka = ?")
        bindings.append(marka.strip().upper())

    if model != None and model.strip() != '':
        conds.append("model = ?")
        bindings.append(model.strip().upper())

    if min_ucret != None:
        conds.append("ucret >= ?")
        bindings.append(min_ucret)

    if max_ucret != None:
        conds.append("ucret <= ?")
        bindings.append(max_ucret)

    if musait_mi != None:
        conds.append("musait_mi = ?")
        bindings.append(musait_mi)
    
    if(len(conds) > 0):
        query = query + " WHERE " + " AND ".join(conds)

    cur = db_con.cursor()
    cur.execute(query, bindings)

    result = cur.fetchall()
    
    cur.close()

    return result


def yeni_kullanici(kullanici_adi):
    kullanici_adi = kullanici_adi.strip().upper()

    if kullanici_adi == '':
        raise hatalar.BosStringHatasi

    try:
        cur = db_con.cursor()
        cur.execute("INSERT OR IGNORE INTO kullanici(kullanici_adi) VALUES(?)",
                    (kullanici_adi,));
        
        cur.execute("SELECT id FROM kullanici WHERE kullanici_adi = ?",
                    (kullanici_adi,));
        
        k_id = cur.fetchone()[0]

        db_con.commit()
        cur.close()
    except sqlite3.IntegrityError as err:
        hatalar.reraise_sqlite_err(err)

    return k_id


def kira_ucreti_hesapla(ucret, baslangic_tarihi, bitis_tarihi):
    baslangic = datetime.datetime.strptime(baslangic_tarihi, '%Y-%m-%d').date()
    bitis = datetime.datetime.strptime(bitis_tarihi, '%Y-%m-%d').date()
    
    if (baslangic - datetime.date.today()).days < 0:
        raise hatalar.GecersizTarihHatasi

    if (bitis - baslangic).days < 0:
        raise hatalar.GecersizTarihHatasi

    return (bitis - baslangic).days * ucret


def ucret_hesapla(ucret, baslangic_tarihi, bitis_tarihi):
    baslangic = datetime.datetime.strptime(baslangic_tarihi, '%Y-%m-%d').date()
    bitis = datetime.datetime.strptime(bitis_tarihi, '%Y-%m-%d').date()

    if (bitis - baslangic).days < 0:
        raise hatalar.GecersizTarihHatasi

    return (bitis - baslangic).days * ucret


def arac_kirala(arac_id, ucret, kullanici_id, baslangic_tarihi, bitis_tarihi):
    baslangic = datetime.datetime.strptime(baslangic_tarihi, '%Y-%m-%d').date()
    bitis = datetime.datetime.strptime(bitis_tarihi, '%Y-%m-%d').date()

    if (baslangic - datetime.date.today()).days < 0:
        raise hatalar.GecersizTarihHatasi

    if (bitis - baslangic).days < 0:
        raise hatalar.GecersizTarihHatasi

    cur = db_con.cursor()
    cur.execute("INSERT INTO kiralamalar" +
                "(arac_id, kullanici_id, baslangic_tarihi, bitis_tarihi, donemki_ucret) "
                "VALUES(?, ?, ?, ?, ?)",
                (arac_id, kullanici_id, baslangic_tarihi, bitis_tarihi, ucret))
    
    db_con.commit()
    cur.close()
    return (bitis - baslangic).days * ucret


def iade_ucreti_hesapla(ucret, baslangic_tarihi, bitis_tarihi):
    baslangic = datetime.datetime.strptime(baslangic_tarihi, '%Y-%m-%d').date()
    bitis = datetime.datetime.strptime(bitis_tarihi, '%Y-%m-%d').date()
    
    if (datetime.date.today() - baslangic).days < 0:
        return (bitis - baslangic).days * ucret

    return (bitis - datetime.date.today()).days * ucret


def arac_iade(arac_id, kullanici_id):
    tarih = datetime.date.today().strftime("%Y-%m-%d")

    cur = db_con.cursor()
    cur.execute("SELECT id, baslangic_tarihi, bitis_tarihi, donemki_ucret, kullanici_id " + 
                "FROM kiralamalar " + 
                "WHERE arac_id = ? AND iade_tarihi IS NULL " + 
                "ORDER BY iade_tarihi DESC " + 
                "LIMIT 1", (arac_id,));

    result = cur.fetchone()
    if result is None:
        return None
    

    kiralama_id = result[0]
    baslangic_tarihi = datetime.datetime.strptime(result[1], '%Y-%m-%d').date()
    bitis_tarihi = datetime.datetime.strptime(result[2], '%Y-%m-%d').date()
    ucret = result[3]
    gercek_kullanici = result[4]
    
    if gercek_kullanici != kullanici_id:
        raise hatalar.YanlisKullanici

    cur.execute("UPDATE kiralamalar SET iade_tarihi = ? WHERE id = ?",
                (tarih, kiralama_id))

    db_con.commit()
    cur.close()
    
    if (datetime.date.today() - baslangic_tarihi).days < 0:
        return (bitis_tarihi - baslangic_tarihi).days * ucret

    return (bitis_tarihi - datetime.date.today()).days * ucret
