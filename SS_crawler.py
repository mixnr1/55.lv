import os
import re
import time
import requests
from bs4 import BeautifulSoup
import smtplib, ssl
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options as FirefoxOptions

start = time.time()
start_tuple=time.localtime()
start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_tuple)
serijas_dic={'103.':'67',#Here you can specify the aparment series which interest you. The ones that doesn't interest you can be simply comment out. 
            '119.':'69',
            '602.':'71',
            'P. kara':'79',
            'Priv. m.':'77',
            #'104.':'68',
            #'467.':'70',
            #'Čehu pr.':'73',
            # 'Hrušč.':'76',
            #'LT proj.':'72',
            #'M. ģim.':'74',
            'Renov.':'3616',
            'Specpr.':'78',
            'Staļina':'75',
            'Jaun.':'3596'}
path=config.path
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options, executable_path=config.driver_path)
flat_list=open(path+'flats.txt', 'r')
hrefs = []
for elemt in flat_list:
    driver.get(elemt)
    min_cena=driver.find_element_by_id('f_o_8_min')
    max_cena=driver.find_element_by_id('f_o_8_max')
    min_cena.send_keys('30000')#Here you can set the starting price. If not needed comment out this line.
    max_cena.send_keys('75000')#Here you can set the max price. If not needed comment out this line.
    min_platiba=driver.find_element_by_id('f_o_3_min')
    max_platiba=driver.find_element_by_id('f_o_3_max')
    min_platiba.send_keys('50')#Here you can set min area in square meters. If not needed comment out this line.
    max_platiba.send_keys('90')#Here you can set max area in square meters. If not needed comment out this line.
    select_min_istabas=Select(driver.find_element_by_name('topt[1][min]'))
    select_min_istabas.select_by_index(3)#Here you can set min number of the rooms. If not needed comment out this line.
    select_max_istabas=Select(driver.find_element_by_name('topt[1][max]'))
    select_max_istabas.select_by_index(4)##Here you can set min number of the rooms. If not needed comment out this line.
    sakuma_stavs=driver.find_element_by_id('f_o_4_min')
    sakuma_stavs.send_keys('2')#Here you can set min number of the floor. If not needed comment out this line.
    time.sleep(1)
    try:
        ser=driver.find_element_by_xpath('//*[@id="f_o_6"]')
        ser_text=ser.text
        for key in serijas_dic.keys():
            if key in ser_text:
                driver.execute_script(f'document.getElementById("f_o_6").value = "{serijas_dic.get(key)}";') 
                myinput=driver.find_element_by_css_selector('input.s12')
                myinput.click()
                time.sleep(1)    
                all_links = driver.find_elements_by_xpath('//a[@href]')
                for elem in all_links:
                    e = elem.get_attribute('href')
                    hrefs.append(e)
            else:
                pass
    except NoSuchElementException:
        myinput=driver.find_element_by_css_selector('input.s12')
        myinput.click()
        time.sleep(1)    
        all_links = driver.find_elements_by_xpath('//a[@href]')
        for elem in all_links:
            e = elem.get_attribute('href')
            hrefs.append(e)
test=[elem for elem in list(set(hrefs)) if re.findall('http[s]?://www.ss.com/msg/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', elem)]
file_text=open(path+"SS_flats_unique.txt", 'r').read().split('\n')
diff=[line for line in test if line not in file_text]
if len(diff) > 0:
    os.remove(path+"SS_flats_unique.txt")
    file_text=open(path+"SS_flats_unique.txt",'w')
    for elem in sorted(test):
        file_text.write(elem + '\n')
    file_text.close()
driver.close()
flat_list.close()

while True:
    if len(diff)==0:
        break
    if len(diff)>0:
        HTML_text=[]
        for elemt in diff:
            page = requests.get(elemt)
            soup = BeautifulSoup(page.content, 'html.parser')
            city=soup.find(id="tdo_20").get_text() 
            disctrict=soup.find(id="tdo_856").get_text() 
            street=soup.find(id="tdo_11").get_text() 
            rooms=soup.find(id="tdo_1").get_text() 
            area=soup.find(id="tdo_3").get_text() 
            floor=soup.find(id="tdo_4").get_text() 
            series=soup.find(id="tdo_6").get_text() 
            price=soup.find(id="tdo_8").get_text() 
            HTML_text.append(str('<tr><td><a href="'+elemt+'">'+city+', '+disctrict+', '+street.replace("[Karte]", "")+'</a></td><td>'+rooms+'</td><td>'+area+'</td><td>'+floor+'</td><td>'+series+'</td><td>'+price+'</td></tr>'))
        sender_email = config.sender_email
        receiver_email = config.receiver_email
        password = config.password
        message = MIMEMultipart("alternative")
        timestr = time.strftime("%d.%m.%Y-%H:%M:%S")
        message["Subject"] = "SLUDINĀJUMI "+timestr 
        message["From"] = sender_email
        message["To"] = receiver_email
        epasta_saturs="\n".join([(str(i).replace('\n', '')) for i in diff])
        plain=f"""{epasta_saturs}"""
        html = f"""\
        <html>
        <body>
            <table border='1' style='border-collapse:collapse'>
                <tr>
                    <th>Street</th>
                    <th>Rooms</th>
                    <th>Area</th>
                    <th>Floor</th>
                    <th>Series</th>
                    <th>Price</th>
                </tr>
                {" ".join(str(x) for x in HTML_text)}
            </table>
        </body>
        </html>
        """
        part1 = MIMEText(plain, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        break

end = time.time()
end_tuple = time.localtime()
end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_tuple)
print("Script ended: "+end_time)
print("Script running time: "+time.strftime('%H:%M:%S', time.gmtime(end - start)))