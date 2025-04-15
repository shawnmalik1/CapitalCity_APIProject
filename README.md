# CapitalCity_APIProject
# DS2002 Assignment
# Name: Shawn Malik

This is a simple API that returns the local time and UTC offset for a given capital city.

IP Address of working API: http://34.85.138.229:5001/ (will show Unauthorized if typing it into your browser as the TOKEN is not correct)


# Documentation of how to call the API

After SSHing into your GCP VM, you can run the following command to start the API:
```python3 app.py```

From there, you can use the following command to call the API:
curl -H "Authorization: Bearer TOKEN" http://34.85.138.229:5001/api/time?city=CapitalName

Example Command:
curl -H "Authorization: Bearer supersecrettoken123" http://34.85.138.229:5001/api/time?city=London

Output:
![Screenshot 2025-04-15 at 7.11.34 PM.png](..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fsc%2F4x1k3r3n61d13_20pq4s_18m0000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_Gaeyd1%2FScreenshot%202025-04-15%20at%207.11.34%E2%80%AFPM.png)

