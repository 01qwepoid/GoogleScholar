#https://scholar.google.co.in/citations?user=MNj1Dw4AAAAJ&hl=en&oi=ao&cstart=0&pagesize=140
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common import action_chains
import time
import bs4
import requests
import webbrowser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

url = 'https://scholar.google.co.in' #starting url
driver = webdriver.Chrome() #opens chrome
driver.get(url) #opens the url
driver.set_page_load_timeout(30) #if not loaded, closes after the given time
assert 'Google' in driver.title #check if right page is loaded
elem = driver.find_element_by_name('q') #find the search box
elem.clear() #cleaer the search box of old queries

##TODO## -------- make a list for all names 
text = 'Prashant Singh Rana' #test to be searches

elem.send_keys(text) #types in the nameFIELDNAME = models.SmallIntegerField()
elem.send_keys(Keys.RETURN) #hits enter
assert 'No results found.' not in driver.page_source #check if results are actually present

##TODO ------- make more general
res = requests.get('https://scholar.google.co.in/scholar?hl=en&as_sdt=0%2C5&q=prashant+singh+rana&btnG=') #url for rana sir's profile
res.raise_for_status() #check the availability
soup = bs4.BeautifulSoup(res.text,"html.parser") #apply bs4 to search results page

#verify for thapar univ
if 'Thapar' in soup.select('div[class="gs_nph"]')[0].getText():
	link = 'https://scholar.google.co.in' + soup.select('[class="gs_rt2"] a')[0].get('href') #profile page of prof

#get link for profile

print(soup.select('[class="gs_rt2"]')[0].getText())#exract name
#webbrowser.open(link)

newlink = link + "&cstart=0&pagesize=40" #display all entries
res = requests.get(newlink) #change res variable to new profile page
soup = bs4.BeautifulSoup(res.text,"html.parser") #apply bs4 to new profile page

driver.get(newlink) #open profile page of prof
entries = len(soup.select("tbody > tr[class='gsc_a_tr']"))
titles = []
for i in range(entries):
	print(i)
	print(soup.select('[class="gsc_a_at"]')[i].getText()) #gets name of  topics
	titles.append(soup.select('[class="gsc_a_at"]')[i].getText())

len(soup.select("td[class='gsc_a_t'] > div[class='gs_gray']")) #
collaborators = []
pubtype = []
for i in range(len(soup.select("td[class='gsc_a_t'] > div[class='gs_gray']"))):
    if i%2==0:
        collaborators.append(soup.select("td[class='gsc_a_t'] > div[class='gs_gray']")[i].getText())
    else:
        pubtype.append(soup.select("td[class='gsc_a_t'] > div[class='gs_gray']")[i].getText())


citedby = []
for i in range(len(soup.select("td[class='gsc_a_c'] > a"))):
    citedby.append(soup.select("td[class='gsc_a_c'] > a")[i].getText())

year = []
for i in range(len(soup.select("td[class='gsc_a_y'] > span"))):
    year.append(soup.select("td[class='gsc_a_y'] > span")[i].getText())

print('hey3')
teacher1 = list(zip(titles,collaborators,pubtype,citedby,year))
df = pd.DataFrame(data = teacher1, columns=['Title', 'Collaborators','Publication','Cited By','Year'])
df.to_csv('C:/Users/Shubham/Desktop/Python Automate/Scholar/tdata2.csv',index=False)

nowread = pd.read_csv('C:/Users/Shubham/Desktop/Python Automate/Scholar/tdata2.csv')
print(nowread.head())

#d = {'Title': {ttl}}.format(ttl=titles)#

#df = pd.DataFrame()



#but = driver.find_element(By.XPATH,'//span[text()="Show more"]')
#but.click()
#action = action_chains.ActionChains(driver)
#action.find_element_by_xpath("//span[@class='gs_lbl']")

#menu = driver.find_element_by_css_selector("")


#element = driver.find_element_by_id("gsc_bpf_more")






########## IMPORTANT CODE ... BUT IGNORE FOR NOW
#print(soup.select('input[name="xsrf"]')[0].get('value')) #value field of the post form - before show more

#element = driver.find_element_by_id('gsc_bpf_more')  #find the tag, for show more
#element.click() #click on the show more button

#print(soup.select('input[name="xsrf"]')[0].get('value')) #value field of the post form - after show more
##################################################





#actions = ActionChains(driver)
#actions.move_to_element(element).perform()



#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#driver.implicitly_wait(10)
#element = driver.find_element_by_id("gsc_bpf_more")
#element.click()
#driver.find_element_by_name(By.id("gsc_bpf_more")).click();

#button = driver.find_element_by_name("#gsc_bpf_more")
#button.click("gs_lbl")


#res = requests.get('https://www.google.com/search?q=' + 'apple')
#res.raise_for_status()

soup = bs4.BeautifulSoup(res.text)
linkelems = soup.select('.r a')

numopen = min(5, len(linkelems))
for i in range(numopen):
	webbrowser.open('https://www.google.com'+linkelems[i].get('href'))



start = time.clock()
while time.clock() - start < 10:
	continue

driver.close()