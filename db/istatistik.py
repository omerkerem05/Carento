from db import db_con

def toplam_gelir():
    cur = db_con.cursor()

    cur.execute("""SELECT
	SUM(
		IIF(
			JULIANDAY(iade_tarihi) - JULIANDAY(baslangic_tarihi) < 0, 
				0, 
				(JULIANDAY(iade_tarihi) - JULIANDAY(baslangic_tarihi)) * donemki_ucret))
	FROM kiralamalar
	WHERE iade_tarihi IS NOT NULL""")
    
    result = cur.fetchone()
    if result is None:
        return None

    return result[0]
