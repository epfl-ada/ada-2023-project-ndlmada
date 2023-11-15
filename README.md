# ada-2023-project-ndlmada
ada-2023-project-ndlmada created by GitHub Classroom


## Abstract <a name="abstract"></a>

Wikispeedia is a game where users get two articles, and have to go from the first one to the second one exclusively by following links. By studying the paths chosen by players, we can capture their chain of thought and find out what key attributes about their goal they used to reach it. 
In this context, we are interested in people. Indeed, as humans, we know the name of thousands of famous people, whether it be for their music, their scientific discoveries or political impact. But is it really the case? Or do we just associate them with more famous people to form a cluster of celebrities associated to a central persona. And finally, do we have an unconscious bias between gender that makes us remember women because of the men in their lives and not because of their personnal successes? And is it linked to their fame domain? Because the first step towards reducing a bias is to acknowledge its existence, we want to determine if there is any in the users choices, so we can consciously try to reduce ours. 

## Research question <a name="research-question"></a>

By focusing on articles about people, we want to determine why people are famous. In particular, we would like to know whether people reach fame because of their accomplishments, or rather their social circle. Indeed, as we know how users got to a certain page, we can track their chain of thought and which elements concerning the given celebrity they used to find them. Furthermore, we would like to see if we can observe any bias between gender or famous people categories. For example, are French painters better known for their friends, or for the artistic movement they belonged to. By analyzing user paths, as well as the overall connection between articles, we aim to answer these questions. 

## Method <a name="method"></a>
### Pre-processing <a name="pre-processing"></a>
#### Dataset <a name="dataset"></a>
We began our data exploration in the [pre-processing](pre_processing.ipynb) Jupyter notebook. Multiple steps of this pre-processing might be useful for further analysis. We decided to create a [utilities](utilities.py) python script containing useful functions including the summary function of the pre-processing applied in the notebook above. 

We looked after the format and the content of the _wikispeedia paths-and-graph_ dataset, revealing manageable sizes of datasets for our analysis. Missing values were only found in the finished path dataset: in the _hashedIpAddress_ (3 missing out of 51,318) and _rating_ (around 50% of missing values) columns. The ratings are optionally assessed by players to evaluate the path's difficulty. Our analysis won't use either the IP address of the players or the ratings. So we decided to simply remove those two columns. With the modified dataset, we did some plots to compare and learn more about the data, focusing particularly on people categories, and their domains.

#### Wikispeedia game <a name="wikispeedia-game"></a>
 We also took some time to examine the game and the links present on the pages. We identified links that were not countable in the game path. For instance, clicking on an image could lead to a page with other article links, but the game would stop tracking the following actions. In our analysis, we need to pay attention to which hyperlinks we must take into account.

### Connection graphs <a name="connection-graphs"></a> 

<!--!! Si jamais j'avais commencé à écrire ça dans ma section, mais enfaite c'est plus utile pour ici, du coup je te l'ai mis, mais si tu veux pas garder aucun soucis, c'est juste au cas ou :) -->

