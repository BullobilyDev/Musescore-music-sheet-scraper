from MusecoreWebsite import BrowserList, MusecoreWebsite


website = MusecoreWebsite("https://musescore.com/user/36103678/scores/8337884", BrowserList.CHROME)
website.scrapScoreSheets()
website.convertScoretSheets()
website.clearScoreSheets()

print("Score extracted successfully")