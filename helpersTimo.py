import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import random
import math


def iter_and_add_to_graph(G, df, index_correction=0):
    for index, row in df.iterrows():
        path = row['path'].split(';')

        for i in range(len(path)-1-index_correction):
            if G.has_edge(path[i], path[i+1]):
                G[path[i]][path[i+1]]['weight'] += 1
            else:
                G.add_edge(path[i], path[i+1], weight=1)
    return G

def create_graph_path(dfs):
    """
    Makes a graph of all the paths in the dataset

    Args:
        dfs (dict): dictionnary of dataframes
    
    Returns:
        G (graph): graph of the paths
    """

    G = nx.DiGraph()
    G = iter_and_add_to_graph(G, dfs['paths_unfinished'])
    # We put an index correction of 1 because we don't want to count the last article of the path since it is the target
    G = iter_and_add_to_graph(G, dfs['paths_finished'], 1)

    return G

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

def get_diff(x, df_ranking_after):
    second_rank = df_ranking_after.loc[df_ranking_after["Node"] == x["Node"]]

    if second_rank.empty:
        return -np.inf
    else:
        return x["Rank"] - second_rank["Rank"].values[0]

def graph_bigest(G: nx.graph, df_pagerank: pd.DataFrame, n = 100):
    # Plots the 100 biggest nodes by PageRank

    df_pagerank.sort_values(by=['PageRank'], ascending=False, inplace=True)

    top_100_nodes = df_pagerank.head(n)['Node'].tolist()

    subgraph = G.subgraph(top_100_nodes)

    #pos = nx.drawing.nx_agraph.graphviz_layout(subgraph)
    pos = nx.spring_layout(subgraph)
    fig, axes = plt.subplots(1, 1, figsize=(20, 10))

    edge_colors = [(0, 0, 0, 0.05) for _ in subgraph.edges()]

    nx.draw(subgraph, pos, with_labels=True, cmap=plt.cm.Reds, node_color="c", node_size=80, font_size=6, font_color= "black", ax=axes,linewidths = 0.5, arrowsize=2, edge_color= edge_colors)

    # Show the plot
    plt.show()


def is_equal_i(rank, i):
    if np.isnan(rank):
        return False
    else:
        return rank == i


def compare_rankings(df_ranking_before: pd.DataFrame, df_ranking_after: pd.DataFrame, replace_rank = np.nan, delete_nan = False):
    """
    Keeps the keys of df_ranking_before and add the diff between the two rankings
    """
    # ça aurait été cool mais ils on pas toujours les mêmes index car les même nodes sont pas toujours là entre les links et les paths
    # De base en plus ils ont pas les même indices mais même si on avit pus résoudre ce soucis c'est la merde
    #df_diff = df_ranking_before.sort_index()["Rank"] - df_ranking_after.sort_index()["Rank"]

    df_diff = df_ranking_before.apply(lambda x: get_diff(x, df_ranking_after), axis=1)

    df_out = pd.concat([df_ranking_before, df_diff], axis=1)

    df_out.columns = ["Node", "PageRank", "Rank", "Diff"]

    df_out = df_out.merge(df_ranking_after, on="Node", how="left", suffixes=("_before", "_after"))

    if not np.isnan(replace_rank): 
        df_out["Rank_after"] = df_out["Rank_after"].fillna(replace_rank)
        
        mask = df_out["Diff"] == -np.inf
        
        df_out["Diff"] = df_out["Diff"].replace(-np.inf, np.nan)
        df_out["Diff"] = df_out["Diff"].fillna(df_out.loc[mask, "Rank_before"] - replace_rank)
    
    all_absent_node = []
    df_ranking_after.apply(lambda row: all_absent_node.append(row["Node"]) if row["Node"] not in df_out["Node"].values else None, axis=1)

    for node in all_absent_node:
        #df_out = df_out.append({"Node": node, "PageRank_before": np.nan, "Rank_before": np.nan, "Diff": np.inf, "PageRank_after": df_ranking_after.loc[df_ranking_after["Node"] == node]["PageRank"].values[0], "Rank_after": df_ranking_after.loc[df_ranking_after["Node"] == node]["Rank"].values[0]}, ignore_index=True)
        try:
            rank_after = df_ranking_after.loc[df_ranking_after["Node"] == node]["Rank"].values[0]
        except IndexError as e:
            print("ERROR, the node is not in the second ranking")
            print(node, df_ranking_after.loc[df_ranking_after["Node"] == node].values)

        new_row = pd.DataFrame({"Node": [node],
                         "PageRank_before": [np.nan],
                         "Rank_before": [replace_rank],
                         "Diff": [np.inf if np.isnan(replace_rank) else replace_rank - rank_after],
                         "PageRank_after": df_ranking_after.loc[df_ranking_after["Node"] == node]["PageRank"].values,
                         "Rank_after": rank_after})
        
        df_out = pd.concat([df_out, new_row], ignore_index=True)
    
    if delete_nan:
        df_out = df_out.dropna()

    return df_out


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


