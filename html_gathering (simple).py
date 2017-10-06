# bot to automatically retrieve ads from "le bon coin"
import urllib.request
from bs4 import BeautifulSoup
from functools import reduce




def get_all_matching_children(input_list_html, my_tag):
    """
        Iterate over a given html and return a list with all smallest children matching a given tag.
        Finally return an output_list of all smallest htmls children.
    """
    temp_list = []
    available_children_in_list = False # to track existence of possible child within output_list

    for my_html in input_list_html:
        available_children_in_given_item = False # to track existence of possible child for a given item
        list_of_children = [item for item in my_html.children]
        for child in list_of_children:
            try:
                child[my_tag]
                temp_list.append(child)
                available_children_in_list = True
                available_children_in_given_item = True
            except (KeyError, TypeError):
                pass
        if not available_children_in_given_item: # if for a given item there is no possible child, keep original one in the list
            temp_list.append(my_html)

    if not available_children_in_list: # repeat operation until there are no remaining possible child
        return temp_list
    else:
        return get_all_matching_children(temp_list, my_tag)


def build_output_dict(list_of_keys, list_of_values):
    my_dict = {}
    if len(list_of_keys) == len(list_of_values):
        for key in list_of_keys:
            my_dict[key] = list_of_values[list_of_keys.index(key)]
        return my_dict
    else:
        raise ValueError('List of keys provided is of different length that list of values provided')


# gather html source code
my_url = 'https://www.leboncoin.fr/ventes_immobilieres/1097564814.htm?ca=12_s'
response = urllib.request.urlopen(my_url)
my_html = response.read()
soup = BeautifulSoup(my_html, "html5lib", from_encoding="ISO-8859-16")

# get html subset we want to get data from
my_html_subset = soup.find('section', {'class':'properties lineNegative'})
#print(my_html_subset.prettify())
LIST_OF_HTML_TAG_TO_RETRIEVE = ['class']


# iterate over tags
for html_tag in LIST_OF_HTML_TAG_TO_RETRIEVE:
    # get all html children where the tag can be found
    children_list = get_all_matching_children([my_html_subset], html_tag)

    # iterate over the children list and get data
    my_list = []
    for child in children_list:
        data_in_child = [i for i in child.stripped_strings]
        if len(data_in_child):
            #print(child[html_tag])
            my_list.append(reduce(lambda x,y: x+' '+y, data_in_child)) # to get 1 list item whatever number of items in data_in_child

    # define keys for output_dict
    OUTPUT_DICT_LIST_OF_KEYS = ['date_mise_en_ligne', 'vendeur']
    OUTPUT_DICT_LIST_OF_KEYS.extend(my_list[2::2])

    # building of values to pass in output_dict and building output dict
    output_dict_list_of_values = my_list[0:2]
    output_dict_list_of_values.extend(my_list[3::2])
    output_dict = build_output_dict(OUTPUT_DICT_LIST_OF_KEYS, output_dict_list_of_values)
    print(output_dict)