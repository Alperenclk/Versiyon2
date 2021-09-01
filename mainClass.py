import sqlite3
from os import close
from sqlite3.dbapi2 import Cursor
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
from datetime import datetime
import matplotlib.pyplot as plt
from Versiyon2UI import *


class Main(QMainWindow):
    
    def __init__(self):
        
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.giris_index = 0
        self.ekle_index= 1
        self.bilgiler_index= 2
        self.ui.tabWidget.setTabEnabled(self.bilgiler_index, False)
        self.ui.btnBilgiler.setEnabled(False)
        
        self.go_home_page()
        self.ui.btnEkle.setEnabled(0)
        
        # region *******SINYAL/SLOT*****
    
        self.ui.btnGirisYap.clicked.connect(self.GIRIS)
        self.ui.btnKaydet.clicked.connect(self.kullanici_kaydet)
        self.ui.btnEkle.clicked.connect(self.verileri_ekle)
        self.ui.btnKaydet_2.clicked.connect(self.verileri_kaydet)
        self.ui.btnBitir.clicked.connect(self.CIKIS)
        self.ui.btnCikis.clicked.connect(self.CIKIS)
        self.ui.btnBilgiler.clicked.connect(self.BILGILER) 
        self.ui.btnBilgiEkle.clicked.connect(self.Yeni_veri) 
        # endregion
    
    
    def GIRIS(self):
        
        self._lneGirisKullaniciAdi = self.ui.lneGirisKullaniciAdi.text()
        self._lneGirisSifre = self.ui.lneGirisSifre.text()
        
        self.hedefKonular = list()
        conn = sqlite3.connect('versiyon2.db')
        cursor = conn.cursor()
        
        try:

            cursor.execute(f"SELECT kullanici_adi from GIRIS WHERE kullanici_adi ='{self._lneGirisKullaniciAdi}' AND sifre = '{self._lneGirisSifre}'")
            if not cursor.fetchone() == None:
                self.ui.tabWidget.setCurrentIndex(self.ekle_index)
                self.ui.tabWidget.setTabEnabled(self.ekle_index, True)
                
                
                cursor.execute(f"SELECT HEDEf from HEDEFLER WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' ")
                data = cursor.fetchall()        
                for index in data:
                    for i in index:
                        self.hedefKonular.append(i)
                        self.ui.cmbKonular.addItem(i)

            else:
                m_box5 = QMessageBox.information(self,"Information","Hatali bilgi!.\nlutfen bilgilerinizi kontrol edin.")
                    
        except Exception as hata:
            self.ui.statusbar.showMessage('HATA: Daha once hic kullanici olusturulmamis')            

        conn.commit()         
        conn.close()
        
        
    def verileri_kaydet(self):
        
        self.ui.btnBilgiler.setEnabled(True)
        self._cmbKonular = self.ui.cmbKonular.currentText()
        self._time = time.strftime("%x %X")
        self._lneGirisKullaniciAdi = self.ui.lneGirisKullaniciAdi.text()
         
            
        self._spnGunlukKacDk=self.ui.spnGunlukDK_7.value()
        self._spnNeKadarVerimli=self.ui.spnGunlukDK_2.value()
        self._spnYarinHedef=self.ui.spnYarinHedef.value()
        temp = '0'
        
        conn = sqlite3.connect('versiyon2.db')
        cursor = conn.cursor()
        
        sorguCreTbl = (f"CREATE TABLE IF NOT EXISTS '{self._cmbKonular.upper()}' (id INTEGER PRIMARY KEY AUTOINCREMENT,kullanici_adi TEXT,GUNLUK_CALISMA  text,VERIM  text,YARIN_HEDEF  text,Gunun_Puani text,kayitT text)")
        cursor.execute(sorguCreTbl)
        conn.commit()

            
        if self.ui.chkIlgilenmedim.isChecked():
             
            self.ui.spnGunlukDK_7.setValue(0)
            self.ui.spnGunlukDK_2.setValue(0)
            self.ui.spnYarinHedef.setValue(0)
                     
            self._spnGunlukKacDk = self.ui.spnGunlukDK_7.value()
            self._spnNeKadarVerimli = self.ui.spnGunlukDK_2.value()
            self._spnYarinHedef=self.ui.spnYarinHedef.value()                       
  
            cursor.execute(f"INSERT INTO '{self._cmbKonular.upper()}' (kullanici_adi,GUNLUK_CALISMA,VERIM,YARIN_HEDEF,Gunun_Puani,kayitT)VALUES(?,?,?,?,?,?)",
                                                  (self._lneGirisKullaniciAdi,self._spnGunlukKacDk,self._spnNeKadarVerimli,self._spnYarinHedef,temp,self._time))

            conn.commit()
            
            
        else:

            cursor.execute(f"INSERT INTO '{self._cmbKonular.upper()}' (kullanici_adi,GUNLUK_CALISMA,VERIM,YARIN_HEDEF,Gunun_Puani,kayitT) VALUES (?,?,?,?,?,?)",
                                  (self._lneGirisKullaniciAdi,self._spnGunlukKacDk,self._spnNeKadarVerimli,self._spnYarinHedef,temp,self._time))

            conn.commit()
            
        self.ui.chkIlgilenmedim.setChecked(False)
        
        self.ui.statusbar.showMessage("Sonuclar Hesaplaniyor...  ",1500)
        

        
        self.ui.lbBaslikKonu.setText(self._cmbKonular.upper())
        
        #toplam GUN
    
        cursor.execute(f"SELECT HEDEF_GUN from HEDEFLER WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' AND HEDEf = '{self._cmbKonular}' ")
        ilkHedef = cursor.fetchone() 
        self.ui.lbToplamHedef.setText(f"TOPLAM HEDEFIMIZ {ilkHedef[0]} GUN.")
        
        #KALAN GUN   
        cursor.execute(f"SELECT kayitT from HEDEFLER WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' AND HEDEf = '{self._cmbKonular}'")
        ilkTarih = cursor.fetchone() 
        ilkTarih = ilkTarih[0][:8]
        
        cursor.execute(f"SELECT kayitT from '{self._cmbKonular.upper()}' WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}'")
        sonTarih = cursor.fetchmany(-1) 
        sonTarih = sonTarih[-1][0][:8]
        
        d1 = datetime.strptime(ilkTarih,"%m/%d/%y")
        d2 = datetime.strptime(sonTarih,"%m/%d/%y")
        
        farkGun = abs((d2 - d1).days)
        kalanGun = abs(int(ilkHedef[0])-farkGun)

        self.ui.lbKalanGun.setText(f"Hedefe ulasmaya {kalanGun} GUN kaldi")
        
        # kalan Dk
        
        cursor.execute(f"SELECT HEDEF_GUN from HEDEFLER WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' AND HEDEf = '{self._cmbKonular}' ")
        hedefGun = cursor.fetchone() 
        

        cursor.execute(f"SELECT HEDEF_GUN_DK from HEDEFLER WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' AND HEDEf = '{self._cmbKonular}' ")
        hedefDk = cursor.fetchone() 
        
        cursor.execute(f"SELECT GUNLUK_CALISMA from '{self._cmbKonular.upper()}' WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}'")
        calismaDK = cursor.fetchall() 
        toplamCalisma = 0
        for index in calismaDK:
            for i in index:
                toplamCalisma = toplamCalisma + int(i)   
                
        
        kalanDK = (int(hedefGun[0])*int(hedefDk[0])) - toplamCalisma
        
        # tablo silinmeden once alinmasi gerekiyor kodun lazim oldugu yer 208. satir
        cursor.execute(f"SELECT  ONEM_PUAN from HEDEFLER WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' AND HEDEf = '{self._cmbKonular}'")
        self.degerler = cursor.fetchone() 

        
        if kalanDK > 0:
            
            self.ui.lbKalanDK.setText(f"Hedefe ulasmak icin {kalanDK} DK daha calismaliyiz")

        else:
            m_box = QMessageBox.information(self, 'TEBRIKLER','TEBRIKLER HEDEFI BASARI ILE TAMAMLADINIZ...')
            self.ui.lbKalanDK.setText("HEDEFE ULASILDI :)")
            self.ui.progKalan.setValue(100)

            cursor.execute(f"SELECT HEDEf,HEDEF_GUN,kayitT from HEDEFLER WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' AND HEDEf = '{self._cmbKonular}'")
            kopyalacanak = cursor.fetchall() 

            for index in kopyalacanak:
                
                cursor.execute("INSERT INTO TAMAMLANANLAR(kullanici_adi,HEDEF,Hedef_gun,toplam_calisma,ilkKayitT,kayitT) VALUES (?,?,?,?,?,?)",
                              (self._lneGirisKullaniciAdi,index[0],index[1],toplamCalisma,index[2],self._time))
                
            cursor.execute(f"DELETE FROM HEDEFLER WHERE HEDEf = '{self._cmbKonular}'")
            conn.commit()
            
        
        # GUNLUK PUAN      =    (gunluk hedef / 60 + onem) - (gunlukDK / 60 + verim  )   
          
        ilkEtap = (int(hedefDk[0]) / 60) + (int(self.degerler[0]))          
        ikinciEtap =(int(self._spnGunlukKacDk) / 60) + int(self._spnNeKadarVerimli)

        sonuc = (ilkEtap - ikinciEtap) *-10

        cursor.execute(f"SELECT YARIN_HEDEF from '{self._cmbKonular.upper()}' WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}'")
        yarinHedef = cursor.fetchall()      
        
        if len(yarinHedef) == 1:
            yarinHedef = int(yarinHedef[-1][0])
            
        else:    
            yarinHedef = int(yarinHedef[-2][0])


          
        if (int(self._spnGunlukKacDk) >=  yarinHedef) and  (yarinHedef!= 0) :                # eger dun yapilan hedef tutmus ise +10 puan
            sonuc = sonuc + 10
 
        sonuc = int(sonuc)   
        self.ui.lbGununPuani.setText(f"GUNUN PUANI: {str(sonuc)}")

        sonuc = str(sonuc)
                   
        cursor.execute(f"UPDATE '{self._cmbKonular.upper()}' SET Gunun_Puani = {sonuc} WHERE kayitT = '{self._time}'")
        conn.commit()
        
        
        # progress bar   hdf_gun* hdfDK = toplamDk        kalanDK/toplamDK*100
        
        yuzdelik =  ((kalanDK * 100) / (int(hedefGun[0])*int(hedefDk[0])))
        yuzdelik = int(100 - yuzdelik)
        self.ui.progKalan.setValue(yuzdelik)
        
        
        # plot 
        
        cursor.execute(f"SELECT Gunun_Puani from '{self._cmbKonular.upper()}' WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' ")
        puanlar = cursor.fetchall()
        toplamPuan = list()
        for index in puanlar:
            for i in index:                
                toplamPuan.append(int(i))
                
        cursor.execute(f"SELECT kayitT from '{self._cmbKonular.upper()}' WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' ")
        puanlar = cursor.fetchall()
        kayitList = list()
        for index in puanlar:
            for i in index:                
                kayitList.append(i[:8])
        
        
        fig = plt.figure(figsize=(3.4,2.3))
        plt.plot(kayitList, toplamPuan, color='r', linewidth=2.0)                
        plt.suptitle('GELISIM')
        #plt.xlabel('TARIH')
        #plt.ylabel('GUNLUK PUANLAR')
        
        plt.savefig("GELISIM.jpg")
        plt.close(fig)
       
        pix = QPixmap("GELISIM.jpg")
        self.ui.lbGrafik.setPixmap(pix)
        
        
        self.ui.btnBilgiler.setEnabled(True)

        conn.close()
    
    # region   *********kullanici_kaydet *********  
      
    def kullanici_kaydet(self):

        self._time = time.strftime("%x %X")
        self._lneKayAdSoyad = self.ui.lneKayitAdSoyad.text()
        self._lneKayitKullanici = self.ui.lneKayitKullaniciAdi.text()
        self._lneKayitSifre = self.ui.lneKayitSifre.text()
        self._lneKonu = self.ui.lneKonu.text()
        if (self._lneKayAdSoyad == '') or (self._lneKayitKullanici == '') or (self._lneKayitSifre == '') or(self._lneKonu == ''):
            m_box6 = QMessageBox.information(self,"WARNING","Bilgiler bos birakilamaz.")
            
        else:    
            self._spnGunlukHedef=self.ui.spnGunlukHedef.value()
            self._spnGunlukDK=self.ui.spnGunlukDK.value()
            self._spnOnemPuan=self.ui.spnOnemPuan.value()

            self.ui.btnEkle.setEnabled(1)    
            
            self.veriTabani()
            
            m_box2 = QMessageBox.information(self,"Information","Kayit islemi basarili.\nIsrerseniz daha fazla konu ekleyebilirsiniz yada Giris yapabilirsiniz")
            
            self.ui.btnKaydet.setEnabled(0)

    # region   *********VERİ TABANI*********
    
    def veriTabani(self):
        
        global cursor
        global conn
        
        conn = sqlite3.connect('versiyon2.db')
        cursor = conn.cursor()
        
        sorguCreTblAna = ("CREATE TABLE IF NOT EXISTS GIRIS (id INTEGER PRIMARY KEY AUTOINCREMENT,Ad_soyad TEXT, kullanici_adi text, sifre text, kayitT text)")
        sorguCreTblhdf = ("CREATE TABLE IF NOT EXISTS HEDEFLER (id INTEGER PRIMARY KEY AUTOINCREMENT,kullanici_adi TEXT, HEDEf text, HEDEF_GUN  text, HEDEF_GUN_DK  text,ONEM_PUAN  text,kayitT text)")
        sorguCreTblBasari = (f"CREATE TABLE IF NOT EXISTS TAMAMLANANLAR (id INTEGER PRIMARY KEY AUTOINCREMENT,kullanici_adi TEXT,HEDEF text,Hedef_gun text,toplam_calisma  text, BOS  text,ilkKayitT text,kayitT text)")
        cursor.execute(sorguCreTblBasari)
        cursor.execute(sorguCreTblAna)
        cursor.execute(sorguCreTblhdf)
        
        conn.commit()
        
        # Kontrol ve kayit
        try:  
          
            cursor.execute(f"SELECT kullanici_adi from GIRIS WHERE kullanici_adi ='{self._lneKayitKullanici}'")
            
            if not cursor.fetchone() == None:
                m_box = QMessageBox.information(self,"Information","Bu kullanici adi zaten kayitli")

            else:
                cursor.execute("INSERT INTO GIRIS(Ad_soyad,kullanici_adi,sifre,kayitT) VALUES (?,?,?,?)",
                              (self._lneKayAdSoyad,self._lneKayitKullanici,self._lneKayitSifre,self._time ))
                
                cursor.execute("INSERT INTO HEDEFLER(kullanici_adi,HEDEf,HEDEF_GUN,HEDEF_GUN_DK,ONEM_PUAN,kayitT) VALUES (?,?,?,?,?,?)",
                              (self._lneKayitKullanici,self._lneKonu,str(self._spnGunlukHedef),str(self._spnGunlukDK),str(self._spnOnemPuan),self._time))

   
        except Exception as hata:
            self.ui.statusbar.showMessage("Şöyle bir hata meydana geldi"+str(hata))
   
        #eski haline cevir       
        self.ui.lneKonu.setText('')
        self.ui.spnGunlukHedef.setValue(1)
        self.ui.spnGunlukDK.setValue(30)
        self.ui.spnOnemPuan.setValue(1)
        
        conn.commit()         
        conn.close() 

    # region   *********verileri_ekle*********
    def verileri_ekle(self):
        
        self._lneKonu = self.ui.lneKonu.text()
        self._spnGunlukHedef=self.ui.spnGunlukHedef.value()
        self._spnGunlukDK=self.ui.spnGunlukDK.value()
        self._spnOnemPuan=self.ui.spnOnemPuan.value()
        
        conn = sqlite3.connect('versiyon2.db')
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO HEDEFLER(kullanici_adi,HEDEf,HEDEF_GUN,HEDEF_GUN_DK,ONEM_PUAN,kayitT) VALUES (?,?,?,?,?,?)",
                              (self._lneKayitKullanici,self._lneKonu,str(self._spnGunlukHedef),str(self._spnGunlukDK),str(self._spnOnemPuan),self._time ))
         
        self.ui.statusbar.showMessage("Ekleme Basarili  ",1000)
        self.ui.lneKonu.setText('')
        self.ui.spnGunlukHedef.setValue(1)
        self.ui.spnGunlukDK.setValue(30)
        self.ui.spnOnemPuan.setValue(1)
        
        conn.commit()         
        conn.close()
        

