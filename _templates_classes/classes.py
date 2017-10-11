import urllib
from bs4 import BeautifulSoup
from functools import reduce


class Webpage_content:
    """
        Instantiate a webpage_content.
        In **kwargs, need to be passed :
            - target url
            - html tag for which we want to retrieve text
            - and criterias to define html subset to look data within (optional, if not specified, entire html)
    """
    url = None
    tag_to_retrieve = None
    html_subset = None

    def __init__(self, **kwargs):
        # set class attributes, and check mandatory ones are there
        for key, value in kwargs.items():
            setattr(self, key, value)

        if not self.url or not self.tag_to_retrieve:
            raise ValueError('Target URL and target HTML tag must be provided')

        # get html
        response = urllib.request.urlopen(self.url)
        my_html = response.read()
        soup = BeautifulSoup(my_html, "html5lib", from_encoding="ISO-8859-16")
        # get html subset we want to get data from, if any specified
        if self.html_subset:
            self.html_subset = soup.find(*self.html_subset)

        #my_list = self.get_all_matching_html_children(self)

    def get_all_matching_html_children(self, *args):
        """
            Iterate over a given html and return a list with all smallest html children matching a given tag.
            Finally return an output_list of all smallest htmls children.
        """
        if not args:
            my_list = [self.html_subset] #first time the recursive function in launched, use html_subset
        else:
            my_list = args
            my_list = my_list[1:] # to exclude 'self'
            my_list = my_list[0] # to get back to a list, and not

        temp_list = []
        available_children_in_list = False  # to track existence of possible child within output_list
        for my_html in my_list:
            available_children_in_given_item = False  # to track existence of possible child for a given item
            list_of_children = [item for item in my_html.children]
            for child in list_of_children:
                try:
                    child[self.tag_to_retrieve]
                    temp_list.append(child)
                    available_children_in_list = True
                    available_children_in_given_item = True
                except (KeyError, TypeError):
                    pass
            if not available_children_in_given_item:  # if for a given item there is no possible child, keep original one in the list
                temp_list.append(my_html)

        if not available_children_in_list:  # repeat operation until there are no remaining possible child
            return temp_list
        else:
            return self.get_all_matching_html_children(self, temp_list)

    def get_text_data(self, input_list_html):
        """
            From a list of htlm elements, returns all text contained.
            Output_list = 1 list item per html element in input_list (input list and output list of same length)
        """
        output_list = []
        for child in input_list_html:
            data_in_child = [i for i in child.stripped_strings]
            if len(data_in_child):
                # print(child[html_tag])
                output_list.append(reduce(lambda x, y: x + ' ' + y, data_in_child))  # to get 1 list item whatever number of items in data_in_child
        return output_list

    def build_output_dict(self, list_of_keys, list_of_values):
        my_dict = {}
        if len(list_of_keys) == len(list_of_values):
            for key in list_of_keys:
                my_dict[key] = list_of_values[list_of_keys.index(key)]
            return my_dict
        else:
            print('\n'+'-'*5)
            print('Warning, in webpage dict : list of keys provided is of different length that list of values provided')
            min_args = min(len(list_of_keys), len(list_of_values))
            for key in list_of_keys[0:min_args]:
                my_dict[key] = list_of_values[list_of_keys.index(key)]
            return my_dict

class Webpage_content_lbc(Webpage_content):
    """
        Instantiate a webpage_content for Le Bon Coin website.
        Gets attributes and methods from Webpage content.
    """
    output_dict_list_of_keys = []
    output_dict_list_of_values = []
    output_dict = {}


    def __init__(self, **kwargs):
        Webpage_content.__init__(self, **kwargs)
        my_html_list = self.get_all_matching_html_children()
        my_text = self.get_text_data(my_html_list)

        # specific to lbc website (depending of what is in my_text)
        self.output_dict_list_of_keys = ['Date', 'Vendeur']
        self.output_dict_list_of_values = []
        self.output_dict_list_of_keys.extend(my_text[2::2])
        self.output_dict_list_of_values = my_text[0:2]
        self.output_dict_list_of_values.extend(my_text[3::2])

        self.output_dict = self.build_output_dict(self.output_dict_list_of_keys, self.output_dict_list_of_values)



#--------------------
#TESTS
#--------------------
#my_url = 'https://www.leboncoin.fr/ventes_immobilieres/1097856199.htm?ca=12_s'
#my_tag_to_retrieve = 'class'
#args_html_subset_tags = ('section', {'class':'properties lineNegative'})
#kwargs_input = {'url': my_url, 'tag_to_retrieve': my_tag_to_retrieve, 'html_subset': args_html_subset_tags}

#kwargs_input_lbc = {'url': my_url, 'tag_to_retrieve': my_tag_to_retrieve, 'html_subset': args_html_subset_tags}
#my_webpage_lbc = Webpage_content_lbc(**kwargs_input_lbc)
#print(my_webpage_lbc.output_dict)

#my_webpage = Webpage_content(**kwargs_input)
#my_list = my_webpage.get_all_matching_html_children()
#my_text = my_webpage.get_text_data(my_list)
#print(my_text)
#import pdb; pdb.set_trace()
# define keys for output_dict
#OUTPUT_DICT_LIST_OF_KEYS = ['date_mise_en_ligne', 'vendeur']
#OUTPUT_DICT_LIST_OF_KEYS.extend(my_text[2::2])

# building of values to pass in output_dict and building output dict
#output_dict_list_of_values = my_text[0:2]
#output_dict_list_of_values.extend(my_text[3::2])

#output_dict = my_webpage.build_output_dict(OUTPUT_DICT_LIST_OF_KEYS, output_dict_list_of_values)
#print(output_dict)