def get_color_from_gender(Node_name, dfs):
    """
    Returns a color depending on the gender of the node, if it has no gender returns black
    If there is an error, returns green

    """

    df_gender = dfs["article"]

    gender = df_gender.loc[df_gender["article"] == Node_name, "gender"]

    if len(gender.values) == 0:
        return (0, 1, 0)
    else:
        gender = gender.values[0]
    
    if gender == "Male":
        return (0, 0, 1)
    elif gender == "Female":
        return (1, 0, 0)
    else:
        return (0, 0, 0)

## MMM BOF PROBLEMES chiant 
def get_color_from_category(Node_name, dfs):
    """
    Returns a color depending on the category of the node
    If there is an error, returns green

    """

    df_category = dfs["categories"]

    category = df_category.loc[df_category["article"] == Node_name, "category"]

    if len(category.values) == 0:
        return (0, 1, 0)
    else: 
        category_string = category.values[0]
        # we have something like "subject.xxx.yyy.zzz" and we want to extract the "xxx"
        category = category_string.split(".")[1]
        
    if category == "People":
        return (0, 0, 1)
    else:
        return (0, 0, 0)
    
def get_color_for_people(Node_name, dfs):
    """
    Returns a color depending on if the node is a person or not
    If there is an error, returns green
    """
    df_gender = dfs["article"]

    gender = df_gender.loc[df_gender["article"] == Node_name, "gender"]

    if len(gender.values) == 0:
        return (0, 1, 0)
    else:
        gender = gender.values[0]
    
    if gender == "Male" or gender == "Female":
        return (0, 0, 1)
    else:
        return (0, 0, 0)



