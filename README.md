# 🚗 Araç Kiralama Otomasyonu (CARENTO)

CARENTO, **BLM2001 – Bilgisayar Programlama II** dersi kapsamında geliştirilmiş, Python ve PyQt5 kullanılarak oluşturulmuş bir **masaüstü araç kiralama otomasyonudur**.

Uygulama; araç envanterinin yönetilmesi, kullanıcı işlemleri ile kiralama ve iade süreçlerinin dijital ortamda yürütülmesini amaçlamaktadır.


---

## 👨‍💻 Geliştiriciler
- Ömer Kerem Çataklı  
- Burak Kaan Karaçay  

---

## ✨ Özellikler
- Admin ve User olmak üzere iki farklı kullanıcı paneli
- Araç ekleme, silme ve düzenleme (Admin)
- Araç kiralama ve iade işlemleri (User)
- Erken iade durumunda otomatik ücret hesaplama
- Filtrelenebilir araç listesi
- SQLite tabanlı veritabanı altyapısı

---

## 🏗️ Mimari
Proje, **MVC (Model-View-Controller)** yapısına benzer **katmanlı bir mimari** ile geliştirilmiştir.

- **Presentation Layer:** PyQt5 arayüzleri  
- **Business Logic Layer:** İş kuralları ve hesaplamalar  
- **Data Layer:** SQLite veritabanı işlemleri  

---

## 🛠️ Kullanılan Teknolojiler
- **Python** 3.13+
- **PyQt5** (Qt Designer)
- **SQLite3**
- **OOP (Nesne Yönelimli Programlama)**

---

## ▶️ Çalıştırma

```bash
run.bat
