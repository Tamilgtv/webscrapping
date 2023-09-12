import requests
from bs4 import BeautifulSoup 
import pandas as pd
from datetime import datetime 
import psycopg2
import psycopg2.extras as extras

State=[]
office_links=[]
r=requests.get('https://www.era.com/real-estate-agents?companyId=reset')
soup=BeautifulSoup(r.content, 'html.parser')
for i in soup.findAll('li',{'class','areaListCol'}):
    State.append('https://www.era.com'+i.a.get('href'))
for i in State[:2]:
    r=requests.get(i)
    soup=BeautifulSoup(r.content, 'html.parser')
    for i in soup.findAll('div',{'class','l-grid__col l-grid__col-2-3'}):
        for x in i.findAll('a'):
            office_links.append('https://www.era.com'+x.get('href'))
            
            
agent_profile_url=[]
agent_name=[]
phone=[]
tag=[]
area_served=[]
rating=[]
office=[]
branch=[]
agent_facebook=[]
agent_Youtube=[] 
agent_Twitter=[] 
agent_Linkedin=[] 
agent_Instagram=[]
agent_Yelp=[]
state=[]
Zip=[]
address=[]
office_phone=[]
area_server=[]

for url in office_links:
    print(url)
    r=requests.get(url)
    soup=BeautifulSoup(r.content, 'html.parser')
    try:
        tag.append(soup.find('span',{'class':'ribbon__txt'}))
    except:
        tag.append('')
    try:
        agent_name.append(soup.find('h1',{'class':'heading-std heading-std--large mb-0'}).text)
    except:
        agent_name.append('')
    try:
        phone.append(soup.find('div',{'class':'agent-info-cont__agent-phone'}).text.strip())
    except:
        phone.append('')
    try:
        rating.append(soup.find('div',{'id':'star-ratings'}).span.text.strip())
    except:
        rating.append('')
    try:
        agent_profile_url.append(soup.find('div',{'class':'media__img media__img--agent-photo media__agent'}).img.get('src'))
    except:
        agent_profile_url.append('')
    try:
        area_served.append(soup.find('div',{'class':'l-two-col-right'}).text.replace('\n\n',''))
    except:
        area_served.append('')
    try:
        office.append(soup.find('div',{'class':'l-two-col-main'}).findAll('li')[1])
    except:
        office.append('')
    try:
        branch.append(soup.find('div',{'class':'l-two-col-main'}).findAll('li')[-1])
    except:
        branch.append('')
    
    F,Y,Ye,T,L,P,I=0,0,0,0,0,0,0
    try:
        for i in soup.find('ul',{'class':'hide-bullet social-list'}).findAll('li'):
            if 'Facebook' in i.a.get('aria-label'):
                agent_facebook.append(i.a.get('href'))
                F=1
            if 'Linkedin' in i.a.get('aria-label'):
                agent_Linkedin.append(i.a.get('href'))
                L=1
            if 'Yelp' in i.a.get('aria-label'):
                agent_Yelp.append(i.a.get('href'))
                Ye=1
            if 'Pinterest' in i.a.get('aria-label'):
                agent_Instagram.append(i.a.get('href'))
                I=1
    except:
        pass
    if F == 0:
        agent_facebook.append('')
    if L == 0:
        agent_Linkedin.append('')
    if Ye == 0:
        agent_Yelp.append('')
    if I == 0:
        agent_Instagram.append('')
    try:
        agent_Youtube.append(soup.find('a',{'class':'ytp-title-link yt-uix-sessionlink'}).get('href'))
    except:
        agent_Youtube.append('')
    try:
        address.append(soup.find('div',{'class':'f-left'}).find('div',{'class':'media__content'}).text.replace('\n',''))
    except:
        address.append('')
    try:
        Zip.append(str(soup.find('div',{'class':'f-left'}).find('div',{'class':'media__content'})).split('<br/>')[2].split(',')[-1].split()[-1])
    except:
        Zip.append('')
    try:
        state.append(str(soup.find('div',{'class':'f-left'}).find('div',{'class':'media__content'})).split('<br/>')[2].split(',')[-1].split()[0])
    except:
        state.append('')
    try:
        office_phone.append(soup.find('div',{'class':'f-left'}).find('strong',{'class':'vmiddle font-15 footer-bottom--phone--CA'}).text.strip().replace('.',''))
    except:
        office_phone.append('')







data=pd.DataFrame({
'unique_id':'',
'agent_url':'',
'agent_dp':agent_profile_url,
'agent_name':agent_name,
'agent_phone':phone,
'agent_email':'',
'agent_role':'',
'agent_license':'',
'agent_areaserved':area_served,
'agent_designations':'',
'agent_facebook':agent_facebook,
'agent_instagram':agent_Instagram,
'agent_twitter':'',
'agent_linkedin':agent_Linkedin,
'agent_pinterest':'',
'agent_youtube':agent_Youtube,
'agent_site':rating,
'agent_special_tag':tag,
'agent_rating':'',
'office_address':address,
'office_fax':'',
'office_branch':branch,
'office_name':office,
'office_phone':office_phone,
'office_site':'',
'office_zip':Zip,
'office_state':state,
'other_phone':'',
'company_facebook': '',
'company_linkedin': '',
'company_name': 'ERA',
'company_site': 'https://www.era.com',
'company_twitter':'',
'date_of_data_extraction': datetime.now(),
'data_extracted_by': 'Justin',
'dataextraction_uuid': 'Justin-'+datetime.now().strftime('%d-%m-%Y')

})


for i in range(len(data)):
    data.loc[i,'unique_id'] = 'era_'+str(i+1)

def execute_values(conn, df, table):
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL quert to execute
    query  = "INSERT INTO %s(%s) VALUES %%s;" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("execute_values() done")
    cursor.close()


connection = psycopg2.connect(user='postgres',
                              password='smartsetter',
                              host='ss-db-data-dev.cpeist8s9qou.us-west-2.rds.amazonaws.com',
                              port=5432,
                              database='postgres')

execute_values(connection,data , 'internal_data_exctraction')

data.to_excel('era.xlsx',index=False)