def plot_ranks_diff(df_pagerank_before: pd.DataFrame, df_pagerank_after: pd.DataFrame, dfs, color_choice: str, n = 100, height = None, limit = np.nan):
    """
    We graph the changes in the biggest rank of the 100 important nodes in the graph 
    We plot the rank before and after and the difference between the two
    The n biggest node before and the n biggest node after are all plotted and thier rank is shown so there is more that n nodes on the graph


    """
    if height is None:
        height = n*60/100

    fig, axes = plt.subplots(1, 1, figsize=(15, height))



    df_diff = compare_rankings(df_pagerank_before, df_pagerank_after, replace_rank=limit)

    # Takes a subset of the firts n nodes of the dataframe
    df_diff_sub = df_diff.loc[:n, :]

    # We add the missing nodes that are in the second top n ranking but not in the first one
    for i in range(1,n):
        all_nodes = []
        df_diff.apply(lambda row: all_nodes.append(row["Node"]) if is_equal_i(row["Rank_after"], i) else None, axis=1)

        if len(all_nodes) > 1:
            print("ERROR, there is more than one node with the same Rank_after")
        else:
            node = all_nodes[0]

        if node not in df_diff_sub["Node"].values:
            df_diff_sub = pd.concat([df_diff_sub, df_diff.loc[df_diff["Node"] == node]], ignore_index=True)
    


    # Replace the -inf and +inf in the diff by the max + 1 rank so that the node is at the bottom of the graph
    #inf_nodes = df_diff_sub.loc[df_diff_sub["Diff"] == -np.inf]

    max_rank = max(df_diff_sub["Rank_after"].max(), df_diff_sub["Rank_before"].max()) if np.isnan(limit) else limit

    df_diff_sub.loc[df_diff_sub["Diff"]== -np.inf, "Rank_after"] = max_rank
    df_diff_sub.loc[df_diff_sub["Diff"]== np.inf, "Rank_before"] = max_rank    

    # If the value of y is too big, we put it at the bottom of the graph
    if not np.isnan(limit):
        df_diff_sub.loc[df_diff_sub["Rank_after"] > limit, "Rank_after"] = max_rank 
        df_diff_sub.loc[df_diff_sub["Rank_before"] > limit, "Rank_before"] = max_rank

    # Some of the rank after are duplicated, so we have to change them
    duplicate_rows = df_diff_sub[df_diff_sub.duplicated(subset='Rank_after', keep=False)]
    df_diff_sub.loc[duplicate_rows.index, 'Rank_after'] = range(len(duplicate_rows)) + duplicate_rows['Rank_after']

    duplicate_rows = df_diff_sub[df_diff_sub.duplicated(subset='Rank_before', keep=False)]
    df_diff_sub.loc[duplicate_rows.index, 'Rank_before'] = range(len(duplicate_rows)) + duplicate_rows['Rank_before']
    
    
    
    # Adds a color depending on the color_choice
    colors = []
    if color_choice == "gender":
        df_diff_sub.apply(lambda row: colors.append(get_color_from_gender(row["Node"], dfs)), axis=1)
    elif color_choice == "random":
        df_diff_sub.insert(loc = len(df_diff_sub.columns), column="Color", value=[(round(random.uniform(0, 1), 2), round(random.uniform(0, 1), 2), round(random.uniform(0, 1), 2)) for _ in range(len(df_diff_sub))])
    elif color_choice == "category":
        df_diff_sub.apply(lambda row: colors.append(get_color_from_category(row["Node"], dfs)), axis=1)
    elif color_choice == "people":
        df_diff_sub.apply(lambda row: colors.append(get_color_for_people(row["Node"], dfs)), axis=1)

    df_diff_sub.insert(loc = len(df_diff_sub.columns), column="Color", value=colors)

    # Set the x and y values
    x_before = 1
    x_after = 3

    y_before = df_diff_sub["Rank_before"].values
    y_after = df_diff_sub["Rank_after"].values

    # Plot the points
    axes.scatter([x_before for _ in y_before], y_before, c=df_diff_sub["Color"].to_list(), label="Before")
    axes.scatter([x_after for _ in y_after], y_after, c=df_diff_sub["Color"].to_list(), label="After")

    # Adds a annotation next to each point with the node name
    # ha = horizontal alignment, aligns the text with the point
    # va = center, center the text vertically in the point
    # textcoords = offset points, offset the text from the point
    df_diff_sub.apply(lambda row: axes.annotate(row["Node"], (x_before, row["Rank_before"]), xytext=(-15, 0), textcoords='offset fontsize', va='center'), axis=1)
    df_diff_sub.apply(lambda row: axes.annotate(row["Node"], (x_after, row["Rank_after"]), xytext=(+7, 0), textcoords='offset fontsize', va='center'), axis=1)

    # Adds a line between the two points of the same node 
    df_diff_sub.apply(lambda row: axes.plot([x_before, x_after], [row["Rank_before"], row["Rank_after"]], c=row["Color"], alpha=0.5), axis=1)

    # This could maybe replace the annotated above, but then you don't have any number left
    #plt.yticks(range(1, n+2), df_diff_sub["Node"].to_list())

    # Set the labels on both size since the graph is big 
    axes.tick_params(labelbottom=True, labeltop=True, labelleft=True, labelright=True,
                     bottom=True, top=True, left=True, right=True)

    # Set nice ticks for readability
    axes.set_xticks([x_before, x_after], ["Before", "After"])
    axes.yaxis.set_major_locator(MultipleLocator(10))
    axes.yaxis.set_minor_locator(MultipleLocator(1))
    axes.set_ylim(0, max(df_diff_sub["Rank_after"].max(), df_diff_sub["Rank_before"].max())  + 1)


    # Set the ticks on both size since the graph is big
    axes.yaxis.set_ticks_position('both')
    axes.xaxis.set_ticks_position('both')
    
    
    # Reverts the y axis so that the biggest Rank is on top
    fig.gca().invert_yaxis()



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
            # BEACOUP DE KEY ERROR TODO !!
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


