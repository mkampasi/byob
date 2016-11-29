These are useful commands to setup solr on your machine. These should be run after navigating to the directory where the solr installer zip file was extracted.

To start solr

1. bin/solr start

To create core:

1.  bin/solr create -c byob

To load core:

1. bin/post -c byob <folder location where all source json files are present>/*.json

To delete core:

1. bin/solr delete -c byob -p 8983

To re-index data:

1. Delete all data as follows: 
   http://localhost:8983/solr/byob/update?stream.body=%3Cdelete%3E%3Cquery%3E*:*%3C/query%3E%3C/delete%3E&commit=true
2. Reload core
3. Load core again to re-index

