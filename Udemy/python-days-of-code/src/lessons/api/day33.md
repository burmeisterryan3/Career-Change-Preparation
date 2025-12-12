# API Introduction

## Requests Call

```
import requests

response = requests.get(url="http://api.open-notify.org/iss-now.json")
print(response)
```

## Response Codes
* 1XX - Hold On - Informational
* 2XX - Here you go - Success
* 3XX - Go away - Redirection
* 4XX - You screwed up - Client Error
* 5XX - I screwed up - Server Error

