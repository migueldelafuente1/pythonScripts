'''
Created on 9 abr. 2020

@author: Miguel
'''

from bs4 import BeautifulSoup
import requests
import lxml
import csv

#===============================================================================
#      IMPORTING WEBSITE AS TEXT
#===============================================================================
# with open('webSite.html') as html_file:
#     soup = BeautifulSoup(html_file, "html5lib") #'lxml'
# 
# #print(soup.prettify())
# 
# ## print a tag and a tag text
# print(soup.title)
# print(soup.title.text)
# 
# ## find elements
# ## find a tag'div' with class='footer'
# match = soup.find('div', class_='footer')
# print(match)
# match = soup.find('div', class_='article')
# print(type(match))
# print(match.h2.a.text)
# 
# ## Iterate over all articles
# for article in soup.find_all('div', class_='article'):
#     print(' >', article.h2.a.text)
#     print('  ', article.p.text)
#
#===============================================================================
#     IMPORTING A WEB BY REQUESTING THE SITE
#===============================================================================

source = requests.get('http://coreyms.com').text
soup = BeautifulSoup(source, "html5lib")
#print(soup.prettify())

article = soup.find('article')
# print(article.prettify())

## find the link of the youtube video
video_src = article.find('iframe', class_='youtube-player')['src']
print(video_src)
video_id = video_src.split('/')[4]
video_id = video_id.split('?')[0]

print("https://youtube.com/watch?v={}".format(video_id))


csv_file = open('cms_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary', 'video_link'])

for article in soup.find_all('article'):
    headline = article.h2.a.text
    print(headline)

    summary = article.find('div', class_='entry-content').p.text
    print(summary)

    try:
        vid_src = article.find('iframe', class_='youtube-player')['src']

        vid_id = vid_src.split('/')[4]
        vid_id = vid_id.split('?')[0]

        yt_link = f'https://youtube.com/watch?v={vid_id}'
    except Exception as e:
        yt_link = None

    print(yt_link)

    print()

    csv_writer.writerow([headline, summary, yt_link])

csv_file.close()