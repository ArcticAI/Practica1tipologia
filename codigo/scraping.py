import requests
from bs4 import BeautifulSoup
import pandas as pd
import subprocess
import wget
import re
import os
import glob


def get_rounds():
    rnd_list=[]

    for x in soup.find_all('td',{'class','mod-rnd'}):
        rnd_list.append(int(x.text))
        
    return rnd_list


def get_players():
    player_list=[]
    
    for x in soup.find_all('div',{'class','text-of'}):
        player_list.append(x.text)
    
    return player_list


def get_countries():
    country_list=[]
    
    for i,x in enumerate(soup.find_all('i',{'class','flag'})):
        if (i>0):
            country_list.append(x.attrs['class'][1].split('-')[1])
    
    return country_list


def get_teams():
    team_list=[]
    
    for x in soup.find_all('div',{'class','stats-player-country'}):
        team_list.append(x.text)

    return team_list


def get_clutches():
    cl_list=[]
    
    for x in soup.find_all('td',{'class','mod-cl'}):
        num,den = x.text.strip().split('/')[0],x.text.strip().split('/')[1]
        cl_list.append(int(round(int(num)*100/int(den),0)))
    
    return cl_list


def get_max_kills():
    kmax_list=[]
    
    for x in soup.find_all('td',{'class','mod-kmax'}):
        kmax_list.append(int(x.text.strip()))
    
    return kmax_list


def get_k_d_a_fk_fd():
    k_list,k_index = [],[]
    d_list,d_index = [],[]
    a_list,a_index = [],[]
    fk_list,fk_index = [],[]
    fd_list,fd_index = [],[]

    for i in range(78):
        k_index.append(i*5)

    for i in range(78):
        d_index.append(i*5+1)

    for i in range(78):
        a_index.append(i*5+2)

    for i in range(78):
        fk_index.append(i*5+3)

    for i in range(78):
        fd_index.append(i*5+4)

    m = re.findall('<td>[0-9]+</td>', str(soup))

    for i,x in enumerate(m):
    
        if (i in k_index):
            k_list.append(int(x.split('<td>')[1].split('</td>')[0]))
        
        if (i in d_index):
            d_list.append(int(x.split('<td>')[1].split('</td>')[0]))
    
        if (i in a_index):
            a_list.append(int(x.split('<td>')[1].split('</td>')[0]))
    
        if (i in fk_index):
            fk_list.append(int(x.split('<td>')[1].split('</td>')[0]))
    
        if (i in fd_index):
            fd_list.append(int(x.split('<td>')[1].split('</td>')[0]))
    return k_list,d_list,a_list,fk_list,fd_list


def get_acs_kd_adr_kpr_apr_fkpr_fdpr_hs():
    acs_list,acs_index = [],[]
    kd_list,kd_index = [],[]
    adr_list,adr_index = [],[]
    kpr_list,kpr_index = [],[]
    apr_list,apr_index = [],[]
    fkpr_list,fkpr_index = [],[]
    fdpr_list,fdpr_index = [],[]
    hs_list,hs_index = [],[]

    i=0
    for x in range(78):
        acs_index.append(i)
        i+=9

    i=1
    for x in range(78):
        kd_index.append(i)
        i+=9

    i=2
    for x in range(78):
        adr_index.append(i)
        i+=9

    i=3
    for x in range(78):
        kpr_index.append(i)
        i+=9

    i=4
    for x in range(78):
        apr_index.append(i)
        i+=9

    i=5
    for x in range(78):
        fkpr_index.append(i)
        i+=9

    i=6
    for x in range(78):
        fdpr_index.append(i)
        i+=9

    i=7
    for x in range(78):
        hs_index.append(i)
        i+=9

    mid = soup.find_all('div',{'class','color-sq'})
    
    for i,x in enumerate(mid):
        if(i in acs_index):
            acs_list.append(float(str(x).split('<span>')[1].split('</span>')[0]))
        
        if(i in kd_index):
            kd_list.append(float(str(x).split('<span>')[1].split('</span>')[0]))
    
        if(i in adr_index):
            adr_list.append(float(str(x).split('<span>')[1].split('</span>')[0]))
    
        if(i in kpr_index):
            kpr_list.append(float(str(x).split('<span>')[1].split('</span>')[0]))
        
        if(i in apr_index):
            apr_list.append(float(str(x).split('<span>')[1].split('</span>')[0]))
        
        if(i in fkpr_index):
            fkpr_list.append(float(str(x).split('<span>')[1].split('</span>')[0]))
        
        if(i in fdpr_index):
            fdpr_list.append(float(str(x).split('<span>')[1].split('</span>')[0]))
    
        if(i in hs_index):
            hs_list.append(int(str(x).split('<span>')[1].split('</span>')[0].replace('%','')))
    
    return acs_list,kd_list,adr_list,kpr_list,apr_list,fkpr_list,fdpr_list,hs_list


