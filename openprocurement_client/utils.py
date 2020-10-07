from openprocurement_client.my_client import Client
import json
from munch import munchify
import io
import os
import wget
import shutil


def get_tenders_list(client=Client(''), id_field='tenderID',descending=True):
    params = {'opt_fields': id_field,'descending': descending}
    client._update_params(params)
    tender_list = True
    while True:
        if not tender_list:
            return
        while tender_list:
            tender_list = client.get_tenders()
            for tender in tender_list:
                yield tender

def get_tender_id_by_uaid(ua_id, descending=True, id_field='tenderID',client=Client('')):
    params = {'opt_fields': id_field, 'descending': descending}
    tender_list = True
    client._update_params(params)
    while tender_list:
        tender_list = client.get_tenders()
        for nom in tender_list:
            if nom[id_field] == ua_id:
                return nom.id
    raise IdNotFound


def get_tender_by_id(tender_id='tenderID',client=Client('')):
    tender = client.get_tender(tender_id)
    #document = client.get_documents(tender)
    #encoded_tender = json.dumps(tender)
    decoded_tender = json.loads(tender)
    
    return decoded_tender

def verifyDirs(BaseDir, nameDir):
    EndDir = os.path.join(BaseDir, nameDir)
    IsDir = False
    for dirs,folder,files in os.walk(BaseDir):
        for m in folder:
            if m == nameDir:
                IsDir = True
                break
    if not IsDir:
        os.mkdir(EndDir)
    return EndDir

def save_doc(wayDir, tender):
    try:
        doc = tender['data']['documents']
        for eachDoc in doc:
            if eachDoc['url']:
                print(eachDoc['url'])
                fileName = eachDoc['title']
                docFile = wget.download(eachDoc['url'])
                shutil.move(docFile, os.path.join(wayDir,fileName))
                print(fileName)
    except: print('не має документів')             

def save_tender(id,filtrs = False):
    verifyDirs('D:\Projects','Tenders')
    tender = get_tender_by_id(id)
    UA_ID = tender['data']['tenderID']
    print(id)
    print(UA_ID)
    if filtrs:
        if tender['data']['items'][0]['classification']['id'] != filtrs:
            print('Этот тендер не попадает под фильтр')
            return
    print(tender['data']['title']) 
    print(tender['data']['value']['amount'])
    print(tender['data']['items'][0]['classification']['id'])
    wayDir = verifyDirs('D:\Projects\Tenders',UA_ID)
    with io.open('{}\{}.json'.format(wayDir, UA_ID), 'w', encoding='utf8') as outfile:
        str_ = json.dumps(tender,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
        outfile.write(str_)
    save_doc(wayDir, tender)

def start():
    print('Выберите варианты поиска:')
    print('1.Поиск по "ID"')
    print('2.Поиск по "ID_UA"')
    print('3.Список тендеров на сегодня c фильтром по ДК 021:2015')
    print('**************************************************************')

    choise = int(input('Введите нужное число: '))
    if choise == 1:
        id_tender = input('tender ID: ')
        save_tender(id_tender)
    elif choise == 2:
        tender_ua_id = input('tender UA_ID: ')
        id_tender = get_tender_id_by_uaid(tender_ua_id)
        save_tender(id_tender)
    elif choise == 3:
       tender_info = get_tenders_list()
       filter = input('ДК 021:2015: ')
       for i in tender_info:
           save_tender(i['id'], filter)
           print(i)
    elif choise > 4:
       return print('Неверный выбор')

start()
