import json
import pandas as pd
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

def nlpEmotion(data):
    try:
        cred = credential.Credential("AKIDVp23tXPLSSN7f2nJG4iIgssiMo36cc4K", "CC0fKo6C5pmokYzHNH1c1EF4lEVfeQ0O")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)
        if(len(data)>200):
            data=data[0:199]

        req = models.SentimentAnalysisRequest()
        params = {
            "Text": data,
            "Mode":'3class'
        }
        req.from_json_string(json.dumps(params))

        resp = client.SentimentAnalysis(req)
        print(resp.to_json_string())
        return resp

    except TencentCloudSDKException as err:
        print(err)
        return ''



def judge_null(column):
    if pd.isna(column):
        return '\n'
    if len(column)<0:
        return '\n'
    return column

data = pd.read_csv('知乎三孩.csv')
data['回答'] = data['回答'].apply(lambda x : judge_null(x).replace('\n', ''))
# data['回答'] = data['回答'].apply(lambda x : judge_null(x).replace('\n', ''))
data['qg'] = data['回答'].apply(lambda x : nlpEmotion(x))
all_words = data['qg'].to_list()
qg_dict = {}
qg_dict['negative']=0
qg_dict['positive']=0
qg_dict['neutral']=0
f_txt = open('qg.txt', 'w+', encoding='utf_8')
for word in all_words:
    if(not word==''):
        word = json.loads(str(word))
        if word['Sentiment'] == 'negative':
            qg_dict['negative'] += 1
        if word['Sentiment'] == 'positive':
            qg_dict['positive'] += 1
        if word['Sentiment'] == 'neutral':
            qg_dict['neutral'] += 1

for k,v in qg_dict.items():
    f_txt.write(str(k) + ':'+str(v)+'\n')

