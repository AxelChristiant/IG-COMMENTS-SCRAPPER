#
# browser.close()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

allUrl = []
with open('all-url.txt') as f:
    allUrl = f.readlines()
f.close()


chrome_options=Options()

chrome_options.add_argument('--lang=en')
browser = webdriver.Chrome('./env/chromedriver.exe')

browser.get("https://www.instagram.com/accounts/login/")
sleep(1)

browser.find_element_by_name("username").send_keys("") #Isi username ig anda
browser.find_element_by_name("password").send_keys("") #Isi password ig anda

sleep(2)

buttons = browser.find_elements_by_tag_name('button')
buttons[1].click()
sleep(5)
print("JUMLAH : "+ str(len(allUrl)))


for i in range(0,len(allUrl)):
    browser.get(allUrl[i])
    sleep(3)
    try:
        cBody  = browser.find_element_by_class_name("cv3IO")
        load_more_comment = browser.find_elements_by_class_name("wpO6b")
        # load_more_comment = browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button/div/svg")
        j = 0
        while j < 15:
            sleep(3)
            for x in range(5):
                browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', cBody)
            load_more_comment[-3].click()
            load_more_comment = browser.find_elements_by_class_name("wpO6b")
            print("Found {}".format(str(load_more_comment)))
            j += 1
    except Exception as e:
        print("Cant click load more : ",e)
        pass

    user_names = []
    user_comments = []
    comment = browser.find_elements_by_class_name('gElp9 ')
    for c in comment:
        content = c.text.split('\n')
        name = content[0]
        comment = content[1]
        user_names.append(name)
        user_comments.append(comment)

    
    user_names.pop(0)
    user_comments.pop(0)
    
    allData = pd.DataFrame()
    allData['usernames'] = user_names
    allData['comments'] = user_comments
    allData['label'] = 'Belum'
    print("NOMOR :" + str(i))
    allData.to_excel('data/data_'+str(i)+".xlsx",index=False,header=True)


browser.close()
