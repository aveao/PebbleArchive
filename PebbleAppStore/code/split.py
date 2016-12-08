import json
import rq
from redis import Redis
from rq import Queue

q = Queue(connection=Redis())

#Once we've processed everything into a single JSON, split it up and enqueue them in groups of 20 for easier downloading.

x = open("all.json")
l = list(json.loads(x.readlines()[0]))
n=20
allList = [l[i:i + n] for i in xrange(0, len(l), n)]
print allList
for listSet in allList:
	result = q.enqueue('pbldown.downloadArray', json.dumps(listSet))
