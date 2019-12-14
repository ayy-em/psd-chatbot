from google.cloud import firestore
import json

def store(update_json):
    psdlkmsg_photo = psdlkmsg_sticker = psdlkmsg_audio = False
    psdlkmsg_audio_duration = 0
    psdlkmsg_sticker_emoji = ''
    psdlkmsg_text = ''
    psdlkmsg = update_json['message']
    psdlkmsg_id = psdlkmsg['message_id']
    psdlkmsg_date = psdlkmsg['date']
    if 'text' in psdlkmsg:
        psdlkmsg_text = psdlkmsg['text']
    elif 'sticker' in psdlkmsg:
        psdlkmsg_text = ''
        psdlkmsg_sticker = True
        psdlkmsg_sticker_emoji = str(psdlkmsg['sticker']['emoji'])
    elif 'photo' in psdlkmsg:
        psdlkmsg_text = ''
        psdlkmsg_photo = True
    elif 'voice' in psdlkmsg:
        psdlkmsg_text = ''
        psdlkmsg_audio = True
        psdlkmsg_voice = psdlkmsg['voice']
        psdlkmsg_audio_duration = psdlkmsg_voice['duration']
    else:
        psdlkmsg_text = ''
    psdlkmsg_from = psdlkmsg['from']
    psdlkmsg_from_id = psdlkmsg_from['id']
    if 'first_name' in psdlkmsg_from.keys():
        psdlkmsg_from_fn = psdlkmsg_from['first_name']
    else:
        psdlkmsg_from_fn = ''
    if 'last_name' in psdlkmsg_from.keys():
        psdlkmsg_from_ln = psdlkmsg_from['last_name']
    else:
        psdlkmsg_from_ln = ''
    if 'username' in psdlkmsg_from.keys():
        psdlkmsg_from_un = psdlkmsg_from['username']
    else:
        psdlkmsg_from_un = ''

    db = firestore.Client()
    doc_ref = db.collection(u'psdlkcollection').document(u'psdlkstatsdoc')
    messages_ref = doc_ref.collection(u'messages').document(str(psdlkmsg_id))
    messages_ref.set({
        u'id': psdlkmsg_id,
        u'date': psdlkmsg_date,
        u'text': psdlkmsg_text,
        u'photo': psdlkmsg_photo,
        u'voice': psdlkmsg_audio,
        u'voice_duration': psdlkmsg_audio_duration,
        u'sticker': psdlkmsg_sticker,
        u'sticker_emoji': psdlkmsg_sticker_emoji,
        u'from_id': psdlkmsg_from_id,
        u'from_fn': psdlkmsg_from_fn,
        u'from_ln': psdlkmsg_from_ln,
        u'from_un': psdlkmsg_from_un
    })

"""
# leftover from testing, keep it
if __name__ == '__main__':
    import sys
    # function = getattr(sys.modules[__name__], sys.argv[1])
    # filename = sys.argv[2]
    # function(filename)
    function = getattr(sys.modules[__name__], sys.argv[1])
    function()
"""
