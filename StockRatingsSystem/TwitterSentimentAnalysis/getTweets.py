import json
import requests
from requests.auth import AuthBase

# Fill these in. Generate tokens at /content/developer-twitter/en/apps. 
CONSUMER_KEY = 'nd7CFVu8evt6hOmKy5foUiKtr'
CONSUMER_SECRET = 'nFzQAdPle23I43sBrVKFPqWNhnBBXSLpksTg2T28KRFBhgO9u7'

base_url = 'https://api.twitter.com/2/tweets/search/recent?max_results='

headers = {
    "Accept-Encoding": "gzip"
}

# Generates a bearer token with consumer key and secret via https://api.twitter.com/oauth2/token.
class BearerTokenAuth(AuthBase):
    def __init__(self, consumer_key, consumer_secret):
        self.bearer_token_url = "https://api.twitter.com/oauth2/token"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.bearer_token = self.get_bearer_token()

    def get_bearer_token(self):
        response = requests.post(
            self.bearer_token_url,
            auth=(self.consumer_key, self.consumer_secret),
            data={'grant_type': 'client_credentials'},
            headers={'User-Agent': 'LabsRecentSearchQuickStartPython'})

        if response.status_code is not 200:
            raise Exception("Cannot get a Bearer token (HTTP %d): %s" % (response.status_code, response.text))

        body = response.json()
        return body['access_token']

    def __call__(self, r):
        r.headers['Authorization'] = "Bearer %s" % self.bearer_token
        r.headers['User-Agent'] = 'LabsResearchSearchQuickStartPython'
        return r

# Script starts here.

#Create Bearer Token for authenticating with recent search.
def getTweets(stock_symbol,max_result):
    bearer_token = BearerTokenAuth(CONSUMER_KEY, CONSUMER_SECRET)
    
    url = base_url+max_result+"&query="+stock_symbol+" stock"
    
    #Make a GET request to the Labs recent search endpoint.
    response = requests.get(url, auth=bearer_token, headers = headers)
    
    if response.status_code is not 200:
        raise Exception("Request reurned an error: %s" % (response.status_code, response.text))
    
    #Display the returned Tweet JSON.
    parsed = json.loads(response.text)
    #pretty_print = json.dumps(parsed, indent=2, sort_keys=True)
    #print (pretty_print)
    
    tweets_fetched = []
    for item in parsed['data']:
        tweets_fetched.append((str)(item['text']))
        #t = (str)(t.text.encode("utf-8"))
    #print(tweets_fetched)
    return tweets_fetched
    
if __name__ == '__main__':
    stock_symbol = "AAPL"
    max_result = '11'
    getTweets(stock_symbol,max_result)