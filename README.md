
# LookUp : Stars and why we know them

## Abstract
[Wikispeedia](https://snap.stanford.edu/data/wikispeedia.html) is a fun game where users get two articles, and have to go from the first to the second one by following links. By studying the paths chosen by players, we can capture their chain of thought and find out what key attributes about their goal they used to reach it. In this context, we are interested in people. Indeed, as humans, we know the names of thousands of famous people, whether it be for their music, their scientific discoveries or political impact. But is it really the case? We want to find out if our brain makes unconscious biases towards some celebrities by remembering them for the wrong reasons.
Because the first step towards reducing a bias is to acknowledge its existence, we want to determine if there is any in the user's choices, so we can consciously try to reduce ours.

## Research question
By focusing on articles about people, we want to determine why they are famous. In particular, whether people are referred to because of their accomplishments or their social circle. Indeed, as we know how users got to a certain page, we can track their chain of thought and which elements concerning the given celebrity they used to find them. Furthermore, we would like to see if we can observe any bias between gender or fame categories. Do we have a bias between gender that makes us remember women because of people in their lives and not their personal success? And is it linked to their fame domain?
We will answer these questions by analyzing user paths, as well as the overall connection between articles and articles themselves.

## Method
### Preprocessing
We looked at the format and the content of the _wikispeedia paths-and-graph_ dataset, revealing manageable sizes of datasets for our analysis. Missing values were only found in the finished path dataset (_hashedIpAddress_ and _rating_ columns). Our analysis won't use these so we removed them. With the modified dataset, we did some plots to compare the data, focusing particularly on people categories.
We took some time to examine the game and the links present on the pages. We identified links that were not countable in the game path. For instance, clicking on an image could lead to a page with other article links, but the game would stop tracking the following actions.

### Article connection graphs
To construct the connection graphs of links between articles, we need to extract the hyperlinks of each page using the HTM file of each article. As previously mentioned, since not all the links are interesting (links to images, legal stuff such as disclaimer pages, email addresses, …), we need to filter the links to only keep those leading to other article pages. For  two articles about people that are linked, we will check if it means that the people linked come from the same domain. This will be done using the classification of articles provided by Wikispeedia and quantifying the relatedness of the two people.

### Paths analysis
To determine why people are famous, we will analyze the behavior of people when navigating Wikispeedia :
Are articles about people mostly visited coming from articles about people or about related themes .
We will use the global path connection graph to establish if articles about people are mostly linked to articles of people. Also, could this influence the player’s choice when navigating Wikispeedia ?

### Page Rank 
To draw some conclusions about why people are famous, we can rank the Wikipedia pages using different criterions and compare the obtained rankings. It is also possible that the difference between rankings show some gender differences between how celebrities are perceived by the public.

We can implement this fame ranking by using page rank. Indeed, we can create a graph by looking at the path players took and taking only edges that go from celebrities and what they did. By running page rank on this graph you get a ranking of the most importants celebrities calculated on what they did and how people remember it.

### Articles analysis
We are interested in both the links contained within each article and their content. 

#### Links
We want to analyze whether the position of a link in an article influences player choices. Given that articles are not constructed as linear plain text, comparing the position of each link may be difficult. Therefore, we will categorize the links. Then we will analyze both (un)finished paths to determine how often they are used. Statistical tests, such as ANOVA, can be employed to compare the occurrences of the link groups. We noticed that some links appear multiple times on the same page, so maybe they are in multiple categories. In this case, we cannot know which one the player took. Also, pages have different lengths and may influence the link selection. To incorporate this information into the analysis, you can obtain page lengths by counting the number of words in the plain text articles.

#### Articles
We will analyze the distribution of the main subjects of an article using natural language processing to determine if the authors focused more on personal achievements or on the social circle.
We will classify linked articles into two types: social circle and theme. Themed links can be further differentiated into two sub-categories:
- Related Themes: Articles implying that people are remembered for their achievements.
- Unrelated Themes: Articles unrelated to the social circle or individual accomplishments.
We want to achieve this distinction using a text analysis tool. We will compare queries (in this case, the article names linking to the target) with the plain text of the target article to assess term importance in articles and cosine similarity as a basis score for comparison.

### Identifying gender
To observe differences between men and women, we need to determine the gender of people. However, in Wikipedia, it isn't explicitly displayed. To do so we will take profit from [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) as it contains a gender category for pages about people. We will extract this information to obtain the required details for our more advanced analysis.


## Timeline


| Week | Task | Assigned to |
| --- | --- | --- |
| **Week 10** | Paths graph connection | `Timo` |
|  | Gender determination | `Louise` |
|  | Links positions with statical tests | `Julie` |
|  | Articles analysis | `Romane` `Emeric`|
| **Week 11** | Paths graph connection | `Timo` |
|  | Merge connection graphs with results of articles analysis | `Everyone` |
|  | Work on Homework 3 | `Everyone` |
| **Week 12** | Finish data analysis and conclude | `Timo` `Louise` `Emeric` |
|  | Beggin storytelling | `Julie` | 
|  | Visual identity of the website | `Romane` |
| **Week 13** | Finish Story details | `Everyone` |
|  | Work on website | `TBD` | 
|  | Update graph visuals | `TBD` |
|  | Re-write README | `Everyone` |
| **Week 14** | Finish Website | `Everyone` |
|  | Clean code | `Everyone` |

## References : 

[Wikispeedia](https://snap.stanford.edu/data/wikispeedia.html)

[Wididata](https://www.wikidata.org/wiki/Wikidata:Main_Page)


