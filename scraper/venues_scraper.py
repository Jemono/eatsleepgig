import requests

url = "https://www.neckofthewoods.co.nz/api/block/render"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "x-csrf-token": "WkxVXcS5c_qYjQ4NmQ4ZDY4ZDJlZTYxNjZkYTE3MDk3ZmI5Yjc1'",  # from DevTools
    "Cookie": "crumb=WkxVXcS5c_qYjQ4NmQ4ZDY4ZDJlZTYxNjZkYTE3MDk3ZmI5Yjc1'; ss_cvr=...; ss_cvt=..."  # copy from Request Headers
}


payload = {
    "collectionId": "54ab5fb8e4b005bf100bdafb",
    "design": "list",
    "showPastOrUpcomingEvents": "upcoming",
    # Add other keys from the original POST payload if needed
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

print(data)
