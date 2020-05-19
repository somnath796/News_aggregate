from django.shortcuts import render
from django.db import IntegrityError
# Create your views here.

import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline


def news_list(request):
	headlines = Headline.objects.all()[::-1]
	context ={
		"object_list": headlines,
	}

	return render(request , "news/home.html",context)

def scrape(request):
	session = requests.Session()
	session.headers ={"User-Agent":"Googlebot/2.1 (+http://www.google.com/bot.html)"}
	url = "https://www.indiatoday.in/world"

	for page in range(1,5):
			url+='?page=%d'%page

			content = session.get(url, verify=False).content
			soup = BSoup(content,"html.parser")
		    #News = soup.find_all('div',{"class": "view-content"})

		    #for article in News:
			
			News = soup.find_all('div',{"class": "catagory-listing"})

			for article in News:
			
				image_url = article.find('div',{"class": "pic"}).img['src']
				title=  article.find('div',{"class": "detail"}).h2.a.contents[0]
				link = str(url[:-6]+article.find('div',{"class": "detail"}).h2.a['href'])
				try:
					description = str(article.find('div',{"class": "detail"}).p.text)
				except:
					description = str(article.find('div',{"class": "detail"}).p)


				new_headline = Headline()
				new_headline.title = title
				new_headline.url = link
				new_headline.image = image_url
				new_headline.description= description

				try:
					new_headline.save()
				
				except IntegrityError as e: 
					if 'unique constraint' in e.args:
						continue 


	return redirect("../")
    
    

