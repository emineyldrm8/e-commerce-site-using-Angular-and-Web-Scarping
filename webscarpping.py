import requests
from bs4 import BeautifulSoup
import pandas as pd
from csv import writer
import pymongo
from pymongo import MongoClient

#Kullanılacak kodlar için gerekli import işlemleri yapıldı.
#databasein ismini ve tablonun ismini ayarladık
client = MongoClient('mongodb://localhost:27017')#MongoDB bağlantısı için gerekli
db = client.EmineŞevval #Veritabanının adı
collection = db.Urunler
#user_agent bilgisini my user agent olarak chromeda aratıp alındı
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.65"
}

#TRENYOL İLE WEB SİTESİ BAĞLAMA KODU
Urun_Listesi=[]
#bos liste olusturulup alınan bilgiler içine kaydedildi.
url = "https://www.trendyol.com/sr?q=laptop&qt=laptop&st=laptop&os=1"#Trendyol'un linki tutuluyor.
response = requests.get(url)#Trendyol linki alınıyor.
content = response.content
soup1 = BeautifulSoup(content, "html.parser")
#trendyol için 300 sayfalık arama yapıldı
for a in range(1,300):
 #urun adını almak için en tepedeki classa baktık  
    urun= soup1.find_all("div", {"class": "prdct-cntnr-wrppr"})
    for urun in urun:#Bütün ürünler için dolasma
        urun_link = urun.find_all("div", attrs={"class": "with-campaign-view"})
        for i in urun_link:#Ürün linki bulunacak
        #urun linkinin içinde dolasarak kalan bilgiler cekildi.
            link = i.find("div", {"class": "p-card-chldrn-cntnr card-border"})
            #a nın degeri artıkca sayfalar ilerletildi.
            link = "https://www.trendyol.com" + link.a.get("href")#Trenyolun ve ürün bilgilerinin linkleri birleştiriliyor.
            detaylar = requests.get(link, headers=header)
            soup2 = BeautifulSoup(detaylar.content, "html.parser")

            # puan = soup2.find_all("div",{"class": "pr-rnr-sm"}).find("span")[0].text
            # Puan almada hata aldığımız için bu ürün bilgisi alınmamıştır.
            
            urun_fiyat = soup2.find("span", {"class": "prc-dsc"}).text
            name_ = soup2.find("h1", {"class": "pr-new-br"})
            urun_marka = name_.a.text
            urun_isim = name_.find("span").text
            urun_foto=soup2.find("div",{"class":"flex-container"}).img.get("src")
            #resimler için img src kullanılmalı
            websiteadi ='Trendyol'#Ürün bilgilerinin veritabanında nasıl görüneceği ayarlanıyor.
            #web site adi alınarak urunun cimri sayfasında hangi siteden geldiği anlasılıyor
            urun_detay = soup2.find_all("ul", {"class": "detail-attr-container"})
            for i in urun_detay:#Ürün detayları alınacak.
                try:
                    isletim_sistemi = i.find_all("b")[2].get_text().strip()
                    #urune ait detaylı bilgiler detya kısmında indekslerde tek tek dolasılarak alınmıstır.
                    urun_islemci = i.find_all("b")[0].get_text().strip()
                    urun_islemci_nesli = i.find_all("b")[26].get_text().strip()
                    urun_Ram = i.find_all("b")[4].get_text().strip()
                    urun_disk_boyutu = i.find_all("b")[16].get_text().strip()
                    urun_disk_turu = "belirtilmemiş"
                    urun_ekran_boyut = i.find_all("b")[20].get_text().strip()
                except:
                    continue
#hata yakalanırsa run edilme devam etsin diye continue ile except blogu içinde devam ettirilmiştir
                Urun_Listesi.append([urun_isim,urun_fiyat, urun_islemci, urun_Ram, urun_marka, urun_ekran_boyut, isletim_sistemi, link, urun_foto,websiteadi])
