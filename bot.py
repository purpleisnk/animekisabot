#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

episode_url = 'https://animekisa.tv'
url = 'https://animekisa.tv/search?q='

#response = requests.post(url)
#title = input('What title would you like to search?\n')
#title = 'Attack on Titan'
title = 'One Punch Man'

### Breaks down the  keyword and makes it compatible to  be used in url for search
def search_query(titles):
	titles = title
	lower_case = titles.lower()
	split_words = lower_case.split()
	result = '+'.join(split_words)
	search_url = (url+result)
	response = requests.get(search_url)

	soup = BeautifulSoup(response.text, 'html.parser')
	similar_result = soup.find_all('a',attrs={"class" : 'an'})

	#################This is converting the parsed <div> containing the info(eg: title name, link, image link)
	list_results = []

	for result in similar_result:
		list_results.append(result)


	#This is  returning the removed extra spaces and again returning 
	#all the searced result into a list
	joined_list = []
	for result in list_results:
		split_result = result.text.split()
		join_result = ' '.join(split_result)
		joined_list.append(join_result)

	ready_for_check = joined_list
	###Returns the index no on which the operation to get the link of the episodes is to be performed
	operate_list_no = ready_for_check.index(title)

	# Here we are going to check if the search result matches the title we want
	if title in ready_for_check:
		print(f'Your Search for <<{title}>> has been found on this page')
	else:
		print(f'Result matching your search[ {title} ] --Not Found')

	####Selects the div with indexing based on the title (the below div is a single div ready to be parsed)

	selected_div = soup.find_all('a',attrs={"class" : 'an'})[operate_list_no]
	## contains the list broken down using split so the link can  be accessed using list indexing
	elements_list = []
	new = str(selected_div)
	for elements in new.split():
		elements_list.append(elements)
	href_str = elements_list[2]
	##prints the cleaned link	
	cleaned_link = href_str[6:-2]
	get_episode_url = episode_url+cleaned_link

######Searching through each episode of the Link and getting the streamable link

	all_episodes = requests.get(get_episode_url)
	all_episodes_soup = BeautifulSoup(all_episodes.text, 'html.parser')
	available_episodes = all_episodes_soup.find_all('a', attrs={'class' : 'infovan'})
	available_episodes = (available_episodes)
	## To store each tag to be siced later
	list_of_avilable_episodes= []
	## To use this as a split  list for the above list
	new_list_of_avilable_episodes= []
	for each_ep in available_episodes:
		each_ep = str(each_ep)
		list_of_avilable_episodes.append(each_ep)
	i = len(list_of_avilable_episodes)

	for x in list_of_avilable_episodes:
		one1 = x.split()
		one2 = one1[2]
		stream_link = one2[6:-2]
		new_list_of_avilable_episodes.append(stream_link)

	url_ = 'https://animekisa.tv/'
	episode = new_list_of_avilable_episodes[0]
	new_url = url_+episode
	single_ep_url = requests.get(new_url)
	new_soup = BeautifulSoup(single_ep_url.text, 'html.parser')
	link_tag = new_soup.find('iframe')
	print(str(link_tag))
	video_link = []

	#selected_div_soup = BeautifulSoup(selected_div.text, 'html.parser')
search_query(title)

