from google.cloud import firestore
import datetime
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
    messages = doc_ref.collection(u'messages')
    date_st = datetime.datetime.now().timestamp() - 31500 - 86400
    date_fn = date_st + 86400
    list_of_yest_numbers = []
    # i was probably super high when i did this but it's so hilarious i'm keeping it
    for id in ids_of_psdlk:
        i = 0
        chuvak_messages = messages.where(u'from_id',u'==',id).where(u'date',u'>',date_st).where(u'date',u'<',date_fn).stream()
        for doc in chuvak_messages:
            i += 1
        list_of_yest_numbers.append(i)
        # print('chuvak id ' + str(id) + ' - ' + str(i) + ' postov.')
    return list_of_yest_numbers

def store_stats_for_yesterday(stats):
    db = firestore.Client()
    doc_ref = db.collection(u'psdlkcollection').document(u'psdlkstatsdoc')
    stats_doc_name = datetime.datetime.now().date()
    messages_ref = doc_ref.collection(u'daily_stats').document(str(stats_doc_name))
    messages_ref.set({
        'DavMan' : stats[0],
        'Dell' : stats[1],
        'NaniS' : stats[2],
        'wocetake' : stats[3],
        'Got the life' : stats[4],
    })
    print('--storing stats ok')

def get_stats_msg():
    list = get_data()
    store_stats_for_yesterday(list)
    spam = max(list)
    overall_messages = sum(list)
    spammer_ind = list.index(max(list))
    spammer = names_of_psdlk[spammer_ind]
    spam_ratio = round(float(spam) / float(overall_messages),2)*100
    print(spam_ratio)
    """
    non_retarded_list = []
    for item, name in zip(list, names_of_psdlk):
        non_retarded_list.append(name + ': ' + str(item) + ' msgs.')
        print(name + ': ' + str(item) + ' msgs.')
    """
    stats_msg = '\n\n🤓 Спаммер вчера: \n\t\t* ' + str(spammer) + '!* - ' + str(spam) + ' сообщений, ' + str(round(spam_ratio,1)) + '% от тотала. Всего сообщений - ' + str(overall_messages) + '.'
    return stats_msg

def get_daily_stats_collection():
    db = firestore.Client()
    doc_ref = db.collection(u'psdlkcollection').document(u'psdlkstatsdoc')
    daily_stats_collection = doc_ref.collection(u'daily_stats').stream()
    return daily_stats_collection
