#In[1]:
import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

settings = json.loads( open('settings.json').read() )

API_KEY = settings['tone_analyzer_apikey']
VERSION_TONE_AN = '2019-03-07'
URL_TONE_AN = settings['tone_analyzer_url']

authenticator = IAMAuthenticator(API_KEY)
tone_analyzer = ToneAnalyzerV3(
    version=VERSION_TONE_AN,
    authenticator=authenticator
)

tone_analyzer.set_service_url(URL_TONE_AN)
#In[2]:

tone_analyzer.set_disable_ssl_verification(True)

text = 'I hate eat chocolate!'
    
tone_analysis = tone_analyzer.tone(
    {'text': text},
    content_type='application/json', 
    accept_language='es'
).get_result()
print(json.dumps(tone_analysis, indent=2))

# %%
tone_analysis

# %%
