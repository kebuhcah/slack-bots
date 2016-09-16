import json
import urllib2,urllib
import pandas as pd
from pandas import DataFrame
import time
import random

tokens=pd.read_csv('../tokens')

userToken=tokens.set_index('tokenType').ix['userToken'].tolist()[0]
botToken=tokens.set_index('tokenType').ix['botToken'].tolist()[0]

generalId='C2841BJFQ'
markovId='C28EW0GU8'

markovUrl='https://hooks.slack.com/services/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'

req = urllib2.Request('https://slack.com/api/channels.history?'+urllib.urlencode({
            'token':userToken,
            'channel': markovId,
            'count': 1000,
            'pretty':1}))
req.add_header('Content-Type', 'application/json; charset=utf-8')
response = urllib2.urlopen(req)
markovHistory=DataFrame(json.load(response)['messages'])

content=pd.read_csv("markov_content.csv",delimiter="|")

markovText = markovHistory[(markovHistory.username.fillna('').str.startswith('Markov '))&(markovHistory.username!='Markov Cthulhu')].text.tolist()
premarkovText = content.message.str.strip().tolist()

material = [s for s in (' $$$ '.join(markovText + premarkovText) + ' $$$').split(' ') if s]

markovmap = {}
maxchainlength=3
for i in range(0,len(material)):
    token = material[i]
    if not token in markovmap:
        markovmap[token]={}
        for j in range(1,maxchainlength):
            markovmap[token][j]={}
    for j in range(1,maxchainlength):
        if i+j < len(material):
            chain = ' '.join(material[i+1:i+j+1])
            if '$$$ ' in chain:
                continue
            if chain in markovmap[token][j]:
                markovmap[token][j][chain]=markovmap[token][j][chain]+1
            else:
                markovmap[token][j][chain]=1

def growMarkov(src=''):
    lastword = src.split(' ')[-1] if src else '$$$'
    #print lastword
    nextword = (lambda t:random.choice([v for s in [[x]*t[x] for x in t.index] for v in s]))(pd.Series(markovmap[lastword][1]))
    if nextword == '$$$':
        return src
    else:
        return growMarkov(src + ' ' + nextword if src else nextword)

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

while True:
    text = growMarkov()
    slackPost(text,'Markov Cthulhu',':cthulhu:','#random')
    sleeptime = len(text) * 7
    print sleeptime
    time.sleep(sleeptime)