#----------------------ÇIKIŞ-----------------------------#

    def CIKIS(self):
  
        self.cevap=QMessageBox.question(penAna,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",\
                                 QMessageBox.Yes | QMessageBox.No)
        if self.cevap == QMessageBox.Yes:
            self.close()
        else:
            penAna.show()
            
            
#----------------------BILGILER-----------------------------#
    def BILGILER(self):
        

        self.ui.tabWidget.setCurrentIndex(self.bilgiler_index)
        self.ui.tabWidget.setTabEnabled(self.bilgiler_index, True)
 
    
        conn = sqlite3.connect('versiyon2.db')
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT Ad_soyad from GIRIS WHERE kullanici_adi ='{self._lneGirisKullaniciAdi}' AND sifre = '{self._lneGirisSifre}'")
        ad_soyad = cursor.fetchone()
        
        toplamGunlukPuan = 0
        self.ui.lbBilgiIsim.setText(ad_soyad[0])
        self.ui.lbBilgiSifre.setText(self._lneGirisSifre)
        self.ui.lbBilgiKullanici.setText(self._lneGirisKullaniciAdi)
        try:

            for i in self.hedefKonular:
                
                cursor.execute(f"SELECT Gunun_Puani from '{i.upper()}' WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' ")
                puanlar = cursor.fetchall()   
            
                for index in puanlar:
                    for j in index:  
                        toplamGunlukPuan = toplamGunlukPuan + int(j)
                
        except Exception as hata:

                self.ui.statusbar.showMessage(f'{hata}:')      


        self.ui.lbBilgiToplamPuan.setText(str(toplamGunlukPuan))
        
        
        self.ui.tbwHedefler.clear()
        self.ui.tbwHedefler.setHorizontalHeaderLabels(('HEDEF','KAC GUN','GUNLUK HEDEF','ONEMI','kayitT'))
        self.ui.tbwHedefler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        cursor.execute(f"SELECT HEDEf,HEDEF_GUN,HEDEF_GUN_DK,ONEM_PUAN,kayitT FROM HEDEFLER WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' ")
        for satirIndeks, satirVeri in enumerate(cursor):
            for sutunIndeks, sutunVeri in enumerate (satirVeri):
                self.ui.tbwHedefler.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
                
        self.ui.tbwTamamlananlar.clear()
        self.ui.tbwTamamlananlar.setHorizontalHeaderLabels(('HEDEF','KAC GUN','toplam DAKIKA','Bitirme Tarihi','kayitT'))
        self.ui.tbwTamamlananlar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        cursor.execute(f"SELECT HEDEF,Hedef_gun,toplam_calisma,ilkKayitT,kayitT FROM TAMAMLANANLAR WHERE kullanici_adi = '{self._lneGirisKullaniciAdi}' ")
        for satirIndeks, satirVeri in enumerate(cursor):
            for sutunIndeks, sutunVeri in enumerate (satirVeri):
                self.ui.tbwTamamlananlar.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
        
        conn.commit()         
        conn.close()
        
        
#----------------------Yeni VERI-----------------------------#       
    def Yeni_veri(self):
        
        conn = sqlite3.connect('versiyon2.db')
        cursor = conn.cursor()
        
        self._time = time.strftime("%x %X")
        self._lneBilgiKonu = self.ui.lneBilgiKonu.text()
        self._spnBilgiGunlukHedef=self.ui.spnBilgiGunlukHedef.value()
        self._spnBilgiGunlukDK=self.ui.spnBilgiGunlukDK.value()
        self._spnBilgiOnemPuan=self.ui.spnBilgiOnemPuan.value()

        
        cursor.execute(f"INSERT INTO HEDEFLER(kullanici_adi,HEDEf,HEDEF_GUN,HEDEF_GUN_DK,ONEM_PUAN,kayitT) VALUES (?,?,?,?,?,?)",
                              (self._lneGirisKullaniciAdi,self._lneBilgiKonu,str(self._spnBilgiGunlukHedef),str(self._spnBilgiGunlukDK),str(self._spnBilgiOnemPuan),self._time))
        
        self.ui.statusbar.showMessage("Basari ile Kaydedildi...  ",1000)
        conn.commit()         
        conn.close()
    
    def go_home_page(self):
        
        self.ui.tabWidget.setCurrentIndex(self.giris_index) 
        

uygulama = QApplication(sys.argv)
penAna = Main()
penAna.show()
sys.exit(uygulama.exec_())  
