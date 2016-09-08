import json
import urllib2
import pandas as pd
import time

lieblichUrl='https://hooks.slack.com/services/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'
markovUrl='https://hooks.slack.com/services/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'

def slackPost(text,username=None, icon_emoji=None, channel='#random', url=markovUrl):
    data = {
        'username': username,
        'icon_emoji': icon_emoji,
        'channel': channel,
        'text': text
    }

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))

    print response

content=pd.read_csv("markov_content.csv",delimiter="|")
content.columns=content.columns.str.strip()
content['user']=content['user'].str.strip()
content['message']=content['message'].str.strip()

user_emoji_map = {
    'Attila' : ':skull:',
    'Carla' : ':smiley_cat:',
    'Amilcar' : ':sleeping:',
    'R-G' : ':upside_down_face:',
    'Andy' : ':hand:',
    'Roy' : ':thinking_face:',
    'David' : ':smiling_imp:',
    'Akira' : ':japanese_goblin:',
    'Nanfei' : ':bird:',
    'Shelley' : ':shell:',
    'Jinnie' : ':dog2:',
    'Hai-Long' : ':dragon:',
    'Gabor' : ':sheep:',
    'Dusan' : ':stuck_out_tongue_winking_eye:',
    'Derek' : ':neutral_face:',
    'Huy Quang' : ':flashlight:',
    'Ivett' : ':cocktail:',
    'Anand' : ':boy::skin-tone-5:',
    'Kevin' : ':fire:',
    'Szabolcs' : ':crossed_swords:',
}

for i in range(0,len(content)):
    user = content.ix[i]['user']
    message = content.ix[i]['message']
    print user, message
    try:
        slackPost(message, 'Markov ' + user, user_emoji_map[user], '#markov')
        time.sleep(60)
    except Exception as e:
        print 'FAILED!'
