
import os
from urllib.parse import unquote
import numpy as np
from bs4 import BeautifulSoup # To Extract all the URLs from the HTML page


def change_characters(dict_df, dataset_name, column_name):
    """ It replaces the %xx escapes with their single-character equivalent for all the value of a specified column.
    param:
        dict_df: dictionnary of dataframes
        dataset_name: str, name of the dataset contain in dict_df
        column_name: str, name of the column from which we want to replace the values
    return:
        dict_df: the provided dictionnary of dataframe with the replaced characters
     """
    dict_df[dataset_name][column_name] = [unquote(art) for art in dict_df[dataset_name][column_name]]
    return dict_df

def extract_links(file_path):
    """It extracts all the links there is in the provided article. 
    param:
        file_path: str, path to the article we want to access.
    return:
       filtered_links: list of str, the list of all the hyperlink (only those link to another article) found in the provided article.
    """
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        soup = BeautifulSoup(file, 'html.parser')

        # Get all the hyperlinks
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # Remove all the links that are not taken into account in the game (those that are not link to another article)
        filtered_links = [link for link in links if '/images/' not in link and 
                                                    'disclaimer.htm' not in link and 
                                                    'index' not in link and 
                                                    '.htm' in link]

        return filtered_links 

def path_to_name(path):
    """ It selects the article name from its path.
    param: 
        path: str
    return: 
        name: str, name of the article extract from the path
     """
    
    # Extract last path name of the source article
    name = os.path.basename(path)
    # Remove the extension
    name = os.path.splitext(name)[0]
    # Be sure name correctly expressed
    name = unquote(unquote(str(name)))
    
    return name
