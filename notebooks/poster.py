import json
import urllib2
import pandas as pd
import time, datetime

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
    'Lorant' : ':beer:',
    'Alexandre' : ':robot_face:',
    'Devin' : ':alien:',
    'Vaibhav' : ':wheel_of_dharma:',
    'Mariano' : ':flag-ar:',
    'Jason' : ':beers:',
    'Sanjay' : ':soccer:',
    'Ran' : ':runner:'
}

for i in range(0,len(content)):
    user = content.ix[i]['user']
    message = content.ix[i]['message']
    secondsPerPost = 0
    if len(content) != i and True:
        #remainingPosts = len(content) - i - 1
        #remainingSeconds = (datetime.datetime(2016, 9, 16, 7) - datetime.datetime.now()).total_seconds()
        #secondsPerPost = remainingSeconds / remainingPosts
        secondsPerPost = 300
    print i,
    try:
        slackPost(message, 'Markov ' + user, user_emoji_map[user], '#markov')
        print secondsPerPost / 60, 'minutes till next post'
        time.sleep(secondsPerPost)
    except Exception as e:
        print e
        print 'FAILED!', user, message
