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

    _auth = tweepy.OAuthHandler(_consumer_key, _consumer_secret)
    _auth.set_access_token(_access_key, _access_secret)
    _api = tweepy.API(_auth)

    def initial_nodes(self):
        # initial_tag = 'TeamJB'
        initial_tag = 'TeamRauner'

        return [(initial_tag, self.make_node_tag(initial_tag, 0))]

    def make_node_user(self, user_id, name, tag, depth):
        """
               Makes a node representing a user
        """
        nid = self.make_node(0, user_id, depth)
        self._graph.nodes[nid]['screen_name'] = name
        self._graph.nodes[nid]['user_tag'] = tag
        return nid;

    def make_node_tag(self, tag, depth):
        """
        Makes a node representing a tag

        Arguments
        id -- the node id (converted to a string)
        tag -- the tag string
        depth -- depth of the search to this point
        graph -- Graph object to add the node to
        """
        nid = super().make_node(1, '#'+tag, depth)
        self._graph.nodes[nid]['tag'] = tag
        return nid

    def execute_names_query(self, user_id):
        try:
            # data = self._api.search('#'+tag, count=10, tweet_mode='extended', result_type='recent')
            data = self._api.user_timeline(user_id)

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

    def execute_tags_query(self, tag):
        """
        Executes the tags query and parses the results
        """
        try:
            data = self._api.search(tag, count=50, tweet_mode='extended', result_type='recent')

            users = [(tweet._json['user']['screen_name'], tweet._json['user']['id']) for tweet in data]

            return True, users
        except ValueError as e:
            print(e)
        except TypeError as e:
            print(e)
            return self._ERROR_RESULT

    # These are USERS bipartite 0
    def get_child0(self, node, graph, state):
        user_id = graph.nodes[node]['label']
        success, data = self.execute_names_query(user_id)

        if success:
            # Distinguish nodes previously seen from new nodes
            old_tags = [tag for tag in data if state.is_visited(1, tag)]
            new_tags = list(set([tag for tag in data if not (state.is_visited(1, tag))]))

            # Get the existing nodes
            old_nodes = [state.visited_node(1, tag) for tag in old_tags]

            # Create the new nodes
            new_depth = graph.node[node]['_depth'] + 1
            new_nodes = [self.make_node_tag(tag, new_depth)
                         for tag in new_tags]
            # Return the dict with the info
            return {'success': True, 'new': new_nodes, 'old': old_nodes}
        else:
            return {'success': False}

    # These are TAGS bipartite 1
    def get_child1(self, node, graph, state):
        tag = graph.nodes[node]['label']
        success, data = self.execute_tags_query(tag);

        if success:
            # Distinguish nodes previously seen from new nodes
            old_names = [user_id for name, user_id in data if state.is_visited(0, user_id)]
            new_names = list(set([(name, user_id) for name, user_id in data if not (state.is_visited(0, user_id))]))
            # duplicate nodes are appearing twice, this might be the fix

            old_nodes = [state.visited_node(0, user_id) for user_id in old_names]

            new_depth = graph.node[node]['_depth'] + 1
            new_nodes = [self.make_node_user(user_id, name, tag, new_depth)
                         for name, user_id in new_names]

            return {'success': True, 'new': new_nodes, 'old': old_nodes}
        else:
            return {'success': False}