#append metodu ile urunun ozellikleri urun_listesi adlı listeye eklendi.
for i in Urun_Listesi:#MongoDB'de nasıl sıralanacağı gösteriliyor.
    bson = {
    'urun_isim':i[0],
    'urun_fiyat':i[1],
    'urun_islemci':i[2],
    'urun_Ram':i[3],
    'urun_marka':i[4],
    'urun_ekran_boyut':i[5],
    'isletim_sistemi':i[6],
    'link':i[7],
    'urun_foto':i[8],
    'websiteadi':i[9]
   }
    response=collection.insert_one(bson)
    #for dongusunden cıkmadan her urun bson sayesinde donguyu her girdiğinde birer eleman olarak eklenmiştir.
#TRENDYOL WEB SCRAPPİNG SONU
   
#HEPSİBURADA İLE WEB SİTE BAĞLANTISI KODU
    
client = MongoClient('mongodb://localhost:27017')#local host adresimiz
db = client.EmineŞevval#veritabanının adı
collection = db.Urunler

#ürün özelliklerinin tutulacağı listeler
#baglantının içinde ozellikler teker teker alınamadıgından urunun ozellikleri ayrı ayrı listelere append metodu ile eklenmiştir.
l_ekrankarti = []
l_isletimsistemi = []
l_islemci = []
l_ram = []
l_harddiskkapasitesi = []
l_ekrankarti = []
l_isletimsistemi = []
l_islemcitipi= []
l_ram = []
l_islemcitipi = []
l_link = []
l_garantitipi=[]
l_siteismi=[]
l_isim = []
l_marka = []
l_original_fiyat = []
l_puan = []
l_degerlendirme = []
l_resim = []
l_ekranhafiza = []
l_boyut = []


a=2

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
r = requests.get("https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa=" + str(a) + "",
                     headers=headers)
