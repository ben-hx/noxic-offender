


url = "https://hooks.slack.com/services/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"
params = {"text": "jo"}
headers={'content-type': 'application/json'}



import requests
r = requests.post(url, json=params, headers=headers)