def get_agent_info():
    number_agents=[]
    morethantwo = []
    isOTP = []
    agents = []
    mains = []
    first_agent = []
    second_agent = []

    for x in soup.find_all('td',{'class','mod-agents'}):
        if(len(str(x).split('<div>')[1].split('</div>')[0].split())==10):
            number_agents.append(1)
            morethantwo.append(0)
            isOTP.append(1)
        if(len(str(x).split('<div>')[1].split('</div>')[0].split())==20):
            number_agents.append(2)
            morethantwo.append(0)
            isOTP.append(0)
        if(len(str(x).split('<div>')[1].split('</div>')[0].split())==21):
            number_agents.append(3)
            morethantwo.append(1)
            isOTP.append(0)
    
    for x in re.findall('img/vlr/game/agents/[A-Za-z]+.png', str(soup)):
        agents.append(x.split('agents/')[1].split('.png')[0])
    
    for x in number_agents:
        if(x==1):
            elements = []
            elements.append(agents.pop(0))
            elements.append(0)
            mains.append(elements)
        if(x!=1):
            elements = []
            elements.append(agents.pop(0))
            elements.append(agents.pop(0))
            mains.append(elements)
    
    for x in mains:
        first_agent.append(x[0])
        second_agent.append(x[1])
    
    return number_agents,morethantwo,isOTP,first_agent,second_agent


def setCountries(data):
    data.loc[data.Country=='ru','Country'] = 'Russia'
    data.loc[data.Country=='br','Country'] = 'Brazil'
    data.loc[data.Country=='us','Country'] = 'USA'
    data.loc[data.Country=='ca','Country'] = 'Canada'
    data.loc[data.Country=='tr','Country'] = 'Turkey'
    data.loc[data.Country=='kr','Country'] = 'Korea'
    data.loc[data.Country=='jp','Country'] = 'Japan'
    data.loc[data.Country=='cl','Country'] = 'Chile'
    data.loc[data.Country=='fr','Country'] = 'France'
    data.loc[data.Country=='es','Country'] = 'Spain'
    data.loc[data.Country=='pl','Country'] = 'Poland'
    data.loc[data.Country=='sg','Country'] = 'Singapore'
    data.loc[data.Country=='ua','Country'] = 'Ukraine'
    data.loc[data.Country=='fi','Country'] = 'Finland'
    data.loc[data.Country=='ar','Country'] = 'Argentina'
    data.loc[data.Country=='id','Country'] = 'Indonesia'
    data.loc[data.Country=='my','Country'] = 'Malaysia'
    data.loc[data.Country=='dk','Country'] = 'Denmark'
    data.loc[data.Country=='lt','Country'] = 'Lithuania'
    data.loc[data.Country=='be','Country'] = 'Belgium'
    data.loc[data.Country=='th','Country'] = 'Thailand'
    data.loc[data.Country=='gb','Country'] = 'England'
    data.loc[data.Country=='cz','Country'] = 'Czech Republic'
    data.loc[data.Country=='hr','Country'] = 'Croatia'
    data.loc[data.Country=='se','Country'] = 'Sweden'
    data.loc[data.Country=='eg','Country'] = 'Egypt'
    data.loc[data.Country=='by','Country'] = 'Belarus'
    data.loc[data.Country=='de','Country'] = 'Germany'
    data.loc[data.Country=='kz','Country'] = 'Kazakhstan'
    data.loc[data.Country=='no','Country'] = 'Norway'
    data.loc[data.Country=='ba','Country'] = 'Bosnia and Herzegovina'
    data.loc[data.Country=='lv','Country'] = 'Latvia'
    data.loc[data.Country=='mn','Country'] = 'Mongolia'
    data.loc[data.Country=='co','Country'] = 'Colombia'
    data.loc[data.Country=='mx','Country'] = 'Mexico'
    data.loc[data.Country=='gt','Country'] = 'Guatemala'
    data.loc[data.Country=='pr','Country'] = 'Puerto Rico'
    data.loc[data.Country=='ph','Country'] = 'Philippines'
    data.loc[data.Country=='tw','Country'] = 'Taiwan'
    return data


def get_images(soup):
  imgs = soup.findAll("img",{"src":True})
  img_list = []
  for img in dict.fromkeys(imgs):
    imgUrl = "https://www.vlr.gg" + img['src'] .strip('"')
    img_name =  imgUrl.rsplit('/', 1)[-1]
    if not os.path.exists(img_name):
      if img_name.rsplit('.', 1)[-2].isalpha() \
      and imgUrl[len(imgUrl)-4:] == ".png": 
        wget.download(imgUrl)

  img_list = glob.glob('*.png')
  return img_list


