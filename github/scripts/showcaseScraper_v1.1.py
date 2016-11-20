import requests
from bs4 import BeautifulSoup
import json

link_prefix = "https://github.com"
repo_json_data = []

unique_languages = []
all_fos = []
tags = {}

with open("../input/allLinks.txt",'r') as fin,open("../output/showcase_v1.1.json","w+") as jsonfout, open("../output/tags.json","w+") as tagsFile:

	for link in fin:
		print "Processing :: " + link

		repo_showcase_data = []
		r = requests.get(link.strip())
		soup = BeautifulSoup(r.content,'html.parser')

		title_tag = soup.find("h1",{"class" : "showcase-page-title"})
		
		if(title_tag is not None):
			# repo_showcase_data["field_of_study"] = title_tag.string.strip()
			if(title_tag.string.strip() not in all_fos):
				all_fos.append(title_tag.string.strip())

			repo_list_tag = soup.find_all("li",{"class" : "repo-list-item"})
			if(repo_list_tag is not None):
				meta_data_List = []

				for repo_tag in repo_list_tag:
					
					repo_link = ""
					repo_name = ""
					repo_description = ""
					repo_language = ""
					data = {}

					data["field_of_study"] = title_tag.string.strip()

					repo_header = repo_tag.find("h3",{"class" : "mb-1"}).find("a")['href']
					if(repo_header is not None):
						repo_link = link_prefix + repo_header.strip()
						data["repo_link"] = repo_link	

					repo_name_tag = repo_tag.find("h3",{"class" : "mb-1"}).find("a")
					if(repo_name_tag is not None):
						repo_name = repo_name_tag.text.strip()
						data["repo_name"] = repo_name

					description_header = repo_tag.find("div",{"class" : "pr-4"})
					if(description_header is not None):
						repo_description = description_header.text.strip()
						data["repo_description"] = repo_description

					repo_language_header = repo_tag.find("span",{"itemprop" : "programmingLanguage"})
					if(repo_language_header is not None):
						repo_language = repo_language_header.text.strip()
						data["repo_language"] = repo_language

						if(repo_language not in unique_languages):
							unique_languages.append(repo_language)
					else:
						continue;

					repo_stargazers = repo_tag.find("a",{"aria-label" : "Stargazers"})
					if(repo_stargazers is not None):
						data["stargazers"] = repo_stargazers.text.strip()

					repo_json_data.append(data)

		tags["unique_languages"] = unique_languages
		tags["all_fields_of_studies"] = all_fos

	final_dump = json.dumps(repo_json_data, indent=4)
	jsonfout.write(final_dump)

	tags_dump = json.dumps(tags,indent=4)
	tagsFile.write(tags_dump)
