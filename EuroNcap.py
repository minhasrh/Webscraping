#Download Euro NCAP rating PDF files 

# import HTMLSession from requests_html
import tkinter
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

url_base = "https://www.euroncap.com"
url_safety_rating = url_base + "/en/ratings-rewards/latest-safety-ratings"

# create an HTML Session object
print('Initiating Data extract session..')
session = HTMLSession()
# Use the object above to connect to needed webpage
resp = session.get(url_safety_rating)
# Run JavaScript code on webpage
resp.html.render(timeout=30)

soup = BeautifulSoup(resp.html.html, "lxml")
div_tags = soup.findAll('div', attrs={'class' : 'rating-table-row-c c9'})

print(str(len(div_tags))+' Models identified ...')
 
#logfile = open('log_file.txt','w') 
#logfile.write('Rating table extract initiated ') 
#logfile.write('------------------------------\n') 
#logfile.write('\n') 
#logfile.write(str(len(div_tags)) + ' Models identified .\n\n') 
#logfile.close()

counter = 0 

try:
        print('Preparing download templates...')
        for div in  div_tags:
            url_car = url_base + div.find('a')['href']
            #print(url_car)
            resp2 = session.get(url_car)
            resp2.html.render(timeout=35)
            soup2 = BeautifulSoup(resp2.html.html, "lxml")
            download_div_tags = soup2.findAll('div', attrs={'class' : 'download-report'})
            
            for div2 in  download_div_tags:
                url_report = div2.find('a')['href']
                
                counter = counter + 1
                #if counter>32:
                url_split_list=url_report.split('/')
                filename_pos=len(url_split_list)-1
                
                filename = url_split_list[filename_pos] 
                b="Downloading ....\n" + filename 
                #print("Downloading .... " , url_car, " " , url_report, " as ", filename)
                #logfile = open('log_file.txt','a')
                #logfile.write(b)
                #logfile.write('\n')
                #logfile.close()
                # Get response object for link 
                response = requests.get(url_report) 
                # Write content in pdf file 
                pdf = open(filename, 'wb') 
                pdf.write(response.content) 
                pdf.close() 
                #print(filename, " downloaded") 
                print(b)
        print(str(counter) +' Files Downloaded successfully .')
except Exception as e:
 print('Error while downloading pdf') 
 logfile=open('log_file.txt','w')
 logfile.write('Error while downloading pdf \n'+str(e))
 logfile.close() 