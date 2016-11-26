import json
import os
finalresult=[]
languages=[]
filesarray = ["hot","featured","week","month","interesting"]

#Load master list of languages from Github
with open('../output/'  + 'languages.json') as language_file:    
    languages = json.load(language_file)
    languages=set(languages)
#Load master list of Field of study from Github
with open('../output/'  + 'fos.json') as fos_file:    
    fos = json.load(fos_file)
    fos=set(fos)
    
#Load Stackoverflow trending topics scraped in previous step
for files in filesarray:
    with open('../output/' + files + '.json') as data_file:    
        data = json.load(data_file)
        finalresult = finalresult + data
        os.remove('../output/' + files + '.json')
        
#Clean data by categorizing language, field of study and other separately
for record in finalresult:
    tags = set(record["tags"])
    record["languages"]=list(tags.intersection(languages))
    record["field_of_study"] = list(tags.intersection(fos))
    record["other"] = list(tags.difference(languages).difference(fos))
    record.pop('tags')
f = open('../output/'  + 'stackoverflowdata.json','w+')

f.write(json.dumps(finalresult,indent=4))