def assign_images(df, list_imgs):
  col_img = "ImagenFirstAgent"
  df[col_img] = df["FirstAgent"] + ".png"
  df[col_img] = ["" if x in list(filter(lambda x: x not in list_imgs, df[col_img])) else x for x in df[col_img]]


event_urls = [
    ['Masters Berlin', 'https://www.vlr.gg/event/stats/466/valorant-champions-tour-stage-3-masters-berlin', 'Europe'],
    ['Masters Reykjavik', 'https://www.vlr.gg/event/stats/353/valorant-champions-tour-stage-2-masters-reykjavik', 'Europe'],
    ['Last Chance EMEA', 'https://www.vlr.gg/event/stats/559/champions-tour-emea-last-chance-qualifier', 'EMEA'],
    ['Online Europe', 'https://www.vlr.gg/event/stats/334/champions-tour-europe-stage-1-masters', 'Europe'],
    ['Masters CIS', 'https://www.vlr.gg/event/stats/344/champions-tour-cis-stage-1-masters', 'CIS'],
    ['Masters TURK', 'https://www.vlr.gg/event/stats/342/champions-tour-turkey-stage-1-masters', 'Turkey'],
    ['Masters NA', 'https://www.vlr.gg/event/stats/333/champions-tour-north-america-stage-1-masters', 'North America'],
    ['Last Chance NA', 'https://www.vlr.gg/event/stats/558/champions-tour-north-america-last-chance-qualifier', 'North America'],
    ['Last Chance LATAM', 'https://www.vlr.gg/event/stats/561/champions-tour-south-america-last-chance-qualifier', 'LATAM'],
    ['Masters BR', 'https://www.vlr.gg/event/stats/338/champions-tour-brazil-stage-1-masters', 'Brazil'],
    ['Masters KR', 'https://www.vlr.gg/event/stats/351/champions-tour-korea-stage-1-masters', 'Korea'],
    ['Masters JP', 'https://www.vlr.gg/event/stats/352/champions-tour-japan-stage-1-masters', 'Japan'],
    ['Masters SEA', 'https://www.vlr.gg/event/stats/347/champions-tour-sea-stage-1-masters', 'SEA']
]  


event_list = []

for url in event_urls:
    r = requests.get(url[1])
    soup = BeautifulSoup(r.text, 'lxml')
    event = []
    event = pd.DataFrame({
        'Player': get_players(),
        'Country': get_countries(),
        'Team': get_teams(),
        'FirstAgent': get_agent_info()[3],
        'SecondAgent': get_agent_info()[4],
        'MoreThan2Agents': get_agent_info()[1],
        'OTP': get_agent_info()[2],
        'Rounds': get_rounds(),
        'AverageCombatScore': get_acs_kd_adr_kpr_apr_fkpr_fdpr_hs()[0],
        'KillsDeaths': get_acs_kd_adr_kpr_apr_fkpr_fdpr_hs()[1],
        'AverageDamagePerRound': get_acs_kd_adr_kpr_apr_fkpr_fdpr_hs()[2],
        'KillsPerRound': get_acs_kd_adr_kpr_apr_fkpr_fdpr_hs()[3],
        'AssistsPerRound': get_acs_kd_adr_kpr_apr_fkpr_fdpr_hs()[4],
        'FirstKillsPerRound': get_acs_kd_adr_kpr_apr_fkpr_fdpr_hs()[5],
        'FirstDeathsPerRound': get_acs_kd_adr_kpr_apr_fkpr_fdpr_hs()[6],
        'HeadshotPercentage': get_acs_kd_adr_kpr_apr_fkpr_fdpr_hs()[7],
        'ClutchesPercentage': get_clutches(),
        'MaxKillsPerMap': get_max_kills(),
        'Kills': get_k_d_a_fk_fd()[0],
        'Deaths': get_k_d_a_fk_fd()[1],
        'Assists': get_k_d_a_fk_fd()[2],
        'FirstKills': get_k_d_a_fk_fd()[3],
        'FirstDeaths': get_k_d_a_fk_fd()[4],
        'Tournament': url[0],
        'Region': url[2]
    })
    
    event = setCountries(event)
    lista_imagenes = get_images(soup)
    assign_images (event, lista_imagenes)
    event_list.append(event)

ds = event_list[0]

for i in range(1,len(event_list) - 1):
    ds = ds.merge(event_list[i], how='outer')

ds.to_csv('valorantscraping.csv',index=False)