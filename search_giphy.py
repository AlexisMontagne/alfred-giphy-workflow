import sys
import urllib
import urllib2
import json

from workflow import Workflow

GIPHY_URL = "http://api.giphy.com/v1/gifs/search?q={}&api_key=dc6zaTOxFJmzC&limit=5"


def main(wf):
    args = wf.args
    query = ' '.join(args[0:])

    def request_gifs():
        resp = urllib2.urlopen(
            GIPHY_URL.format(urllib.quote_plus(query))).read()

        gifs = json.loads(resp)["data"]

        for gif in gifs:
            f = open(wf.cachefile("{}.{}".format(gif['id'], gif['type'])), 'w')
            f.write(urllib2.urlopen(
                gif['images']['fixed_height_downsampled']['url']).read())
            f.close()

        return gifs

    results = wf.cached_data(query, request_gifs, max_age=3600)
    # results = request_gifs()

    if not results or len(results) == 0:
        title = 'No results'
        subtitle = 'We could not fetch any gifs for \'{0}\''.format(query)
        wf.add_item(title, subtitle)
    else:
        for document in results:
            wf.add_item(
                title=document['caption'] or query,
                subtitle=document['url'],
                arg=document['images']['original']['url'],
                valid=True,
                icon=wf.cachefile(
                    "{}.{}".format(document['id'], document['type'])))

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
