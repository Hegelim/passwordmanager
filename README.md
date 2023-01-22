## passwordmanager
An app built in Python that helps you manage passwords easily


## Development In WSL2

First, start `VcxSrv`, then Use the following code to set the display device correctly if you are using WSL2
```
export DISPLAY=$(route.exe print | grep 0.0.0.0 | head -1 | awk '{print $4}'):0.0
python welcomescreen.py
```

## Development in Windows

```
python welcomescreen.py
```

## Export

Make sure you are in windows environment so that the execuatable file is .exe
```
pip install pyinstaller
pyinstaller --onedir --windowed welcomescreen.py
```

## Features

### V1.1.0

* Save entries
* Delete entries
* Export entries
* Backup with Google Drive
* Styled


