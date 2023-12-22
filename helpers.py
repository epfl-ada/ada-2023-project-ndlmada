
import pandas as pd
import os
from urllib.parse import unquote
import numpy as np
from bs4 import BeautifulSoup # To Extract all the URLs from the HTML page
from IPython.display import display
import requests
import csv
import networkx as nx
import math
import matplotlib.pyplot as plt



def change_characters(dict_df, dataset_name, column_name):
    """ It replaces the %xx escapes with their single-character equivalent for all the value of a specified column.
    param:
        dict_df: dict
            dictionary of dataframes
        dataset_name: str
            name of the dataset contain in dict_df
        column_name: str
            name of the column from which we want to replace the values
    return:
        dict_df: the provided dictionary of dataframe with the replaced characters
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
        dictionary: dict
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


    # Function to create the dictionary from a TSV file
def create_dictionary_from_tsv(file_path):
    """  Creates a dictionary from a TSV file
    parameter:
        file_path: str
            path to the TSV file
    return:
        all_article: list of str
            name of each articles added as key
        data_dict: dictionary
            article name as key and 3 first subject as values
    """
    data_dict = {}

    with open(file_path, 'r', newline='', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        
        all_articles = []
        for row in reader:
            if len(row) == 2:
                article, subjects = row
                subjects_list = subjects.split('.')
                article = unquote(article)
                all_articles.append(article)

                data_dict[article] = {
                    'main_subject': unquote(subjects_list[1]) if len(subjects_list) >= 2 else None,
                    'secondary_subject': unquote(subjects_list[2]) if len(subjects_list) >= 3 else None,
                    'tertiary_subject': unquote(subjects_list[3]) if len(subjects_list) >= 4 else None
                }

    return data_dict, all_articles


def create_dictionary_from_tsv_graph(file_path):
    data_dict = {}
    G = nx.DiGraph()
    with open(file_path, 'r', newline='', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        
        all_articles = []
        for row in reader:
            if len(row) == 2:
                article, subjects = row
                subjects_list = subjects.split('.')
                for i in range(len(subjects_list)-1):
                    G.add_edge(unquote(subjects_list[i]), unquote(subjects_list[i+1]))
                

                article = unquote(article)
                all_articles.append(article)

                data_dict[article] = {
                    'main_subject': unquote(subjects_list[1]) if len(subjects_list) >= 2 else None,
                    'secondary_subject': unquote(subjects_list[2]) if len(subjects_list) >= 3 else None,
                    'tertiary_subject': unquote(subjects_list[3]) if len(subjects_list) >= 4 else None
                }
    G.remove_edges_from(nx.selfloop_edges(G))
    
    return data_dict, all_articles, G



def get_dict_from_list(path_list):
    # transform a dict with path list into a dictionary with the following items 
        # the path list
        # the path list but with only paths longer than one
        # N0, N1, N2, N3, dataframe containing the number of articles in each category at time step N, N-1, N-2, N-3

    N0 = pd.DataFrame({'category':[path[-1] for path in path_list if len(path)>0]}).value_counts().to_frame().reset_index()
    N1 = pd.DataFrame({'category':[path[-2] for path in path_list if len(path)>1]}).value_counts().to_frame().reset_index()
    N2 = pd.DataFrame({'category':[path[-3] for path in path_list if len(path)>2]}).value_counts().to_frame().reset_index()
    N3 = pd.DataFrame({'category':[path[-4] for path in path_list if len(path)>3]}).value_counts().to_frame().reset_index()
    long_paths = [path for path in path_list if len(path) > 1]

    return {'list':path_list, 'long_path_list': long_paths, 'N0': N0, 'N1': N1, 'N2': N2, 'N3': N3}

def update_dict_with_counts(path_dict):
    # update a dict with path lists from each category with the counts at each step 

    new_path_dict = {}
    for cat in path_dict.keys():
        new_path_dict[cat] = get_dict_from_list(path_dict[cat])
    return new_path_dict

def replace_to_simple(path):
    # replace a path with complete categories to a path of principal categories

    new_path = []
    for i in range (len(path)):#-1) :
        new_path.append(path[i].split('.')[0])
    return new_path

def create_dict_for_plotly_bar(new_path_dict):
    #combines the data into a single dataframe to use with plotly
    
    N0_N1 = pd.merge(new_path_dict['N0'], new_path_dict['N1'], on = 'category', how = 'outer', suffixes = ('_N0', '_N1')).fillna(0)
    N2_N3 = pd.merge(new_path_dict['N2'], new_path_dict['N3'], on = 'category', how = 'outer', suffixes = ('_N2', '_N3')).fillna(0)
    final = pd.merge(N0_N1, N2_N3, on = 'category', how = 'outer').fillna(0)
    return final

def transform_path_main_category(path, dict_article_target):
    split_path = path.split(';')
    split_cat = []
    for art in split_path:
         if art[0] != '.' : 
            try: art in dict_article_target.keys()
            except IndexError : print('Warning: not valid article:', art)
            if art in dict_article_target.keys():
                split_cat.append(dict_article_target[art]['main_subject'])
    
    return split_cat


def transform_path(categories,path):
    split_path = path.split(';')
    split_cat = []
    for art in split_path:
        if art != '<' : 
            try: split_cat.append(categories.loc[categories['article'] == art, 'category'].iloc[0].replace('subject.', ''))
            except IndexError : pass
    return split_cat


def create_graph_Gender(path_finished_dfs, path_unfinished_dfs, gender_dict, target_gender: str, last_node_from_path: bool = False, both_gender = False):
    """
    Creates a graph of all the paths where the gender of the target node is equal to target_gender. 
    If Both_gender is True, creates a graph of the paths where a Male or a Female is the target node. 

    Args:
        path_finished_dfs (dataframe): dataframe of the finished paths
        path_unfinished_dfs (dataframe): dataframe of the unfinished paths
        gender_dict (dict): dict of the gender of the nodes 
        target_gender (str): gender of the taget node 
        last_node_from_path (bool, optional): If True, the target node is the created grap. Defaults to False.
        both_gender (bool): If true, both gender are added to the graph. Defaults to False.

    Returns:
        G (graph): graph of the paths
        endnode_names (list): list of the names of the target nodes, this lists contains repetitions if the target node is the same in multiple paths
    
    """    

    G = nx.DiGraph()
    endnode_names = []
    indexing_correction = 1 if last_node_from_path else 0
    

    for index, row in path_finished_dfs.iterrows():

        path = row['path'].split(';')

        try: 
            gender_last = gender_dict[path[-1]]
        except KeyError as e:
            #print("KeyError for ", e)
            continue
        
        # The isinstace is required otherwise math.isnan(gender_last) will throw an error
        if isinstance(gender_last, float) and math.isnan(gender_last):
            continue

        # If it is the good gender we add the entire path to the graph
        if gender_last == target_gender or (both_gender and (gender_last == "Male" or gender_last == "Female")):
            endnode_names.append(path[-1])
            
            # Add the path to the graph or adds 1 to the weight if the edge already exists
            for i in range(len(path)-1 -indexing_correction):
                
                # The "."" at the beggining is a marker of going back to this page, we don't want to add the backlink
                if path[i+1][0] == '.': 
                    continue
                
                # Remove the "." at the beggining of the node name, this is ok since itterows gives a copy of the dataframe
                if path[i][0] == ".":
                    path[i] = path[i][1:]

                if G.has_edge(path[i], path[i+1]):
                    G[path[i]][path[i+1]]['weight'] += 1
                else:
                    G.add_edge(path[i], path[i+1], weight=1)

    for index, row in path_unfinished_dfs.iterrows():

        path = row['path'].split(';')

        try: 
            gender_last = gender_dict[row["target"]]
        except KeyError as e:
            #print("KeyError for ", e)
            continue

        if isinstance(gender_last, float) and math.isnan(gender_last):
            continue
        
        if gender_last == target_gender or (both_gender and (gender_last == "Male" or gender_last == "Female")):
            endnode_names.append(row["target"])
            
            for i in range(len(path) -1 -indexing_correction):

                # The "."" at the beggining is a marker of going back to this page, we don't want to add the backlink
                if path[i+1][0] == '.': 
                    continue
                
                # Remove the "." at the beggining of the node name, this is ok since itterows gives a copy of the dataframe
                if path[i][0] == ".":
                    path[i] = path[i][1:]

                if G.has_edge(path[i], path[i+1]):
                    G[path[i]][path[i+1]]['weight'] += 1
                else:
                    G.add_edge(path[i], path[i+1], weight=1)

    return G, endnode_names

def get_df_pagerank(graph):
    """
    Returns a dataframe with the PageRank of each node

    Args:
        graph (graph): graph of the paths
    
    Returns:
        df_pagerank (dataframe): dataframe with the PageRank of each node, columns are "Node" and "PageRank"
    """
    
    pagerank = nx.pagerank(graph)
    df_pagerank = pd.DataFrame(list(pagerank.items()), columns=['Node', 'PageRank'])

    return df_pagerank

def sort_and_rank(df_pagerank):
    """
    Sort the dataframe by PageRank and add a column with the rank

    Args:
        df_pagerank (dataframe): dataframe with the PageRank of each node
    
    Returns:
        df_pagerank (dataframe): dataframe with the PageRank of each node sorted and ranked
    """
    df_pagerank.sort_values(by=['PageRank'], ascending=False, inplace=True)
    df_pagerank["Rank"] = df_pagerank["PageRank"].rank(ascending=False, method="first")

    return df_pagerank

def get_diff2(x, df_ranking_after):
    try:   
        second_rank = df_ranking_after.loc[x.name, "Rank"]
        return x["Rank"] - second_rank
    except KeyError as e:
        return np.nan

def compare_rankings2(df_pagerank_before: pd.DataFrame, df_pagerank_after: pd.DataFrame):
    """
    Keeps the keys of df_ranking_before and add the diff between the two rankings
    """
    # ça aurait été cool mais ils on pas toujours les mêmes index car les même nodes sont pas toujours là entre les links et les paths
    # De base en plus ils ont pas les même indices mais même si on avit pus résoudre ce soucis c'est la merde
    #df_diff = df_ranking_before.sort_index()["Rank"] - df_ranking_after.sort_index()["Rank"]

    df_pagerank_before = df_pagerank_before.set_index("Node")
    df_pagerank_after = df_pagerank_after.set_index("Node")

    # Removes the nodes that are in the first ranking but not in the second
    index_difference = df_pagerank_before.index.difference(df_pagerank_after.index, sort=False)
    df_pagerank_before = df_pagerank_before.drop(index_difference)

    # Removes the nodes that are in the second ranking but not in the first
    index_difference = df_pagerank_after.index.difference(df_pagerank_before.index, sort=False)
    df_pagerank_after = df_pagerank_after.drop(index_difference)

    df_ranking_before = sort_and_rank(df_pagerank_before)
    df_ranking_after = sort_and_rank(df_pagerank_after)

    # Calculates the difference between the two rankings
    df_diff = df_ranking_before.apply(lambda x: get_diff2(x, df_ranking_after), axis=1)

    df_out = pd.concat([df_ranking_before, df_diff], axis=1)

    df_out.columns = ["PageRank", "Rank", "Diff"]

    df_out = df_out.merge(df_ranking_after, left_index= True, right_index= True, how="inner", suffixes=("_before", "_after"))

    return df_out

def graph_category_rank(df_rank, all_cat):
    fig, axes = plt.subplots(5, 3, figsize=(20, 25), sharex=True, sharey=True)
    colors = plt.cm.tab20(range(20))

    for i in range(5):
        for j in range(3):
            category = all_cat[3*i+j]
            df_subset_cat = df_rank.loc[df_rank["MainCat"] == category, :]
            axes[i, j].hist(df_subset_cat["Rank"], bins=100, alpha=0.5, label=category, color=colors[3*i+j], density=True)
            axes[i, j].set_title(category)
            axes[i, j].axvline(df_subset_cat["Rank"].median(), color="Black", linestyle='dashed', linewidth=1, alpha=0.75, label='Median')
            axes[i, j].set_xlabel("Rank")
            axes[i, j].set_ylabel("Number of nodes normalized")

def get_cat(Node, result_dict):
    try:
        return result_dict[Node]["main_subject"]
    except KeyError as e:
        return np.nan
    
def create_graph_links(dfs_links):
    G = nx.DiGraph()
    for index, row in dfs_links.iterrows():
        if G.has_edge(row['linkSource'], row['linkTarget']):
            G[row['linkSource']][row['linkTarget']]['weight'] += 1
        else:
            G.add_edge(row['linkSource'], row['linkTarget'])
    return G

def create_graph_Gender_n_last(path_finished_dfs, path_unfinished_dfs, gender_dict, target_gender: str, last_node_from_path: bool = False, both_gender = False, n=3):
    """
    Creates a graph of all the paths where the gender of the target node is equal to target_gender. 
    If Both_gender is True, creates a graph of the paths where a Male or a Female is the target node. 

    Args:
        path_finished_dfs (dataframe): dataframe of the finished paths
        path_unfinished_dfs (dataframe): dataframe of the unfinished paths
        gender_dict (dict): dict of the gender of the nodes 
        target_gender (str): gender of the taget node 
        last_node_from_path (bool, optional): If True, the target node is the created grap. Defaults to False.
        both_gender (bool): If true, both gender are added to the graph. Defaults to False.

    Returns:
        G (graph): graph of the paths
        endnode_names (list): list of the names of the target nodes, this lists contains repetitions if the target node is the same in multiple paths
    
    """    

    G = nx.DiGraph()
    endnode_names = []
    indexing_correction = 1 if last_node_from_path else 0
    

    for index, row in path_finished_dfs.iterrows():

        path = row['path'].split(';')

        try: 
            gender_last = gender_dict[path[-1]]
        except KeyError as e:
            # BEACOUP DE KEY ERROR TODO !!
            #print("KeyError for ", e)
            continue
        
        # The isinstace is required otherwise math.isnan(gender_last) will throw an error
        if isinstance(gender_last, float) and math.isnan(gender_last):
            continue
        
        # If it is the good gender we add the entire path to the graph
        if gender_last == target_gender or (both_gender and (gender_last == "Male" or gender_last == "Female")):
            endnode_names.append(path[-1])
            
            edges_to_add = []
            # Add the path to the graph or adds 1 to the weight if the edge already exists
            for i in range(len(path)-1 -indexing_correction):
                
                # The "."" at the beggining is a marker of going back to this page, we don't want to add the backlink
                if path[i+1][0] == '.': 
                    continue
                
                # Remove the "." at the beggining of the node name, this is ok since itterows gives a copy of the dataframe
                if path[i][0] == ".":
                    path[i] = path[i][1:]
                
                edges_to_add.append((path[i], path[i+1]))
        
            # We add only the last n edges of the path to the graph
            starting_index = len(edges_to_add)-1
            for i in range(starting_index, max(starting_index-n, -1), -1):
                tuple_to_add = edges_to_add[i]

                if G.has_edge(tuple_to_add[0], tuple_to_add[1]):
                    G[tuple_to_add[0]][tuple_to_add[1]]['weight'] += 1
                else:
                    G.add_edge(tuple_to_add[0], tuple_to_add[1], weight=1)

    return G, endnode_names


def get_median_rank_per_cat(df, all_cat):
    data = {}
    for cat in all_cat:
        data[cat] = df.loc[df["MainCat"] == cat, "Rank"].median()

    df_out = pd.DataFrame(list(data.items()), columns=['MainCat', 'MedianRank']).set_index("MainCat")
    
    return df_out