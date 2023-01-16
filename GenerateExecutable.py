import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    '--name=MuseScoreDownloader_script',
    '--icon=resources/executable_logo.ico',
    'MuseScoreDownloader.py'
])

#generate updated requirements.txt
#pipreqs --encoding utf-8 --force