#hepsiburada için de yaklasık 300 sayfa veri cekilmiştit.
#hepsiburadada str(a) kkısmı için 1 girilemediğinden 2.sayfadan cekmeye basladık
while a<=300:
    #html parser yerine lxml kullandık
    soup = BeautifulSoup(r.content, "lxml")
    st1 = soup.find("div", attrs={"class": "MORIA-voltran-body voltran-body ProductList"})
    st3 = st1.find_all("li", attrs={"class": "productListContent-zAP0Y5msy8OHn5z7T_K_"})
    
    for detaylar in st3:
        #surekli olarak try except blokları sayesinde hata alındıgında kodun run edilişinin durması engellendi.
        #hata alınan girilmeyen yerlere de YOK yazılarak oraların null kalması engellendi.
        try:
            link_sonu = detaylar.a.get("href")#ürün detaylarının linki alınıyor.
            link_bası = "https://www.hepsiburada.com"#hepsibrada'nın linki alınıyor.
            link = link_bası + link_sonu
            l_link.append(link)
            siteismi="HEPSİBURADA"#siteismi eklendi cimri sayfamız için
            #alınan tum ozellikler append metoduyla listelere eklendi
            l_siteismi.append(siteismi)
        
        except:
            link="YOK"
            l_link.append(link)
            #except olup yok olarak kalsa da null deger olmasın diye onlar da listelere eklendi
        r1 = requests.get(link, headers=headers)
        soup1 = BeautifulSoup(r1.content, "lxml")
        try:
            isim = soup1.find("span", attrs={"class": "product-name"}).text#ürün ismi alınıyor
            l_isim.append(isim)
        except:
            isim ="YOK"
            l_isim.append(isim)
        try:
            marka = soup1.find("a", attrs={#ürün markası alınıyor.
                "data-bind": "attr: {'data-hbus': userInformation() && userInformation().userId && isEventReady()? productDetailHbus('BrandClick') : '' }"}).text
            l_marka.append(marka)
        except: 
             marka="YOK"  
             l_marka.append(marka)
        try:
            original_fiyat = soup1.find("del", attrs={"id": "originalPrice"}).text#fiyat alınıyor.
            l_original_fiyat.append(original_fiyat)
        except:
            original_fiyat="YOK"
            l_original_fiyat.append(original_fiyat)
        try:
            puan = soup1.find("span", attrs={"class": "rating-star"}).text.strip()
            l_puan.append(puan)#ürün puanı alınıyor.
        except:
            puan = "YOK"
            l_puan.append(puan)
        try:

            degerlendirme_sayisi = soup1.find("div", attrs={"id": "comments-container"}).text.strip().strip()
            l_degerlendirme.append(degerlendirme_sayisi)
        except:
            degerlendirme_sayisi = "degerlendirme yok"
            l_degerlendirme.append(degerlendirme_sayisi)
        try:
            urun_resmi = soup1.img.get("src")
            l_resim.append(urun_resmi)#ürün resmine erişiliyor.
        except:
            urun_resmi="YOK"
            l_resim.append(urun_resmi)
            
        # urun ozellikleri cekme
        teknikayrinti = soup1.find("div", attrs={"data-bind": "css: {'hidden': keyFeatures().length}"})
        liste = teknikayrinti.find("ul", attrs={"class": ""})
        
        eklenecek = liste.find_all("span")
        sonliste = []
        for i in eklenecek:
            yenieleman = i.text.strip()
            sonliste.append(yenieleman)

        for j in sonliste:#ilk özelliklerden sonra son listeye geçiliyor.
            try:
                garantitipi=sonliste[0]#ürün garantisi alınıyor.
                l_garantitipi.append(garantitipi)
            except:
                garantitipi="YOK"
                l_garantitipi.append(garantitipi)
            try:
                harddiskkapasitesi = sonliste[1]#harddisk kapasitesi alınıyor.
                l_harddiskkapasitesi.append(harddiskkapasitesi)
            except:
                harddiskkapasitesi="YOK"
                l_harddiskkapasitesi.append(harddiskkapasitesi)
            try:
                islemcitipi = sonliste[2]#islemci tipi alınıyor.
                l_islemcitipi.append(islemcitipi)
            except:
                islemcitipi="YOK"  
                l_islemcitipi.append(islemcitipi)
            try:
                islemci= sonliste[3]#islemci alınıyor.
                l_islemci.append(islemci)
            except:
                islemci="YOK"
                l_islemci.append(islemci)
            try:
                isletimsistemi = sonliste[4]#işletim sistemi alınıyor.
                l_isletimsistemi.append(isletimsistemi)
            except:
                isletimsistemi="YOK"
                l_isletimsistemi.append(isletimsistemi)
            try:
                ram = sonliste[5]
                l_ram.append(ram)#ram alınıyor.
            except:
                ram="YOK"
                l_ram.append(ram)
            try:
                ekrankartihafizasi = sonliste[6]
                l_ekranhafiza.append(ekrankartihafizasi)#ekran bilgileri alınıyor.
            except:
                ekrankartihafizasi="YOK"
                l_ekranhafiza.append(ekrankartihafizasi)
            try:  
                ekranboyutu = sonliste[7]
                l_boyut.append(ekranboyutu)
            except:
                ekranboyutu="YOK"
                l_boyut.append(ekranboyutu)
            try:
                ekrankarti = sonliste[8]
                l_ekrankarti.append(ekrankarti)
            except:
                ekrankarti="YOK"
                l_ekrankarti.append(ekrankarti)
            
    a = a + 1       
 #hepsiburadadan tum veriler cekildi 
#hepsiburadadan cekilen veriler ayrı listelere atılmıstı.
#zip metoduyla tum listelerimiz tek bir liste haline geldi   
yeniliste = list(#değerler yazdırılıyor.
    zip(l_isim,l_marka,l_original_fiyat,l_link,l_puan, l_degerlendirme,l_resim,l_garantitipi,l_harddiskkapasitesi, l_islemcitipi,l_islemci,l_isletimsistemi,l_ram,l_ekranhafiza,l_boyut,l_ekrankarti,l_siteismi))
