import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/search/keyword/?keywords=anime&sort=moviemeter,asc&mode=detail&page=1&ref_=kw_nxt'
response = requests.get(url)
soup = BeautifulSoup(response.content,'html.parser')

#create empty lists
Title = []
release_year = []
genre = []
duration = []
rating = []
desc = []
votes = []

anime_data = soup.findAll('div',attrs = {'class':'lister-item mode-detail'})

final = pd.DataFrame()
for j in range(1,21):
  url = 'https://www.imdb.com/search/keyword/?keywords=anime&sort=moviemeter,asc&mode=detail&page={}&ref_=kw_nxt'.format(j)
  response = requests.get(url)
  soup = BeautifulSoup(response.content,'html.parser')

  anime_data = soup.findAll('div',attrs = {'class':'lister-item mode-detail'})

  for o in anime_data:

    #name = o.h3.a.text
    #Title.append(name)
    try:
      name = o.h3.a.text
      Title.append(name)
    except AttributeError:
      Title.append('NA')

    #OA means on air and the anime is still going on

    #yor = o.h3.find('span',class_='lister-item-year text-muted unbold').text.replace('(','').replace(')','').replace(' ','OA')
    #release_year.append(yor)
    try:
      yor = o.h3.find('span',class_='lister-item-year text-muted unbold').text.replace('(','').replace(')','').replace(' ','OA')
      release_year.append(yor)
    except AttributeError:
      release_year.append('NA')

    #type_anime = o.p.find('span',class_='genre').text.replace('\n','').replace(' ','')
    #genre.append(type_anime)
    try:
      type_anime = o.p.find('span',class_='genre').text.replace('\n','').replace(' ','')
      genre.append(type_anime)
    except AttributeError:
      genre.append('NA')

    #runtime = o.p.find('span',class_='runtime')
    #if o.p.find('span',class_='runtime'):
    #    duration.append(runtime.text.replace(' min',''))
    #else:
        #duration.append('**')
    try:
      runtime = o.p.find('span',class_='runtime')
      if o.p.find('span',class_='runtime'):
        duration.append(runtime.text.replace(' min',''))
      else:
        duration.append('NA')
    except AttributeError:
      duration.append('NA')


    #rate = o.find('div',attrs = {'class':'inline-block ratings-imdb-rating'})
    #rating.append(rate.text.replace('\n',''))
    try:
      rate = o.find('div',attrs = {'class':'inline-block ratings-imdb-rating'})
      rating.append(rate.text.replace('\n',''))
    except AttributeError:
      rating.append('NA')

    #summary = o.find('p',class_='').text.replace('\n','')
    #desc.append(summary)
    try:
      summary = o.find('p',class_='').text.replace('\n','')
      desc.append(summary)
    except AttributeError:
      desc.append('NA')

    #nv = o.find('span',attrs = {'name':'nv'})
    #votes.append(nv.text)
    try:
        nv = o.find('span',attrs = {'name':'nv'})
        votes.append(nv.text)
    except AttributeError:
        votes.append('NA')


anime_DF = pd.DataFrame({
    'Anime Title' : Title,
    'Release Year': release_year,
    'Genre': genre,
    'Duration':duration,
    'Rating':rating,
    'Description':desc,
    'No. of Votes':votes
})

final = final.append(anime_DF)

imdb_anime_data = final.to_csv('imdb_anime_data.csv')

final
