import os
import config
import urllib.request
from html.parser import HTMLParser
from urllib.request import urlopen

clear = lambda: os.system('cls')

VidIDs = []


class HTMLP(HTMLParser):
    # Globals
    cl = "item-section"
    channel = "yt-lockup-channel"
    olTag = "ol"
    divTag = "div"
    findVidEnd = False
    srch = False
    n = 1


    # Definitions
    def handle_starttag(self, tag, attrs):
        #if any("guide-main-title" in s for s in attrs):
        #print("Found tag:", end=" ")
        #print(tag)
        #print("Found attrs:", end=" ")
        #print(attrs)
        if tag == self.olTag and any(self.cl in s for s in attrs):
            self.srch = True
            #print("Searching for video")

        if self.n > 0:
            if self.srch:
                #print(attrs)
                if any(self.channel in s for s in attrs):
                    pass
                else:
                    #print("This isn't a channel!")
                    if tag == self.divTag:
                        #VidIDs.append(attrs["data-context-item-id"])
                        #print("Video found:", end=" ")
                        #print(attrs)
                        for s in attrs:
                            if "data-context-item-id" in s:
                                VidIDs.append(s[1])                                
                        self.n -= 1
        else:
            self.srch = False
            #self.close()

    #def handle_endtag(self, tag):



file = "links.txt"
worker = open(file, "r")
songs = {}


def search(s):
    print("Searching: " + s)
    s = s.replace(" ", "%20")
    #print(s)
    site = "http://www.youtube.com/results?search_query=" + s
    connection = urllib.request.Request(site, headers=config.hdr)
    parser = HTMLP()
    html = ""

    for word in urlopen(connection).readlines():
       html += word.strip().decode('utf-8')

    parser.feed(html)



for line in worker:
    songs[line[0:len(line) - 1]] = ""

i = 1
for s in songs:
    search(s)
    #clear()
    print(str(i) + "/" + str(len(songs)))
    i += 1

print("Finished")

text_file = open("converted.txt", "w")
for x in range(0, len(VidIDs)):
    VidIDs[x] = "https://www.youtube.com/watch?v=" + VidIDs[x]
    text_file.write(VidIDs[x] + "\n")
print("File: converted.txt")
