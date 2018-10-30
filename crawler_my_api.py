import urllib.parse
import urllib.request
import json
from crawler_abst_api import CrawlerAbstractAPI


class MyAPI (CrawlerAbstractAPI):
    """
    Encapsulates the interactions for the API used in lab.
    There are people and tags. Person is bipartite 0. Tags bipartite 1.

    Variables
    _baseUrl -- This is the URL that access the API interface
    _delay -- Number of seconds to wait between API calls
    """

    _baseUrl = "http://josquin.cti.depaul.edu/~rburke/cgi-bin/"
    _nameQuery = "get-users.py?q={}"
    _tagQuery = "get-tags.py?q={}"
    _nameErrorTest = "get-users.py?q={}&ErrRate=100"

    def initial_nodes(self):
        initial_tag = '#Foo'

        # You might have make a query to get the attribute here.
        return [(initial_tag, self.make_node_tag(initial_tag, 0))]

    def make_names_url(self, tag):
        """
        Returns a URL that can be used to issue the query.

        Arguments
        query -- a string to be passed to the API
        """
        q_string = urllib.parse.quote_plus(tag)  # Escape special characters
        q_url = ''.join([self._baseUrl, self._nameQuery])
        return q_url.format(q_string)

    def make_tags_url(self, name):
        """
        Returns a URL that can be used to issue the query.

        Arguments
        query -- a string to be passed to the API
        """
        q_string = urllib.parse.quote_plus(name)  # Escape special characters
        q_url = ''.join([self._baseUrl, self._tagQuery])
        return q_url.format(q_string)

    def make_node_user(self, name, planet, depth):
        """
        Makes a node representing a user

        Arguments
        id -- the node id (converted to a string)
        name -- user name
        planet -- the user's planet
        depth -- depth of the search to this point
        graph -- Graph object to add the node to
        """
        nid = self.make_node(0, name, depth)
        self._graph.nodes[nid]['planet'] = planet

        return nid

    def make_node_tag(self, tag, depth):
        """
        Makes a node representing a tag

        Arguments
        id -- the node id (converted to a string)
        tag -- the tag string
        depth -- depth of the search to this point
        graph -- Graph object to add the node to
        """
        nid = super().make_node(1, tag, depth)

        return nid

    def execute_names_query(self, tag):
        """
        Executes the names query and parses the results.

        Arguments
        tag -- a tag

        Returns
        (success flag, data) -- tuple
        success flag -- true if the values were successfully parsed (no errors)
        data -- a list of (name, planet) pairs that resulted from the query
        """
        url = self.make_names_url(tag)
        try:
            data = json.loads(urllib.request.urlopen(url).read())
            if data['type'] == 'Error':
                return self._ERROR_RESULT

            return (True, [(user['user_id'], user['planet'])
                           for user in data['users']])
        except ValueError as e:
            # Usually this means that the API call has failed
            print(e)
            return self._ERROR_RESULT
        except TypeError as e:
            print(e)
            return self._ERROR_RESULT

    def execute_tags_query(self, name):
        """
        Executes the tags query and parses the results.

        Arguments
        name -- a user name

        Returns
        (success flag, data) -- tuple
        success flag -- true if the values were successfully parsed (no errors)
        data -- a list of tags that resulted from the query
        """
        url = self.make_tags_url(name)
        try:
            data = json.loads(urllib.request.urlopen(url).read())
            if data['type'] == 'Error':
                return self._ERROR_RESULT
            return True, data['tags']
        except ValueError as e:
            # Usually this means that the API call has failed
            print(e)
            return self._ERROR_RESULT
        except TypeError as e:
            print(e)
            return self._ERROR_RESULT

    # These are USERS bipartite 0
    def get_child0(self, node, graph, state):
        name = graph.node[node]['label']
        success, data = self.execute_tags_query(name)

        if success:
            # Distinguish nodes previously seen from new nodes
            old_tags = [tag for tag in data if state.is_visited(1, tag)]
            new_tags = [tag for tag in data if not (state.is_visited(1, tag))]

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
        success, data = self.execute_names_query(tag)

        if success:
            # Distinguish nodes previously seen from new nodes
            old_names = [name for name, planet in data if state.is_visited(0, name)]
            new_names = [(name, planet) for name, planet in data
                         if not (state.is_visited(0, name))]
            old_nodes = [state.visited_node(0, name) for name in old_names]

            new_depth = graph.node[node]['_depth'] + 1
            new_nodes = [self.make_node_user(name, planet, new_depth)
                         for name, planet in new_names]
            return {'success': True, 'new': new_nodes, 'old': old_nodes}
        else:
            return {'success': False}
