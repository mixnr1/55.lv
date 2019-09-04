import time
import requests
from lxml import html
import config
start = time.time()
start_tuple=time.localtime()
start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_tuple)
# darijumu_veids={'Izīrē':'hand_over/',
#                 'Īrē':'remove/',
#                 'Maina':'change/',
#                 'Dažādi':'other/'}
path=config.path
flat_list=open(path+'flats.txt', 'r')
     
def parser(elemt):
        regions=elemt[:elemt.find("/sell/")].replace('https://www.ss.com/lv/real-estate/flats/','')
        all_lines=[]
        page = requests.get(elemt, proxies=config.proxies, allow_redirects=False)
        soup=html.fromstring(page.content)
        tr_elements = soup.xpath('//tr')
        for T in tr_elements:
                if len(T)==10:#izpildas ja kolonnu skais tabula ir precizi desmit
                        line=[(regions)]#sakam ar regionu
                        for j in T.iterchildren():
                                data=j.text_content()
                                if len(data)>0:
                                        try:
                                                line.append(data)
                                        except:
                                                pass
                        all_lines.append(line)
        file_text=open(path+"test.txt",'a')
        # test=[]
        for ele in all_lines:
                st=[]
                for i in range(0, len(ele)):#no nulles nesakam lai izlaistu pirmo kolonnu
                        if i==1:
                                pass
                        else:
                                st.append(ele[i])
                line=','.join(st)
                file_text.write(line + '\n')
                # test.append(line)
        # print(test)
        file_text.close()
for elemt in flat_list:
        parser(elemt) 
        for i in range(2, 30):
                page=''.join([elemt.rstrip(), 'page', str(i), '.html'])                            
                response = requests.get(page, proxies=config.proxies, allow_redirects=False)#What to do if doesn't exist
                if response.status_code == 200:
                        parser(page)
                elif response.status_code == 302:
                        pass
                elif response.status_code == 404:
                        pass
end = time.time()
end_tuple = time.localtime()
end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_tuple)
print("Script ended: "+end_time)
print("Script running time: "+time.strftime('%H:%M:%S', time.gmtime(end - start)))

