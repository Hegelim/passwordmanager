# passwordmanager
An app built in Python that helps you manage passwords easily


## Development In WSL2

First, start `VcxSrv`, then Use the following code to set the display device correctly if you are using WSL2
```
export DISPLAY=$(route.exe print | grep 0.0.0.0 | head -1 | awk '{print $4}'):0.0
python welcomescreen.py
```

