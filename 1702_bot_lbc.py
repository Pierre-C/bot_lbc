import os
import datetime
import operator
import re
import urllib.request

from bs4 import BeautifulSoup
from prettytable import PrettyTable

from _templates_classes.classes import Webpage_content_lbc
from _templates_classes.send_email import send_html_email


def find_matching_link(my_url, my_link_regex, my_output_list):
    """
        Get all items matching a given matching regex, and add it to a list passed as argument.
    """
    website = urllib.request.urlopen(my_url)
    html = website.read()
    links = my_link_regex.findall(html)
    my_output_list.extend(links)


def get_next_page_url(my_start_url, *args):
    """
        Look for html links included within a given html subset (the button) passed in *args
        Here, used to get html link associated to the "next page" button (the subset).
    """
    try:
        website = urllib.request.urlopen(my_start_url)
        my_html = website.read()
        soup = BeautifulSoup(my_html, "html5lib", from_encoding="ISO-8859-16")
        my_html_subset = soup.find(*args)
        new_url = my_html_subset.find('a', {'id':'next'}).get('href')
        return new_url
    except (KeyError, AttributeError):
        print("No further page to be found")
        return  False


def match_criteria_string(input_dict, my_criteria, my_target_string, start_with = False):
    """
        Check if my_target_string is in input_dict[my_criteria]. If yes return True else return False
    """
    if start_with == False:
        try:
            if my_target_string in input_dict[my_criteria]:
                return True
            else:
                return False
        except KeyError:
            return False
    else:
        try:
            if input_dict[my_criteria].startswith(my_target_string):
                return True
            else:
                return False
        except KeyError:
            return False


def match_criteria_int(input_dict, my_criteria,  my_target_int, comparison = '<='):
    """
        Check if my_criteria is below or equal my_target_int. If yes return True else return False.
        NB: specific to website.
    """
    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '=': operator.eq}
    try:
        # converting dict value to int for comparison
        my_int = [letter for letter in input_dict[my_criteria] if is_integer(letter)]
        my_int = int(''.join(letter for letter in my_int))
        if ops[comparison](my_int, my_target_int):
            return True
        else:
            return False
    except KeyError:
        return False


def is_integer(my_string):
    """
        Check if a string passed as an input is an integer
    """
    try:
        int(my_string)
        return True
    except ValueError:
        return False



# set up
MY_START_URL = 'https://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/?th=1&location=Bordeaux'
MY_LINK_REGEX = re.compile(b'www.leboncoin.fr/ventes_immobilieres/[\d]+[.\w\d\?\=]*')
HTML_TAG_TO_RETRIEVE = 'class'
ARGS_HTML_SUBST_TAGS = ('section', {'class':'properties lineNegative'})

# filtering criterias
CITY_CRITERIA = 'Bordeaux'
PRICE_CRITERIA = 200000
PIECES_CRITERIA = 2
NB_LINKS_TO_RETRIEVE = 5 # get last x ads matching criterias

# email criterias
TO_ADDR = 'constant.pierre@gmail.com'
CC_ADDR = None
SUBJECT = 'bot_lbc'+datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
HTML_TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), '_templates_classes', 'email_template.html')


# start
my_url = MY_START_URL

if __name__ == '__main__':

# while target nb returned is not matched
    matched_links = []
    output_tables = []
    output_descriptions = []
 # from mainpage
    while True:

         # get list links for ads
        list_of_links = []
        find_matching_link(my_url, MY_LINK_REGEX, list_of_links)
        list_of_links = [link.decode("ISO-8859-16") for link in list_of_links] # list contains byte strings*
        list_of_links = ['https://'+link for link in list_of_links]

        # loop over ads, and get dictionnary
        for link in list_of_links:
            kwargs_input_lbc = {'url': link, 'tag_to_retrieve': HTML_TAG_TO_RETRIEVE, 'html_subset': ARGS_HTML_SUBST_TAGS}
            my_webpage_lbc = Webpage_content_lbc(**kwargs_input_lbc)
            ad_dict = my_webpage_lbc.output_dict

            # match dictionnary against criteria
            if match_criteria_string(ad_dict, 'Ville', CITY_CRITERIA, True) and \
                    match_criteria_int(ad_dict, 'Pièces', 2, ">=") and \
                    match_criteria_int(ad_dict, 'Prix', PRICE_CRITERIA, "<="):

                # print table
                print('\n')
                my_table = PrettyTable()
                my_table.field_names= ["Key", "Value"]
                list_attributes = [item for item in ad_dict.items()]
                for item in list_attributes[:-1]: # to exclude description, to long to be sent by email
                    my_table.add_row(item)
                my_table.add_row(["URL", link])
                my_table.align = "l"
                output_tables.append(my_table)
                output_descriptions.append(list_attributes[-1:][0][1]) # get description value only
                print(my_table)
                print(list_attributes[-1:])

                # append relevant link and check if target number is reached
                matched_links.append(link)
                if len(matched_links) == NB_LINKS_TO_RETRIEVE:
                    main_message = ''
                    for table in output_tables:
                        main_message = main_message + ''.join(table.get_html_string())
                        main_message = main_message + '<br>' + '<p>' + '<b>'+'Description :'+'</b>'+'</p>'
                        main_message = main_message + '<p>' + ''.join(output_descriptions[output_tables.index(table)])+'</p>'
                        main_message = main_message + '<br>'*2 + '<hr>'


                    send_html_email(TO_ADDR,
                                    SUBJECT+' | '+datetime.datetime.now().strftime("%d %B %y - %H:%M"),
                                    HTML_TEMPLATE,
                                    main_message,
                                    CC_ADDR)
                    exit()


        # move to next mainpage if target number of ads not reached
        my_url = 'https:' + get_next_page_url(my_url, 'footer', {'class': 'pagination clearfix'})