def mean_median_change_in_rank_of_peoples(df_pagerank_before, df_pagerank_after, gender_dict):
    """
    Returns the mean and median of the change in rank of the nodes that are people or not and graphs the distribution of the change in rank

    Args:
        df_pagerank_before (dataframe): dataframe with the PageRank of each node in the fisrt ranking
        df_pagerank_after (dataframe): dataframe with the PageRank of each node in the second ranking
        gender_dict (dict): Dictionary of the genders of the nodes
    
    Returns:
        mean_people (float): mean of the change in rank of the people
        median_people (float): median of the change in rank of the people
        mean_not_people (float): mean of the change in rank of the not people
        median_not_people (float): median of the change in rank of the not people

    """
    df_diff = compare_rankings2(df_pagerank_before, df_pagerank_after)

    desired_genders = ['Male', 'Female']

    # Use the map function to map nodes to their genders
    df_diff['node_gender'] = df_diff.index.map(gender_dict)

    #Filter rows based on the desired genders
    df_diff_subset_people = df_diff[df_diff['node_gender'].isin(desired_genders)]

    df_diff_subset_not_people = df_diff[~df_diff['node_gender'].isin(desired_genders)]
    

    # plot the diff of the df_diff_subset_people
    fig, axes = plt.subplots(1, 1, figsize=(15, 10))
    axes.hist(df_diff_subset_not_people["Diff"], bins=100, alpha=0.5, label='Not people', color="#B80C09", density=True)
    axes.hist(df_diff_subset_people["Diff"], bins=100, alpha=0.5, label='People', color="#01BAEF", density=True)

    axes.axvline(df_diff_subset_people["Diff"].median(), color='blue', linestyle='dashed', linewidth=1, alpha=0.5, label='Median')
    axes.axvline(df_diff_subset_not_people["Diff"].median(), color='red', linestyle='dashed', linewidth=1, alpha=0.5, label='Median not people')
    axes.legend()
    axes.set_title("Difference of the rank between the two rankings")
    axes.set_xlabel("Difference of the rank")
    axes.set_ylabel("Number of nodes")
    axes.grid(True)
    axes.text(100, 0.00075, 'Better ranked after', bbox = {'facecolor': 'oldlace', 'alpha': 0.5, 'boxstyle': "rarrow, pad=0.3", 'ec': 'green'})
    axes.text(-100, 0.00075, 'Better ranked before', ha= "right", bbox = {'facecolor': 'oldlace', 'alpha': 0.5, 'boxstyle': "larrow, pad=0.3", 'ec': 'red'})
    plt.show()

    return df_diff_subset_people["Diff"].mean(), df_diff_subset_people["Diff"].median(), df_diff_subset_not_people["Diff"].mean(), df_diff_subset_not_people["Diff"].median()


def create_graph_links(dfs_links):
    G = nx.DiGraph()
    for index, row in dfs_links.iterrows():
        if G.has_edge(row['linkSource'], row['linkTarget']):
            G[row['linkSource']][row['linkTarget']]['weight'] += 1
        else:
            G.add_edge(row['linkSource'], row['linkTarget'])
    return G

    