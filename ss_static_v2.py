import csv
import time
import requests
from lxml import html
from lxml import etree
import config
start = time.time()
start_tuple=time.localtime()
start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_tuple)
darijumu_veids={'Izire':'hand_over/',
                'Ire':'remove/',
                'Pardod':'sell/',
                'Maina':'change/',
                'Dazadi':'other/'}
date = time.strftime('%d.%m.%Y.')
path=config.path
# flat_list=open(path+'flats.txt', 'r')
flat_list=open(path+'flats_updated_022022.txt', 'r')
def parser(elemt, tips):
        try:
                regions=elemt[:elemt.find("/"+tips)].replace('https://www.ss.com/lv/real-estate/flats/','')
                all_lines=[]
                # page = requests.get(elemt, proxies=config.proxies, allow_redirects=False)
                page = requests.get(elemt, allow_redirects=False)
                soup=html.fromstring(page.content)
                tr_elements = soup.xpath('//tr')
                for T in tr_elements:
                        if len(T)==10:
                                line=[(regions)]
                                for j in T.iterchildren():
                                        if j.find('a') is not None:
                                                line.append("https://www.ss.com"+(j.find('a').get('href')))
                                        data=j.text_content()
                                        if len(data)>0:
                                                try:
                                                        line.append(data)
                                                except:
                                                        pass
                                all_lines.append(line)
                for ele in all_lines:
                        st=[]
                        for i in range(0, len(ele)):
                                if i==2:
                                        pass
                                elif i==8 or i==9:
                                        st.append(ele[i].replace('€','').replace(',','').replace(' ',''))
                                else:
                                        st.append(ele[i])
                        line='|'.join(st)
                        with open('/home/mix/my_n3xcl0ud/Documents/ss_rent_static.csv', mode='a') as csv_file:#file name must be specified
                                csv_file.write(line+'|'+date)
                                csv_file.write('\n')
        except etree.ParserError as e:
                print(f"Parserr error: {e}")

for elemt in flat_list:
        site=''.join([elemt.rstrip(), darijumu_veids['Izire']])#section must be specified
        parser(site, darijumu_veids['Izire']) #section must be specified
        for i in range(2, 30):
                page=''.join([site, 'page', str(i), '.html'])     
                response = requests.get(page, allow_redirects=False)                    
                # response = requests.get(page, proxies=config.proxies, allow_redirects=False)
                if response.status_code == 200:
                        parser(page, darijumu_veids['Izire']) #section must be specified
                elif response.status_code == 302:
                        pass
                elif response.status_code == 404:
                        pass
end = time.time()
end_tuple = time.localtime()
end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_tuple)
print("Script ended: "+end_time)
print("Script running time: "+time.strftime('%H:%M:%S', time.gmtime(end - start)))

