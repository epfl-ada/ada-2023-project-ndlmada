
import pandas as pd
import os
from urllib.parse import unquote
import numpy as np
from bs4 import BeautifulSoup # To Extract all the URLs from the HTML page
from IPython.display import display
import requests


def change_characters(dict_df, dataset_name, column_name):
    """ It replaces the %xx escapes with their single-character equivalent for all the value of a specified column.
    param:
        dict_df: dict
            dictionnary of dataframes
        dataset_name: str
            name of the dataset contain in dict_df
        column_name: str
            name of the column from which we want to replace the values
    return:
        dict_df: the provided dictionnary of dataframe with the replaced characters
     """
    dict_df[dataset_name][column_name] = [unquote(art) for art in dict_df[dataset_name][column_name]]
    return dict_df


def preprocessing():
    """ It downloads the dataset from wikispeedia paths-and-graph and applied the preprocessing
        return:
            dfs: a dictionary with the preprocessed dataset.
     """
    ## Download the data: 
    
    # Paths
    folder_path = "dataset/wikispeedia_paths-and-graph/"
    file_paths = ["paths_finished.tsv", "paths_unfinished.tsv", "categories.tsv", "articles.tsv", "links.tsv"]

    # Datasets: Names and their columns name
    data_frames_names = ["paths_finished", "paths_unfinished", "categories", "article", "links"]
    dfs_headers = [
        ["hashedIpAddress", "timestamp", "durationInSec", "path", "rating"],
        ["hashedIpAddress", "timestamp", "durationInSec", "path", "target", "type"],
        ["article", "category"],
        ["article"],
        ["linkSource", "linkTarget"]
    ]

    dfs_skiprows = [16, 17, 13, 12, 12]
    dfs = {}
    for i in range(len(file_paths)):
        dfs[data_frames_names[i]] = pd.read_csv(folder_path + file_paths[i], sep='\t', header=None, names=dfs_headers[i], skiprows=range(dfs_skiprows[i]))
    
    ## Preprocessing 
    dfs = change_characters(dfs, 'paths_finished', 'path')
    dfs['paths_finished'] = dfs['paths_finished'].drop(['hashedIpAddress', 'rating'], axis = 1)

    dfs = change_characters(dfs, 'paths_unfinished', 'path')
    dfs = change_characters(dfs, 'paths_unfinished', 'target')

    dfs = change_characters(dfs, 'categories', 'article')
    dfs = change_characters(dfs, 'categories', 'category')

    dfs = change_characters(dfs, 'article', 'article')

    dfs = change_characters(dfs, 'links', 'linkSource')
    dfs = change_characters(dfs, 'links', 'linkTarget')

    #Replace the returns (<) by the corresponding article the (sequence) of return leads to. The return article is higlighted by a . prefixe
    dfs['paths_finished'].path = [';'.join(replace_return(list_)) for list_ in dfs['paths_finished'].path.str.split(';')]
    dfs['paths_unfinished'].path = [';'.join(replace_return(list_)) for list_ in dfs['paths_unfinished'].path.str.split(';')]   

    return dfs


def extract_links(file_path):
    """It extracts all the links there are in the provided article. 
    param:
        file_path: str
            path to the article we want to access.
    return:
       filtered_links: list of str
            the list of all the hyperlink (only those link to another article) found in the provided article.
    """
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        soup = BeautifulSoup(file, 'html.parser')

        # Get all the hyperlinks
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # Remove all the links that are not taken into account in the game (those that are not link to another article)
        filtered_links = [link for link in links if '/images/' not in link and 
                                                    'disclaimer.htm' not in link and 
                                                    '/index/' not in link and 
                                                    '.htm' in link]

        return filtered_links 

def path_to_name(path):
    """ It selects the article name from its path.
    param: 
        path: str
    return: 
        name: str
            name of the article extract from the path
     """
    
    # Extract last path name of the source article
    name = os.path.basename(path)
    # Remove the extension
    name = os.path.splitext(name)[0]
    # Be sure name correctly expressed
    name = unquote(unquote(str(name)))
    
    return name

def dataset_info(dictionary, dataset_name):
    """ Display main information about a specified dataset from the given dictionary.
    params:
        dictionnary: dict
            A dictionary of dataframes.
        dataset_name: str 
            The name of the dataframe to be accessed in the dictionary
     """
    # Print the dataset name we are working on
    print('{}:'.format(dataset_name))

    df = dictionary[dataset_name]
    print('\tShape of the dataset: {}'.format(df.shape))
    

     # Check for NaN values in each column
    columns_with_nan = df.columns[df.isna().any()].tolist()

    # Print the columns with NaN values if they exsit
    if columns_with_nan == []:
        print('\tThe dataset has no column with NaN values.\n')
    else:
        print('\tThe dataset has {} columns with NaN values: {}\n'.format(len(columns_with_nan), columns_with_nan))
    
    # Provide statistical info 
    print('Visualisation of the first column and statistical infos:')
    display(df.head(1))
    display(df.describe(include='all'))
    df.info()

def get_gender_for_name(name):
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&search={name}"

    response = requests.get(url)
    data = response.json()

    if data["search"]:
        q_number = data["search"][0]["id"]

        # Use the Q number to get gender information
        gender_url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims&ids={q_number}"
        gender_response = requests.get(gender_url)
        gender_data = gender_response.json()

        # Extract gender information
        claims = gender_data["entities"][q_number]["claims"]
        if "P21" in claims:
            gender_id = claims["P21"][0]["mainsnak"]["datavalue"]["value"]["id"]
            
            # Male is Q6581097, Female is Q6581072
            if gender_id == "Q6581097":
                return "Male"
            elif gender_id == "Q6581072":
                return "Female"

    return "Unknown"


def add_all_genders(dataframe):

    # Iterate over the names and get genders
    #retrieve the names
    name_list = list(dataframe['article'])
    name_list = list(name.replace('_',' ') for name in name_list)
    gender_list = [get_gender_for_name(name) for name in name_list]
    dataframe['gender'] = gender_list
    return dataframe

def replace_return(path_list):
    """ In a given path, it replaces the return character (<) by the corresponding article name. 

    parameter:
        path_list: list of str
            list of path from one article to another, where the '<' character represent a return. 
    return: 
        the modified path_list that repace the returns by the corresponding articles with a prefix (.).
    """
    count = 0
    result_path_list = []
    history = [] # To add the right path when multiples > not in sequence

    l = len(path_list)
    for i in range(l):

        #Verify if the element of the list is an article or a return
        if (path_list[i] == '<') & (count == 0): 
            #Take into account the case of a sequence of <
            while(( i + count < l) and (path_list[i + count] == '<')):
                count += 1

            corresponding_return = history[-(count+1)]
            history = history[:-(count)]
            result_path_list.append('.' + corresponding_return) 
        
        elif path_list[i] != '<':
            count = 0
            result_path_list.append(path_list[i])
            history.append(path_list[i])
            
    return result_path_list