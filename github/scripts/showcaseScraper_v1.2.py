import requests
from bs4 import BeautifulSoup
import json

link_prefix = "https://github.com"
repo_json_data = []

unique_languages = []
all_fos = []
tags = {}

with open("../input/allLangLinks.txt",'r') as fin,open("../output/showcase_v1.2_master_dump.json","w+") as jsonfout:

	for link in fin:
		print "Processing :: " + link

		repo_showcase_data = []
		r = requests.get(link.strip())
		soup = BeautifulSoup(r.content,'html.parser')

		repo_list_tag = soup.find_all("li",{"class" : "py-4"})
		meta_data_List = []

		for row in repo_list_tag:
			if(row is not None):
				
				repo_link = ""
				repo_name = ""
				repo_description = ""
				repo_language = ""
				data = {}

				data["source"] = "github"

				repo_header = row.find("div",{"class" : "mb-1"}).find("h3").find("a")['href']
				if(repo_header is not None):
					repo_link = link_prefix + repo_header.strip()
					data["repo_link"] = repo_link

				repo_name_tag = row.find("div",{"class" : "mb-1"}).find("h3").find("a")
				if(repo_name_tag is not None):
					repo_name = repo_name_tag.text.strip()
					data["repo_name"] = repo_name

				description_header = row.find("div",{"class" : "py-1"})
				if(description_header is not None):
					repo_description = description_header.text.strip()
					if repo_description.strip() == '':
						data["repo_description"] = "Not Available"
					else:	
						data["repo_description"] = repo_description

				repo_language_header = row.find("span",{"itemprop" : "programmingLanguage"})
				if(repo_language_header is not None):
					repo_language = repo_language_header.text.strip()
					data["repo_language"] = repo_language

				repo_stargazers = row.find("a",{"aria-label" : "Stargazers"})
				if(repo_stargazers is not None):
					data["stargazers"] = repo_stargazers.text.strip()
					print repo_stargazers.text.strip()

				repo_json_data.append(data)

	final_dump = json.dumps(repo_json_data, indent=4)
	jsonfout.write(final_dump)