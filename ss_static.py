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
all_lines=[]
for elemt in flat_list:
        if len(str(elemt).replace('https://www.ss.com/lv/real-estate/flats/','').split("/")[1].replace('hand_over', ''))>0:
                regions=str(elemt).replace('https://www.ss.com/lv/real-estate/flats/','').split("/")[0]+":"+str(elemt).replace('https://www.ss.com/lv/real-estate/flats/','').split("/")[1].replace('hand_over', '')
        else:
                regions=str(elemt).replace('https://www.ss.com/lv/real-estate/flats/','').split("/")[0]
        page = requests.get(elemt)
        soup=html.fromstring(page.content)
        tr_elements = soup.xpath('//tr')
        # i=0
        # for T in tr_elements:
        #         i+=1
        #         print(i, T.text_content())
        # i=0
        # for T in tr_elements:
        #         i+=1
        #         print(i, len(T))
        
        # i=0
        # for T in tr_elements:
        #         i+=1
        #         if len(T)==10:
        #                 print(i, T.text_content())
       
        # i=0
        # for T in tr_elements:
        #         i+=1
        #         if len(T)==10:
        #                 for j in T.iterchildren():
        #                         data=j.text_content()
        #                         print(i, data)
                
        # i=0
        # for T in tr_elements:
        #         i+=1
        #         if len(T)==10:
                        
        #                 for j in T.iterchildren():
        #                         data=j.text_content()
        #                         if len(data)>0:
        #                                 try:
        #                                         print(i, data)
        #                                 except:
        #                                         pass
                      
        # i=0     
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
file_text=open(path+"test.txt",'w')
for ele in all_lines:
        st=[]
        for i in range(0, len(ele)):#no nulles nesakam lai izlaistu pirmo kolonnu
                if i==1:
                        pass
                else:
                        st.append(ele[i])
        line=','.join(st)
        file_text.write(line + '\n')
file_text.close()
end = time.time()
end_tuple = time.localtime()
end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_tuple)
print("Script ended: "+end_time)
print("Script running time: "+time.strftime('%H:%M:%S', time.gmtime(end - start)))