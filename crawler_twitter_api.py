import urllib.parse
import urllib.request
import json
import tweepy

from crawler_abst_api import CrawlerAbstractAPI


class TwitterApi(CrawlerAbstractAPI):
    """
    There are people and tags. Tags are bipartite 0. Persons bipartite 1.

    Variables
    _baseUrl -- This is the URL that access the API interface
    _delay -- Number of seconds to wait between API calls
    """

    _baseUrl = 'https://api.twitter.com/1.1/search/'
    _searchQuery = 'tweets.json?q={}&result_type=recent&lang=en&count={}&max_id={}'
    _consumer_key = "NkQPzpiRJZ6CJVeRzrVLqIGuh"
    _consumer_secret = "yMhadrMcNmAQyFGX8YKDWtyX6szbr3hKGwCKrz9xp36KPI7tMX"
    _access_key = "1066866967-dDLwsuOq4YdKRm1v1v4lbzWlu3rTMvPoS8TYjWG"
    _access_secret = "FiC4HGQDEInch3tar4nGDwpApxcwI2KesP85h3JXOX5fo"

    _auth = tweepy.OAuthHandler(_consumer_key, _consumer_secret)
    _auth.set_access_token(_access_key, _access_secret)
    _api = tweepy.API(_auth)

    def initial_nodes(self):
        initial_tag = '#TeamJB'

        return [(initial_tag, self.make_node_tag(initial_tag, 0))]

    def make_tags_url(self, tag):
        """
           Returns a URL that can be used to issue the query.
        """
        q_string = urllib.parse.quote_plus(tag)
        q_url = ''.join([self._baseUrl, self._searchQuery])

        return q_url.format(q_string, 15, '')

    def make_node_tag(self, tag, depth):
        """
        Makes a node representing a tag

        Arguments
        id -- the node id (converted to a string)
        tag -- the tag string
        depth -- depth of the search to this point
        graph -- Graph object to add the node to
        """
        nid = super().make_node(0, tag, depth)
        return nid

    def make_node_user(self, name, user, depth):
        """
               Makes a node representing a user
        """
        nid = self.make_node(1, name, depth)
        # self._graph.nodes[name] =
        return nid;

    def execute_tags_query(self, tag):
        """
        Executes the tags query and parses the results
        """
        url = self.make_tags_url(tag)
        try:
            data = self._api.search("#TeamJB", count=2, tweet_mode='extended', result_type='recent')

            tags = []
            for tweet in data:
                for t in tweet._json['entities']['hashtags']:
                    tags.append(t['text'])

            return True, tags
        except ValueError as e:
            print(e)
        except TypeError as e:
            print(e)
            return self._ERROR_RESULT



    # These are TAGS bipartite 0
    def get_child0(self, node, graph, state, new_depth):
        tag = graph.nodes[node]['label']
        success, data = self.execute_tags_query(tag)

        if success:
            # Distinguish nodes previously seen from new nodes
            old_tags = [tag for tag in data if state.is_visited(0, tag)]
            new_tags = [tag for tag in data if not (state.is_visited(0, tag))]

            # Get the existing nodes
            old_nodes = [state.visited_node(0, tag) for tag in old_tags]

            # Create the new nodes
            new_depth = graph.node[node]['_depth'] + 1
            new_nodes = [self.make_node_tag(tag, new_depth)
                         for tag in new_tags]
            return {'success': True, 'new': new_nodes, 'old': old_nodes}
        else:
            return {'success': False}

    def get_child1(self, node, graph, state, new_depth):
        pass
