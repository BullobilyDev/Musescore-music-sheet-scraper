from MusecoreWebsite import BrowserList, MusecoreWebsite

print("""
███╗   ███╗██╗   ██╗███████╗███████╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗         
████╗ ████║██║   ██║██╔════╝██╔════╝██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝         
██╔████╔██║██║   ██║███████╗█████╗  ███████╗██║     ██║   ██║██████╔╝█████╗           
██║╚██╔╝██║██║   ██║╚════██║██╔══╝  ╚════██║██║     ██║   ██║██╔══██╗██╔══╝           
██║ ╚═╝ ██║╚██████╔╝███████║███████╗███████║╚██████╗╚██████╔╝██║  ██║███████╗         
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝         
                                                                                      
██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝                                                                         
                                                                                      """)

browser = None
scoreUrl = ""

while browser == None:
    userInput = input(
"""\nWhich browser should be used to scrap the music score?
Can be:
f for Firefox,
c for Chrome.
Your choice: """)

    if userInput == "f":
        browser = BrowserList.FIREFOX
    elif userInput == "c":
        browser = BrowserList.FIREFOX
    else:
        print("\nInvalid choice, please retry.")


while scoreUrl == "":
    userInput = input("\nCopy paste the music score link: ")

    if userInput.startswith("https://musescore.com"):
        scoreUrl = userInput
    else:
        print("\nInvalid choice, the link should start with 'https://musescore.com', please retry.")

print("""
\nMusic score scrapping is in progress. It may take a few minutes.
To avoid weird bugs, please set and keep focus on script browser window.
Please don't interract with the script browser window!\n""")

#website = MusecoreWebsite("https://musescore.com/user/36103678/scores/8337884", BrowserList.FIREFOX)
website = MusecoreWebsite(scoreUrl=scoreUrl, browser=browser)
website.scrapScoreSheets()
musicScorePath = website.convertScoretSheets()
website.clearScoreSheets()

input(f"\nScore successfully downloaded. Download location:\n{musicScorePath}.")
exit()
#pyinstaller -F -w -icon="executable_logo.ico" main.py