#olusan liste içinde dolasıldı bsona akatarmak için
for i in yeniliste:
    
    bson = {#MongoDB bağlantısı gerçekleştiriliyor.
        'urun_isim':i[0],
        'urun_marka':i[1],
        'urun_fiyat':i[2],
        'link':i[3],
        'l_puan':i[4],
        'l_degerlendirme':i[5],
        'urun_foto':i[6],
       
        'l_garantitipi':i[7],
        'l_harddiskkapasitesi':i[8],
        'l_islemcitipi':i[9],
        'urun_islemci':i[10],
        'isletim_sistemi':i[11],
        'urun_Ram':i[12],
        'l_ekranhafiza':i[13],
        'urun_ekran_boyut':i[14],
        'l_ekrankarti':i[15],
        'websiteadi':i[16]
        
    }
    #insert one ile  donguden cıkılmadan o anki eleman teker teker eklendi
    r=collection.insert_one(bson)   #Bağlantı sonu
#HEPSİBURADA SONU

#N11 İLE WEB SİTE BAĞLANTI KODU

client = MongoClient('mongodb://localhost:27017')
db = client.EmineŞevval#veritabanının adı
collection = db.Urunler
#urunlerin tutulacagı listeler
urun_listesi=[]

header= {
   "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.65"
}
#yine yaklasık 300 veri girildi.
for a in range(1,300):
    url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar?pg="+str(a)#n11 linki alınıyor.
    #a eklenerek sayfalarda dolasılması saglandı

    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
#html.parser kullanıldı.
    list = soup.find_all("li",{"class":"column"})
   
    for li in list:

        urun_ismi = li.div.a.h3.text.strip()
        link = li.div.a.get("href")
        websiteadi="N11"
        #yine cimri sayfası için websiteadi eklendi
        urun_fiyat = li.find("div",{"class":"priceContainer"}).div.find_all("span")[0].text.strip()#ürün fiyatı alınıyor.
        
        urun_puan= li.find("div", {"class":"proDetail"}).find_all("span")[1].text.strip()#puan alınıyor.

        detay=requests.get(link,headers=header).content
        soup2=BeautifulSoup(detay,"html.parser")

        list2=soup2.find_all("div",{"class":"unf-p-lBox"})
        
        a=0
        #hata allma durumunda try except kontrolu ile kodun run edilme sureci durdurulmadı pass sayesinde
        for div in list2:
            try:
                urun_islemci=div.find("div",{"class":"unf-attribute-cover"}).find_all("strong")[0].get_text().strip()#işlemci alınıyor
            except (IndexError,TypeError, AttributeError):
                pass
            
            try:
                urun_bellek=div.find("div",{"class":"unf-attribute-cover"}).find_all("strong")[1].get_text().strip()#bellek alınıyor
            except (IndexError,TypeError, AttributeError):
                bellek= ""
                pass
            
            try:
                urun_bellek=div.find("div",{"class":"unf-attribute-cover"}).find_all("strong")[1].get_text().strip()#bellek alınıyor.
                a=a+1
                
            except (IndexError,TypeError, AttributeError):
                pass
            
            try:
                urun_marka=div.find("div",{"class":"unf-attribute-cover"}).find_all("strong")[2].get_text().strip()#marka alınıyor
            except (IndexError,TypeError, AttributeError):
                pass
            
            try:
                urun_boyut=div.find("div",{"class":"unf-attribute-cover"}).find_all("strong")[3].get_text().strip()#boyut alınıyor
            except (IndexError,TypeError, AttributeError):
                pass
            
            try:
                urun_isletim_sistemi=div.find("div",{"class":"unf-attribute-cover"}).find_all("strong")[4].get_text().strip()#işletim sistemi alınıyor
            except (IndexError,TypeError, AttributeError):
                pass
            
            try:
                urun_foto=div.img.get("data-src")#ürün resmi alınıyor.
            except (IndexError,TypeError, AttributeError):
                pass    
    
    
            urun_listesi.append([urun_ismi,urun_puan,urun_fiyat,urun_islemci,urun_bellek,urun_marka,urun_boyut,urun_isletim_sistemi,link,urun_foto,websiteadi])
            for i in urun_listesi:#özellikler getiriliyor
            #urun_listesinde dolasılarak bsona eklenildi.
                bson = {#MongoDB'de bağlantısı
                    'urun_isim':i[0],
                    'puan':i[1],
                    'urun_fiyat':i[2],
                    'islemci':i[3],
                    'bellek':i[4],
                    'urun_marka':i[5],
                    'urun_ekran_boyut':i[6],
                    'isletim_sistemi':i[7],
                    'websiteadi':i[8],
                    'link':i[9],
                    'urun_foto':i[10]}
                
                    
            html=collection.insert_one(bson)#bağlantı sonu
            #donguden cıkılmadan bsona tum ozellikler eklendi.
