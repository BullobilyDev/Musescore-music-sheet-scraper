from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.edge.options import Options as EdgeOptions

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import time
from PyPDF2 import PdfMerger

import os
from enum import Enum

import requests

from svglib.svglib import svg2rlg
import img2pdf

from reportlab.graphics import renderPDF

from pathvalidate import sanitize_filename

class BrowserList(Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"
    EDGE_DO_NOT_USE = "edge"

class MusecoreWebsite():
    def __init__(self, scoreUrl:str, browser:BrowserList):
        if browser == BrowserList.FIREFOX:
            profile = FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", os.getcwd())
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

            self.driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()), firefox_profile=profile)

        elif browser == BrowserList.CHROME:
            options = ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option("prefs", {
            "download.default_directory": os.getcwd()
            })

            self.driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), options=options)

        elif browser == BrowserList.EDGE_DO_NOT_USE:
            options = EdgeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option("prefs", {
            "download.default_directory": os.getcwd()
            })

            self.driver = webdriver.Edge(service=EdgeService(executable_path=EdgeChromiumDriverManager().install()), options=options)


        self.driver.maximize_window()
        self.driver.implicitly_wait(3)
        
        """self.driver.get('chrome://settings/')
        self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.5);')"""
        
        
        self.driver.get(scoreUrl)

        #skip cookies popup
        time.sleep(3)
        try:
            self.driver.find_element(By.CSS_SELECTOR, value=".css-47sehv").click()
        except:
            pass

        self.scoreName = sanitize_filename(self.driver.title)[:200]
        self.scorePagesUrls = []

    def login(self, user:str, pwd:str):
        self.driver.get(r"https://musescore.com/user/login?destination=%2Fcas%2Flogin")
        
        if user != "":
            element = self.driver.find_element(by=By.ID, value="username")
            element.send_keys(user)

            element = self.driver.find_element(by=By.ID, value="password")
            element.send_keys(pwd + Keys.ENTER)
        else:
            input("Please login manually in MuseScore, then press ENTER")
        

    def scrapScoreSheets(self) -> list:
        scrollLength = 400
        scrollCount = 0

        uselessIterationsCount = 0
        while uselessIterationsCount < 5:
            urlsCount = len(self.scorePagesUrls)

            scrapOk = self.scrapCurrentPage()
            
            time.sleep(2)
            
            if scrapOk:
                self.driver.execute_script(f"document.getElementById(\"jmuse-scroller-component\").scrollBy(0, {scrollLength});")
                scrollCount += 1

                uselessIterationsCount = 0 if len(self.scorePagesUrls) > urlsCount else uselessIterationsCount + 1
            else:
                for i in range(0, min(3, scrollCount)):
                    self.driver.execute_script(f"document.getElementById(\"jmuse-scroller-component\").scrollBy(0, {- scrollLength});")
                    time.sleep(1 / (scrollCount * 2))
                    self.driver.execute_script(f"document.getElementById(\"jmuse-scroller-component\").scrollBy(0, {scrollLength});")
                    time.sleep(1 / (scrollCount * 2))
        

    def scrapCurrentPage(self) -> bool:
        """Scrap the current display of the page

        Returns:
            bool: True if everything was OK, False if a new iteration should be done
        """
        html = self.driver.find_element(by=By.XPATH, value="//body").get_attribute('outerHTML')
        
        #self.driver.execute_script("argument[0].style.visibility='hidden';", htmlBody)
        #self.driver.execute_script("arguments[0].outerHTML = arguments[1]", htmlBody, "SUPER BODY")

        tagBuffer = ""
        for letter in html:
            if letter == ">":
                if "class=\"KfFlO\"" in tagBuffer.split(" "): 
                    
                    if not "src=" in tagBuffer:
                        return False

                    url = tagBuffer[tagBuffer.index("src=") + 5:]
                    url = url[:url.index("\"")]
                    url = url.replace("amp;", "")
                    
                    alt = tagBuffer[tagBuffer.index("alt=") + 5:]
                    alt = alt[:alt.index("\"")]

                    #elements = self.driver.find_elements(by=By.XPATH, value=f"//*[@id=\"jmuse-scroller-component\"]/div[{nextPage}]/img")
                    if not url in self.scorePagesUrls:
                        currentHandle = self.driver.current_window_handle

                        #open score page url in new tab
                        #time.sleep(5)

                        #save page as picture if from musescore website
                        if url.startswith("https://musescore.com"):
                            with open("score_0.svg", "wb+") as f:
                                img = requests.get(url).content
                                #shutil.copyfileobj(res.raw, f)
                                #f.write(self.driver.page_source)
                                f.write(img)
                                f.close()
                        else:
                            self.driver.execute_script(f"window.open('{url}')")
                            #self.driver.switch_to.window(self.driver.window_handles[-1])
                            self.driver.switch_to.window(currentHandle)
                        
                        #close the newly opened tab (if there is one)
                        """if len(self.driver.window_handles) > 1:
                            self.driver.close()"""
                        
                        #add the url to the already scrapped url list
                        self.scorePagesUrls.append(url)

                tagBuffer = ""
            elif letter != "<":
                tagBuffer += letter
            
        return True


    def convertScoretSheets(self) -> str:
        merger = PdfMerger()

        #only for debug
        files = []

        for file in os.listdir(os.getcwd()):
            if file.startswith("score_"):
                files.append(file)

                merger.append(self.convertSheetToPdf(file))
        
        targetPath = os.path.join(os.getcwd(), f"{self.scoreName}.pdf")
        merger.write(targetPath)
        merger.close()

        return targetPath

    def convertSheetToPdf(self, sheetFilePath:str) -> str:

        sheetFile = sheetFilePath.split("\\")[-1].split("/")[-1]
        sheetName = sheetFilePath.split(".")[0]
        sheetExtension = sheetFilePath.split(".")[1]

        newSheetFilePath = os.path.join(os.getcwd(), f"{sheetName}.pdf")

        if sheetExtension == "svg":
            drawing = svg2rlg(sheetFilePath)
            renderPDF.drawToFile(drawing, newSheetFilePath)
            
        elif sheetExtension == "png":
            pdf_bytes = img2pdf.convert(sheetFilePath)
            with open(newSheetFilePath, "wb+") as f:
                f.write(pdf_bytes)
                f.close()

        return newSheetFilePath


    def clearScoreSheets(self):
        for file in os.listdir(os.getcwd()):
            if file.startswith("score_"):
                os.remove(file)

        self.driver.close()