To construct the connection graphs, we need to extract the hyperlinks of each page. To do so, we can use the HTM file of each article since the hyperlinks are specified as _href_. As mentioned in the [wikispeedia game](#wikispeedia-game) section, since not all the links are interesting (links to images, legal stuff such as disclaimer pages, email addresses, …), we need to filter the links to only keep those leading to other article pages.

### Paths analysis <a name="paths-analysis"></a>
To answer our question if people are famous because of their social environment or because of the things they did in life, we will analyse the behavior of people when navigating Wikispeedia : 
1. We will try and understand if people usually follow the shortest path to reach given end articles. This will be done using the known network graph and try to understand if people use more or less steps to go from the start article to the goal article. 
2. We will check if two articles about people that are linked means that the people linked come from the same domains. This will be done using the classification of articles provided by Wikispeedia and quantifying the relatedness of the two people. 
3. We will establish if articles that talk about people on Wikispeedia are mostly visited coming from articles about people (thus hinting to a more "social circle" way of remembering) or about related themes (thus hinting to the fact that we remember people from what they have done). We will use the global connection graph to establish if articles about people are mostly linked to other articles of people and if this could influence the choice when navigating Wikispeedia.

### Articles analysis <a name="article-analysis"></a>

In this section, we are interested in both the links contained within each article and the content of those articles.

#### Links <a name="links"></a>
Our objective is to analyze whether the position of a link on an article page influences player choices. Through this analysis, we want to understand if such influences, if any, have and implications for our main research question.
Given that articles are not constructed as linear plain text due to the presence of tables and images, comparing the absolute position of each link may be difficult. Therefore, we will classify the link positions into the following groups:
  - **Table Links**: Links within tables providing main information about the page subject, often situated on the right.
  - **Section and Sub-Section Links**: Links located within each (sub-)section of pages, ordered according to the sections order.
  - **Legends Links**: Links found in image legends.

After categorizing these links, we will analyze both finished and unfinished paths to determine how often they are used. Then, statistical tests, such as ANOVA, can be employed to compare the occurrences of the three different link groups.
Some considerations need attention:
  1. Some links appear multiple times on the same page. We must assess the percentage of repeating links and determine whether these links belong to multiple position categories. In the latter case of multiple link position categories, the data from the game does not allow us to know which one the player used. Addressing this involves either exclusion from the analysis (if the percentage is small) or creating a new class with mixed positions.
  2. Does the length of a page also influence link selection? Intuitively, shorter pages might have less impact as there is less scrolling before finding the optimal link. The page lengths can be obtained by looking for the number of characters or words in the plain text articles provided in the dataset.

#### Article <a name="article"></a>
In this sub-section, we will analyze the distribution of the main subjects of an article using natural language processing (NLP) techniques, such as Latent Dirichlet Allocation (LDA). This step aims to determine whether the choice of link may be influenced by external factors and, thus, if it has an impact on the main research question.

Finally, related to the [paths analysis](#paths-analysis) section, we classify links into two types: social circle and theme. Themed links can be further differentiated into two sub-categories:
  - **Related Theme**: Articles implying that people are remembered for their achievements.
  - **Unrelated Theme**: Articles unrelated to the social circle or individual accomplishments.

We want to achieve this distinction using a text analysis tool. We will compare queries (in this case, the article names linking to the target) with the plain text of the target article using term frequency-inverse document frequency (TF-IDF) to assess term importance in articles and cosine similarity as a basis score for comparison. Queries not mentioned in the target page will have a cosine similarity score close to zero and thus be categorized as unrelated to the target.


### Identifying gender <a name="identifiying-gender"></a>

To be able to make our observations of differences between men and women, we need to determine which people articles are about women and which are about men. However, in wikipedia, it isn't explicitely displayed. We therefore need to determine it ourselves. To do so, we want to use a pretrained BERT model that we will fine tune for our unsupervised learning task in order to split all those articles in 2 categories. 

#### Page rank <a name="page-rank"></a>

Lets make a graph of the Stars, when one user goes form *Rihanna* to *Madonna* then we create a directed edge *Rihanna* --> *Madonna* in our graph.

Now when we look at the graph we could simply say "ok, lets look at the $in$ degree of each node and the Star with the most in degree would be the most important person".

If the importance score of a Star is denoted by $\pi_u$ then $\pi_u = i_{u}$

But that would be maybe too easy and would not give us the best results. Maybe a star is more clicked on beacause it is in every page. For example, people want to find France and they know that *Jean Dujardin* comes from France but he is not everywhere, however *George Clooney* is on every wikipedia page, so they click on him and then click on *Jean Dujardin*. In our simple model looking only at in degrees, *George* would be more important, but the real important star is *Jean Dujardin*

So we will look at an other more complicated model: 

$\pi_{u} = \sum_{(v,u)}\frac{\pi_{v}}{o_{v}}$ <font size="1">where (u,v) denotes if there is a directed edge form v to u and o is the out degree of a node</font>

More important endorser = more important people 
Your importance is the sum of the importance of all the other peoples that point to you, but if  the person pointing to you is linked with a lot of other peoples then the importance of this link is diminushed. 

So we have a graph of people. Maybe the graph of people is circular and maybe there is a lot of stars, how do we find $\bar{\pi} = [\pi_{1}, \pi_{2}, ...., \pi_{n}]$ which satisfies the above condition ? 

We define the probability for a Random walk to go from node u to v as:
$$\begin{equation}
  H_{uv} =
    \begin{cases}
      1/o_{u} & \text{if $(u,v)\in E$}\\
      0 & \text{Otherwise}\\
    \end{cases}       
\end{equation}$$

So $H$ is the transition matrix of a RW on the graph 

And a "random surfer" has the probability of beeing on a node at a time $t+1$ defined as:
$p(t+1) = p(t)H$, we recognise here a markov chain. <br>If this markov chain is ergodic (non-periodic and strogly connected ie. no dead end) then $p(t) \rightarrow \pi$

To make it ergodic we have to connect the dangeling nodes to the graph 

We define: 
<br>$w=$ indicator of dangeling node <br> $e=$ vector full of 1's

So $\hat{H} = H + \frac{1}{n}(w^{T}e)$

Here we still have some cases where you can be stuck if for example you have a graph like this:<br>
A --> B <--> C, you will never go back to A.
So we implement another Matrix, the teleportation matrix: at every iteration you do a coin flip: with prob $\theta$ you walk on graph $\hat{H}$, with prob $1-\theta$ jump to a random node. 

$G = \theta\hat{H} + (1-\theta)\frac{e^{T}e}{n}$

This matrix can be further complicated by taking weights of the links and changing the definition of $H_{uv}$. For example somone could take this path *Gorge Clooney* --> *coffe* --> *Jean Dujardin* which should have a wheight smaller than a direct *Gorge Clooney* --> *Jean Dujardin*. Or we could take into account if more people took the route *Gorge Clooney* --> *Jean Dujardin* than the route *Francis Coppola* --> *Ariana Grande* then the weight between *Gorge Clooney* and *Jean Dujardin* should be higher. A lot of optimisation can be done to make our model stronger and more complete. 

#### How to find $\pi$ 

We are going to use the Power Method, we are not going to prove it here but basicaly you can calulate $\pi$ bit iterating 
$$\pi_{t+1} = \frac{\pi_{t} G}{\pi_{t} G e^{T}}$$

This will converge in about 50-100 iterations and then you just have to sort the arguments of your vector $\bar{\pi}$ to find the most important star. 


#### Applications and further possibilities of analysis 

We discused here about ranking stars but this method is applicable to a lot of other things like ranking historical (or not) events, books, movies, the wikipedia pages themselfs etc.. Anything that can be used. 

We could also rank the different pages by looking at the links on the HTML files and creating a graph with that and ranking the pages that way. You could then compare your ranking with the path that user took and the ranking with the html link and compare the two. Maybe there is interesting comparaisons to make. 

## Timeline

Friday 22nd december, 6pm, drink free mulled wine with agepoly on the esplanade :)

