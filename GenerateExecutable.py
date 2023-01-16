import PyInstaller.__main__

PyInstaller.__main__.run([
    'MuseScoreDownloader.py',
    '--onefile',
    #'--windowed',
    '-i=executable_logo.ico'
])

#generate updated requirements.txt
#pipreqs --encoding utf-8 --force