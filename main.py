from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

import requests
from PIL import Image
from io import StringIO

import time

import urllib.parse as uri
from PyPDF2 import PdfMerger

"""import os

print(os.getcwd())

os.environ['path'] += f";{os.getcwd()}"
from cairosvg import svg2pdf"""

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM


class MusecoreWebsite():
    def __init__(self) -> None:
        #self.driver = webdriver.Firefox(executable_path="geckodriver.exe")
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get('chrome://settings/')
        self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.5);')
        self.driver.implicitly_wait(3)

        self.tempDir = ""

        self.currentScoreUrl = ""

    def login(self, user:str, pwd:str):
        self.driver.get(r"https://musescore.com/user/login?destination=%2Fcas%2Flogin")
        
        if user != "":
            element = self.driver.find_element(by=By.ID, value="username")
            element.send_keys(user)

            element = self.driver.find_element(by=By.ID, value="password")
            element.send_keys(pwd + Keys.ENTER)
        else:
            input("Please login manually in MuseScore, then press ENTER")
        

    def getScoreSheets(self, scoreUrl:str) -> list:
        self.currentScoreUrl = scoreUrl
        
        self.driver.get(scoreUrl)
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, value=".css-47sehv").click()
        
        urlList = []

        for i in range(1, 10):
            urlList += self.scrapHtml(i)

            self.driver.find_element(by=By.ID, value="jmuse-scroller-component").send_keys(Keys.PAGE_DOWN)
            time.sleep(3)

        #remove duplicates in list
        urlList = list(dict.fromkeys(urlList))

        for url in urlList:
            self.driver.get(url)

        return urlList
        

    def scrapHtml(self, nextPage:int) -> list:
        html = self.driver.find_element(by=By.XPATH, value="//body").get_attribute('outerHTML')
        
        #self.driver.execute_script("argument[0].style.visibility='hidden';", htmlBody)
        

        #self.driver.execute_script("arguments[0].outerHTML = arguments[1]", htmlBody, "SUPER BODY")

        urlList = []
        iFile = 0

        tagBuffer = ""
        for iLetter, letter in enumerate(html):
            if letter == ">":
                if "class=\"KfFlO\"" in tagBuffer.split(" "): 
                    
                    iFile += 1

                    """newHtml = html[:iLetter] + f" id=\"CUSTOM_SELECTOR_{iFile}\" " + html[iLetter:]
                    self.driver.execute_script("arguments[0].outerHTML = arguments[1]", htmlBody, newHtml)"""

                    url = tagBuffer[tagBuffer.index("src=") + 5:]
                    url = url[:url.index("\"")]
                    
                    alt = tagBuffer[tagBuffer.index("alt=") + 5:]
                    alt = alt[:alt.index("\"")]

                    elements = self.driver.find_elements(by=By.XPATH, value=f"//*[@id=\"jmuse-scroller-component\"]/div[{nextPage}]/img")
                    
                    if len(elements) > 0:
                        #elements[0].screenshot(f"{iFile}.png")
                        
                        with open("test.png", "wb+") as file:
                            file.write(elements[0].screenshot_as_png)

                    return ""
                    element = self.driver.find_element(by=By.ID, value=f"CUSTOM_SELECTOR_{iFile}")
                    element.screenshot(f"{iFile}.png")

                    if False:
                        with open(f"{iFile}.svg", "wb+") as file:
                            response = requests.get(url)
                            file.write(response.content)

                    urlList.append(url)

                tagBuffer = ""
            elif letter != "<":
                tagBuffer += letter

        return urlList


    def convertSheets(self, sheets:list) -> str:
        #files = [self.convertSheetToPdf(i, sh) for i, sh in sheets]
        merger = PdfMerger()

        for i, sheet in sheets:
            merger.append(self.convertSheetToPdf(i, sheet))
        
        score = merger.write(uri.urljoin(self.tempDir, f"/MusescoreSheet_merged.pdf"))
        merger.close()

        return score

    def convertSheetToPdf(self, sheetId:int, sheetFilePath:str) -> str:
        #return svg2pdf(bytestring=sheet, write_to=uri.urljoin(self.tempDir, f"/musescoreSheet_{sheetId}.pdf"))
        drawing = svg2rlg(sheetFilePath)
        filePath = uri.urljoin(self.tempDir, f"/MusescoreSheet_{sheetId}.pdf")
        renderPDF.drawToFile(drawing, filePath)
        return filePath



website = MusecoreWebsite()
#website.login("", "")
l = website.getScoreSheets("https://musescore.com/user/36103678/scores/8337884")

print("Score sheets urls:")
for e in l:
    print(e + "\n")

#C:\Users\robidela\AppData\Local\Programs\GIMP 2