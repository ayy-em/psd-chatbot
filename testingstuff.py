from google.cloud import firestore
import datetime
import csv
import json

## Ids
# dav - 171258213
# j - 135499785
# Alex - 61178981
# serg - 215950478
# egor - 154100195
ids_of_psdlk = [171258213, 135499785, 61178981, 215950478, 154100195]
names_of_psdlk = ['DavMan', 'Dell', 'NaniS', 'wocetake', 'Got the life']

def get_data():
    db = firestore.Client()
    doc_ref = db.collection(u'psdlkcollection').document(u'psdlkstatsdoc')
    messages = doc_ref.collection(u'messages').stream()
    to_csv_list = []
    for doc in messages:
        from_whom = doc.get('from_fn')
        from_date = from_ts(doc.get('date'))
        thing = [from_date,from_whom]
        to_csv_list.append(thing)
    with open('teststats.csv', 'w+') as opencsv:
        writerino = csv.writer(opencsv, delimiter=',')
        writerino.writerows(to_csv_list)

def from_ts(unx_ts):
    dayreal = datetime.datetime.fromtimestamp(unx_ts).date()
    return dayreal

get_data()