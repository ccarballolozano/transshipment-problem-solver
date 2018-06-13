import requests
import json

url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=Seattle&destinations=San+Francisco&mode=driving&sensor=false"
r = requests.get(url)
print(json.loads(r.text))