import os
import json
from pdf2image import convert_from_path
import easyocr
import re
import numpy as np
from transformers import BertTokenizer, BertForTokenClassification, pipeline

pdfPath = "/Users/cengizhandumlu/Documents/Develop/python/ocr/invoice/" #PDF path alındı.

ocrReader = easyocr.Reader(['en']) #OCR reader initilize edildi ingilizce dili ile birlikte.

tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english") #Önceden eğitilmiş bir BERT modeline ait tokenizer initilize edildi.
model = BertForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english") #Tokenlar için sınıflandırma yapacak olan model initilize edildi.

nlpNER = pipeline("ner", model=model, tokenizer=tokenizer) #NER işlemleri için pipeline oluşturuldu.

ocrResult = [] #OCR sonuçlarının tutulacağı liste oluşturuldu.

# pdf dosyalarının birer image olarak okunması ve OCR işlemlerinin yapılması.
for pdfFile in os.listdir(pdfPath):
    if pdfFile.endswith(".pdf"):
        path = os.path.join(pdfPath, pdfFile)
        
        images = convert_from_path(path, 500) #500 dpi ile pdf dosyası image olarak okundu.

        for i, image in enumerate(images, start=1):
            npPage = np.array(image)
            result = ocrReader.readtext(npPage) #Gerçekleştirilen OCR sonucu result değişkenine atandı.
            pageNext = ""
            for text in result:
                pageNext = pageNext + text[1] + "\n"
            ocrResult.append({
                "file": pdfFile,
                "page": i,
                "text": pageNext
            })

#Çıkarılan textlerin temizleme işlemini gerçekleştiren fonksiyon.
def cleanText(text):
    text = re.sub(r'\s+', ' ', text) #birden fazla boşluk tek boşlukla birleştirildi.
    text = re.sub(r'\s*\.\s*', '.', text) #arada birden fazla boşluk olan noktalama işaretleri tek noktaya dönüştürüldü.
    text = re.sub(r'\s*-\s*', '-', text) #arada birden fazla boşluk olan tire işaretleri tek tireye dönüştürüldü.
    text = re.sub(r'\s*\:\s*', ':', text) #arada birden fazla boşluk olan iki nokta işaretleri tek iki noktaya dönüştürüldü.
    return text.strip()

def getInvoiceDate(text): #tarihlerin alınması
    patternDate = r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}\s\w+\s\d{4})"
    dates = re.findall(patternDate, text)
    if dates:
        return dates[0]
    else:
        return ""
    
def getInvoiceDetails(text): #fatura detaylarının alınması
    patternProduct = r"PRD-\d+"
    patternQTY = r"(?:Qty|Quantity):\s*(\d+)"
    patternPrice = r"Price:\s*\$?([\d\.,]+)"
    patternTotal = r"Total:\s*\$?([\d\.,]+)"
    patternPOnumber = r"PO\s*[-:]\s*(PO-\d+)"

    products = re.findall(patternProduct, text)
    quantities = re.findall(patternQTY, text)
    prices = re.findall(patternPrice, text)
    totals = re.findall(patternTotal, text)
    poNumbers = re.findall(patternPOnumber, text)

    items = []
    for i in range(len(products)):
        item = {}
        if i < len(products):
            item["product"] = products[i]
        else:
            item["product"] = ""
        if i < len(quantities):
            item["quantity"] = quantities[i]
        else:
            item["quantity"] = ""
        if i < len(prices):
            item["price"] = prices[i]
        else:
            item["price"] = ""
        if i < len(totals):
            item["total"] = totals[i]
        else:
            item["total"] = ""
        if i < len(poNumbers):
            item["po_number"] = poNumbers[i]
        else:
            item["po_number"] = ""
        items.append(item)
    
    return items

def processOCRdata(text):
    cleanedText = cleanText(text)
    entities = nlpNER(cleanedText)

    invoiceData = {
        "company": "",
        "invoice_date": "",
        "invoice_number": "",
        "customer": "",
        "address": "",
        "tax_id": "",
        "items": []
    }

    invoiceData["date"] = getInvoiceDate(cleanedText)

    for entity in entities:
        word = entity['word']
        entityType = entity['entity']

        if entityType == "DATE":
            invoiceData["invoice_date"] = word
        elif entityType == "MISC" and "INV-" in word:
            invoiceData["invoice_number"] = word
        elif entityType == "ORG" and "Tech" in word:
            customerWords = []
            for e in entities:
                if e['entity'] == "LTD":
                    customerWords.append(e['word'])
        elif entityType == "LOC" and word[0].isupper():
            invoiceData["address"] = word
        elif entityType == "MISC" and word.startswith("US"):
            invoiceData["tax_id"] = word
    
    invoiceData["items"] = getInvoiceDetails(cleanedText)
    
    return invoiceData

data = [] #OCR sonuçlarının işlenmiş hali için liste oluşturuldu.
for item in ocrResult:
    text = item['text']
    processedData = processOCRdata(text)
    data.append(processedData)

jsonFilePath = "/Users/cengizhandumlu/Documents/Develop/python/ocr/invoice/invoice_output.json" #işlenmiş OCR sonuçlarının json dosyası olarak kaydedileceği path.

with open(jsonFilePath, "w") as f:
    json.dump(data, f, indent=4)

print(json.dumps(data, indent=4))

