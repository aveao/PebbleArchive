Pebble Archival Code
----

This code was written in a few hours in the back of a lecture. It's not particularly well-formatted, but it's reasonably well guarded from errors, and was able to index some 14K apps and watchfaces.

The current algorithm to index watchfaces is a little... bad. It just reuses the search function to search for aa,ab,ac,...,zz,a,b,c,...,z, and saves all of the found IDs into two JSON files

General structure:

getFaces/getApps.py will search for apps and faces using the described algorithm and produce JSON files.

split.py will take a combined JSON file, split it into chunks, and add it to a Redis queue for batch processing.

pbldown.py - doesn't run on it's own, though it could. It's meant to be invoked via rq, a Python batch processing/queueing tool.

sort.py - Will sort all the downloaded data into folders.

# THIS FILE AND THE CODE WAS WRITTEN BY /U/MAGMAPUS [HERE](https://www.reddit.com/r/pebble/comments/5g0gmx/in_light_of_recent_news_i_archived_the_app_store/) - I ONLY DUMPED THAT DATA HERE FOR SAKE OF ARCHIVAL.
