# Ninitelike

Open source ninite like for Windows

## Software Available

* CCleaner
* 7zip
* notepadplusplus
* adwcleaner
* malwarebytes
* avast
* bitdefender
* glasswire
* bleachbit
* windirstat
* autoruns

## Using Ninitelike

### Release

You can download last release [here](https://github.com/Parcothsai/ninitelike/releases).

### Build

```
/git clone https://github.com/Parcothsai/ninitelike.git
cd ninitelike
& venv/Scripts/Activate.ps1
pip3 install -r requirements.txt
pyinstaller --onefile --name NiniteLike .\ninitelike.py
```

Go to dist folder and execute in admin the file "NiniteLike.exe" and voila 👍
