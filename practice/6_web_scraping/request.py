import requests
# %%
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
# %% [markdown]
# We'll cache the request responses to not hit the rate limits and for faster testing

# %%
## Make sure to not clear the cache on accident!
response_cache = {}

# %%
def request(url: str):
    try:
        return response_cache[url]
    except:
        pass
    r = requests.get(url, headers=headers)
    response_cache[url] = r
    return r