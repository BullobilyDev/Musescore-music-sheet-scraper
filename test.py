html = "<class=\"KfFlO\" 12><3456><789>"
newHtml = ""

iFile = 0

tagBuffer = ""
for iLetter, letter in enumerate(html):
    if letter == ">":
        if "class=\"KfFlO\"" in tagBuffer.split(" "): 
            
            iFile += 1

            newHtml = html[:iLetter] + f" CUSTOM_SELECTOR_{iFile} " + html[iLetter:]

        tagBuffer = ""
    elif letter != "<":
        tagBuffer += letter

print(newHtml)