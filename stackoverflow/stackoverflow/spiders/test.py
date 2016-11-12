import json
filename = 'myfile.json'
f = open(filename, 'wb')
res=[{'a':1,'b':2},{'a':3,'b':4}]
#parsed = json.loads(res)
f.write( json.dumps(res, indent=4, sort_keys=True))