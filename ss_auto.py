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
def write_to_file(the_list):
    with open(config.file_path+'unique.txt', 'w') as f:
        for elem in the_list: 
            f.write(str(elem[0]) + '\n')
    f.close()

year=int(time.strftime("%Y"))
start = time.time()
start_tuple=time.localtime()
start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_tuple)

path=config.file_path
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options, executable_path=config.driver_path)
# driver = webdriver.Firefox(executable_path=config.driver_path)
driver.get(config.url)
min_cena=driver.find_element_by_id("f_o_8_min")
max_cena=driver.find_element_by_id("f_o_8_max")
min_cena.send_keys("6000")
max_cena.send_keys("12000")
select_min_year=Select(driver.find_element_by_name('topt[18][min]'))
select_min_year.select_by_value("2013")
select_max_year=Select(driver.find_element_by_name('topt[18][max]'))
select_max_year.select_by_value("2019")
select_min_tilp=Select(driver.find_element_by_name('topt[15][min]'))
select_min_tilp.select_by_value("1.6")
select_max_tilp=Select(driver.find_element_by_name('topt[15][max]'))
select_max_tilp.select_by_value("2.0")
select_dzinejs=Select(driver.find_element_by_name('opt[34]'))
select_dzinejs.select_by_value("494")#Dīzelis
select_atr_karba=Select(driver.find_element_by_name('opt[35]'))
# select_atr_karba.select_by_value("497")#Automāts
# select_atr_karba.select_by_value("496")#Manuāla
select_virs_tips=Select(driver.find_element_by_name('opt[32]'))
select_virs_tips.select_by_value("483")#Universālis
time.sleep(2)
myinput=driver.find_element_by_css_selector('input.s12')
myinput.click()
time.sleep(2)
table = driver.find_element_by_xpath('/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/form/table[2]/tbody')
table_rows = table.find_elements_by_tag_name("tr")
the_list=[]
for row in table_rows:
    cells = row.find_elements_by_tag_name("td")
    if len(cells) == 7:      
        sludinajuma_teksts = str(cells[2].text)
        sludinajuma_teksta_links = cells[2].find_element_by_tag_name("a").get_attribute("href")
        gads = (cells[3].text)
        tilpums = str(cells[4].text)
        nobraukums = str(cells[5].text)
        cena = str(cells[6].text)
        gada_nobraukums = nobraukums.strip('tūkst.').replace(" ", "")
        if gada_nobraukums == "-":
            videjais_gada_nobraukums = "-"
            the_list.append([sludinajuma_teksta_links, sludinajuma_teksts,  gads, tilpums, gada_nobraukums, videjais_gada_nobraukums, cena])
        else:
            videjais_gada_nobraukums = (int(gada_nobraukums)*1000)/(int(year)-int(gads))
            the_list.append([sludinajuma_teksta_links, sludinajuma_teksts,  gads, tilpums, gada_nobraukums, round(videjais_gada_nobraukums, 2), cena])
driver.close()
test = [i[0] for i in the_list]
file_text=open(config.file_path+'unique.txt', 'r').read().split('\n')
diff=[line for line in test if line not in file_text]
while True:
    if len(diff) == 0:
        break
    if len(diff) > 0:
        os.remove(config.file_path+"unique.txt")
        write_to_file(the_list)
        HTML_text = []
        for i in range(0, len(diff)):
            for n in range(0, len(the_list)):
                if the_list[n][0] == diff[i]:
                    HTML_text.append(str("<tr><td><a href='"+the_list[n][0]+"'>"+the_list[n][1]+"</a></td><td>"+the_list[n][2]+"</td><td>"+the_list[n][3]+"</td><td>"+the_list[n][4]+"</td><td>"+str(the_list[n][5])+"</td><td>"+str(the_list[n][6])+"</td></tr>"))
        sender_email = config.sender_email
        receiver_email = config.receiver_email
        password = config.password
        message = MIMEMultipart("alternative")
        timestr = time.strftime("%d.%m.%Y-%H:%M:%S")
        message["Subject"] = "SS "+timestr 
        message["From"] = sender_email
        message["To"] = receiver_email
        epasta_saturs="\n".join([(str(i).replace('\n', '')) for i in diff])
        plain=f"""{epasta_saturs}"""
        html = f"""\
        <html>
        <body>
            <table border='1' style='border-collapse:collapse'>
                <tr>
                    <th>Nosaukums</th>
                    <th>Gads</th>
                    <th>Motors</th>
                    <th>km (tūkst.)</th>
                    <th>Vid.gada nobraukums</th>
                    <th>Cena</th>
                </tr>
                {" ".join(str(x) for x in HTML_text)}
            </table>
        </body>
        </html>
        """
        # print(html)
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