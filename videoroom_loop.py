import requests
import json
import random
import string
import time

api = 'http://localhost:8088/janus'


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def call(data):
    data['transaction'] = randomString()
    return requests.post(api, data=json.dumps(data)).json()


def call_session(session, data):
    url = "{}/{}".format(api, session)
    data['transaction'] = randomString()
    return requests.post(url, data=json.dumps(data)).json()


def call_handle(session, handle, data):
    url = "{}/{}/{}".format(api, session, handle)
    data['transaction'] = randomString()
    return requests.post(url, data=json.dumps(data)).json()


def mk_session():
    return call({'janus': 'create'})['data']['id']


def mk_handle(session):
    return call_session(session, {'janus': 'attach', 'plugin': 'janus.plugin.videoroom'})['data']['id']


def get_events(session):
    url = "{}/{}?maxev=1".format(api, session)
    return requests.get(url).json()


def get_pub_ids(session, handle):
    response = call_handle(session, handle, {'janus': 'message', 'body': {
                           'request': 'listparticipants', 'room': 1234}})
    participants = response['plugindata']['data']['participants']
    return [part['id'] for part in participants if part['publisher'] == True]


def subscribe(session, handle, pubid):
    return call_handle(session, handle, {'janus': 'message', 'body': {
        'request': 'join',
        'ptype': 'subscriber',
        'room': 1234,
        'feed': pubid,
        'video': True,
    }})


def join_pub(session, handle):
    return call_handle(session, handle, {'janus': 'message', 'body': {
        'request': 'join',
        'ptype': 'publisher',
        'room': 1234,
    }})


def offer(session, handle, sdp):
    return call_handle(session, handle, {'janus': 'message', 'body': {
        'request': 'configure',
        'audio': True,
        'video': True
    },
        'jsep': {
            'type': 'offer',
            'trickle': False,
            'sdp': sdp
    }
    })


def start_send(session, handle, sdp):
    return call_handle(session, handle, {'janus': 'message', 'body': {
        'request': 'start',
    },
        'jsep': {
            'type': 'answer',
            'sdp': sdp
    }
    })


def leave(session, handle):
    return call_handle(session, handle, {'janus': 'message', 'body': {'request': 'leave', }})


def detach(session):
    return call_session(session, {'janus': 'detach'})


session = mk_session()
handle = mk_handle(session)
pub_ids = get_pub_ids(session, handle)
subscribe(session, handle, pub_ids[0])

sdp_offer = get_events(session)['jsep']['sdp']

pub_handle = mk_handle(session)
join_pub(session, pub_handle)
offer(session, pub_handle, sdp_offer)
print('Send offer')
get_events(session)
sdp_answer = get_events(session)['jsep']['sdp']
start_send(session, handle, sdp_answer)

for x in range(2):
    print(get_events(session))

time.sleep(10)
leave(session, pub_handle)
leave(session, handle)
detach(session)
