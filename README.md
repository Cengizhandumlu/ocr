# Fatura OCR ve Veri Çıkarma Sistemi

  Bu proje, **Optik Karakter Tanıma (OCR)** ve **Adlandırılmış Varlık Tanıma (NER)** modellerini kullanarak PDF formatındaki faturalar üzerinden otomatik olarak yapılandırılmış veri çıkarmayı amaçlamaktadır.

## Temel Özellikler

- **OCR (Optik Karakter Tanıma) ile Metin Çıkarma:**  
    PDF sayfalarını görüntülere çevirerek EasyOCR ile metin tanıma işlenmesi.
  
- **NER (Adlandırılmış Varlık Tanıma) ile Bilgi Çıkarma:**  
    Önceden eğitilmiş **BERT modeli**, faturadaki önemli varlıkları (tarih, fatura numarası, müşteri adı, vergi numarası vb.) tanımlanması.
  
- **Ürün ve Fatura Bilgileri Çıkarma:**  
    Ürün kodları, miktarlar, birim fiyatlar ve toplam tutarları tespit edilmesi.

- **Yapılandırılmış Veri Çıktısı:**  
    Çıkarılan veriler **JSON formatında** kaydedilerek daha kolay erişilebilir hale getirilmesi.


## Çalışma Akışı

** PDF’ten Görsele Dönüştürme:**  
   `pdf2image` kütüphanesi kullanılarak her fatura sayfası bir görsele dönüştürür.

** OCR ile Metin Tanıma:**  
   EasyOCR kütüphanesi kullanılarak faturadan metin çıkarma işlemi gerçekleştirir.

** NER Analizi ile Bilgi Çıkarma:**  
   OCR ile çıkarılan metin, BERT tabanlı **Adlandırılmış Varlık Tanıma (NER)** modeli ile analiz edilir ve anahtar bilgiler elde eder:
   - **Fatura Tarihi**
   - **Müşteri Bilgileri**
   - **Fatura Numarası**
   - **Vergi Numarası**
   - **Ürün Listesi**

** Yapılandırılmış Veri Haline Getirme:**  
   Tüm bilgiler json kütüphanesi ile JSON formatına dönüştürülerek kaydedilir.
   
## Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|-----------|----------|
| **Python 3.8 | Projenin ana programlama |
| **EasyOCR** | OCR işlemleri için |
| **pdf2image** | PDF’leri görüntüye dönüştürmek |
| **BERT (Hugging Face Transformers)** | Metinleri analiz edip anlamlandırmak |
| **re (Düzenli İfadeler)** | Fatura verilerini ayıklamak |
| **JSON** | Çıktıları yapılandırılmış formatta saklamak |

## Kurulum

Projenin bilgisayara github üzerinden clone edilmesi:
    git clone https://github.com/Cengizhandumlu/ocr

### Gerekli Kütüphaneleri Yükleyin

Proje kullanılmadan önce aşağıdaki bağımlılıkların yüklenmesi:
    pip install easyocr pdf2image transformers numpy regex




