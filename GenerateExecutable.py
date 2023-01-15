import PyInstaller.__main__

PyInstaller.__main__.run([
    'MuseScoreDownloader.py',
    '--onefile',
    #'--windowed',
    '-i=executable_logo.ico'
])