#n11 bitti
        
#VATAN baslıyor

client = MongoClient('mongodb://localhost:27017')
db = client.EmineŞevval#Veritabanının adı
collection = db.Urunler

urun_liste=[]
#vatandan sadece 20 sayfa veri geldi.
for sayfa in range(1,21):
#sayfa ilerledikce url degişiyor bu sayede ilerleyen sayfalardan bilgileri cekebiliyoruz.      
   url = "https://www.vatanbilgisayar.com/notebook/?page={}".format(sayfa)#vatan linki alınıyor.
#lxml yerine html.parser kullandık.
   parser=BeautifulSoup(requests.get(url).content,"html.parser")

   veri=parser.find("div",{"class":"wrapper-product wrapper-product--list-page clearfix"})\
   .find_all("div",{"class":"product-list product-list--list-page"})#ürünlerin linkine erişiliyor.

#veri listesinin içinde gezinerek diğer ozellikler de cekildi.
   for i in veri:
       #h3 baslıgından urunbilgisi cekildi.
      urunbilgisi=i.find("div",{"class":"product-list__product-name"}).find("h3").text
     #split metoduyla urun bilgisinde yer allan - ler kaldırıldı boylece istediğimiz elemanları teker teker cektik indeksleriyle
      yeniliste=urunbilgisi.split("-")
      urun_ismi=yeniliste[0]#isim getiriliyor
      
      yeniliste2=urun_ismi.split(" ")
      urun_marka=yeniliste2[0]#marka getiriliyor.
      
      urun_Ram=yeniliste[1]#ram getiriliyor

      urun_islemci=yeniliste[2]
      urun_ekran_boyutu=yeniliste[3]#ürün özellikleri getiriliyor.
      urun_fiyat=i.find("span",{"class":"product-list__price"}).text#fiyatlar text şeklinde alınıyor.
      urun_modelNoliste=i.find("div",{"class":"product-list__product-code"}).text.split()
      #urun modelnosu bosluklu geliyordu o yuzden ilk elemanını aldık.
      urun_modelNo=urun_modelNoliste[0]
      
      header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
   
      for detaylar in veri:
          
         linksonu = detaylar.a.get("href")
         linkbası = "https://www.vatanbilgisayar.com"#vatan linki
         link =linkbası+linksonu#linkler birleşiriliyor.

         detay=requests.get(link,headers = header)
         detay_soup=BeautifulSoup(detay._content,"lxml")
         teknik_ayrıntılar= detay_soup.find_all("ul",{"class":"pdetail-property-list"})
         
      urun_puan=i.find("div",{"class":"product-list__content"}).find("div",{"class":"wrapper-star"}).text.strip()#puan alınıyor.
      websiteadi="VATANBİLGİSAYAR"#cimri için
      #foto alınca alınabiecek hatalar exceptle belirtildi.
      try:
       urun_foto=i.img.get("data-src")#ürün resmi alınıyor.
      except (IndexError,TypeError, AttributeError):
       pass    
#tum urunler urun_liste sine eklendi.
      urun_liste.append([urun_ismi,urun_Ram,urun_puan,urun_marka,link,urun_fiyat,urun_foto,urun_islemci,urun_ekran_boyutu,websiteadi,urun_modelNo])
for i in urun_liste:#özellikler listeleniyor
              bson = {#MongoDB bağlantısı
                  'urun_isim':i[0],
                  'urun_Ram':i[1],
                  'urun_puan':i[2],
                  'urun_marka':i[3],
                  'link':i[4],
                  'urun_fiyat':i[5],
                  'urun_foto':i[6],
                  'urun_islemci':i[7],
                  'urun_ekran_boyutu':i[8],
                  'websiteadi':i[9],
                  'modelNo':i[10]}
              parser=collection.insert_one(bson)    #bağlantı sonu         
#bsona aktarıldı