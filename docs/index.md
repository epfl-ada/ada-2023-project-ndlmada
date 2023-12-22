Have you ever wondered how many people you know? Well, the answer depends on what you mean by “knowing” and even like this, it’s not an easy question to answer. Quite a few scientists have tackled this question. First of all, let’s consider the people you really know, the one you could have a drink with when you cross them in the street. This question was answered in the nineties by the British anthropologist Robin Dunbar. He linked the size of the primates’ brains to their ability to remember their peers. Given this, he concluded that we know around 150 people[^1]. 

But that seems rather small, right? Think about all the people you went to school with, or all of your coworkers, that’s definitely more than 150. So let’s consider a new category then. Can you tell me how many faces you remember? Whether it be your favourite singer whom you never met but would definitely recognise, or the cashier you see every week at the supermarket but whose name you don’t know, these are all faces that you recognize in a crowd. In this case, studies showed that humans remember around 5,000 faces, which makes already more sense[^2].

<div align="center"><iframe src="https://giphy.com/embed/3oEduNGzfmQkYtT916" align-items="center" display="block" width="350" height="350" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/suitsusanetwork-suits-donna-paulsen-3oEduNGzfmQkYtT916">via GIPHY</a></p></div>

And then there’s an even larger category, comprising all the names that you know: all your relatives, colleagues, neighbours, politicians, historical figures, artists, musicians, scientists… SThis category is almost endless but sadly no studies have managed to determine this number.

Now let’s forget the people you really know, and focus on those we might call celebrities, our stars. There are so many names that we know: the scientist whose theorem you studied in high school, the politician that made reforms in your country 3 years ago or the athlete that you followed since primary school. Say you are a fan of Taylor Swift, you know so much about her: where she comes from, all her albums, her personal life and the name of her cats. However, you’ve only ever vaguely heard about Napoleon and only know that he’s French. And then there’s that painter Turner and you only know that he was friends with Monet. Or Michelle Obama, you definitely know her because of her husband, but can you list anything that she accomplished? 

Overall, we remember different people for different reasons. There are those whom we know everything about, those we learned about in school, those we know for what they did, where they lived or who they knew. This is what we want to try and understandAnd that’s what interests us : how do we remember people? 

## Wikispeedia and the exploration of our data:
To answer our question, we used the data from the Wikispeedia Game[^3] developed by the Data Science Lab (dLab), a research group at EPFL[^4]. The aim of this game is to navigate from one Wikipedia page to another using the links between them and creating the shortest path you can. The number of articles available is only a fraction of the Wikipedia database. The choice of source and target articles is either randomly assigned by the game or chosen by the player. 
To gain insights into how people are remembered, we studied the data and first started by looking looked into the different article categories. Each category is a groupment of sub-categories. Fig.1 is the representation of the three first sub-categories. 

<iframe src="overall_dataset_bar.html" width="1100px" height="530px" frameborder="0" position="relative">enre plot</iframe>
<p style="text-align: center;font-size: 0.8em;"><span style="color :blue"> Fig. X :</span> Pie chart of perfecntages blebleble</p>

The category that interested us the most is the one about of people. To compare it with others, we need a better overview of their distribution across all articles. We found out that only 15% of the articles are about people. Even so, this category still represents the third most prominent category as observed in Fig.2. However, not all articles are selected as targets. Within target articles the target group, around 12% of them are people, which is close to the article distribution. Looking at the paths leading to those selected targets, 25% of the articles visited are people. The percentage of people articles visited is lower than those of non-people, but it is not surprising given the distribution of people/non-people articles. If we looked at the ratio of the categories distribution within the path divided by the categories distribution among the articles and compared for the people and non-people articles, we found two ratios quite similar. Thus according to the repartition of people pages and non-people pages, the 25% is not so low. 

<iframe src="Pie_paths_percentages.html" width="100%" height="400px" frameborder="0" position="relative">enre plot</iframe>
<p style="text-align: center;font-size: 0.8em;"><span style="color :blue"> Fig. X :</span> Pie chart of perfecntages blebleble</p>
## Path representation & Game strategy: 
We wanted to visualise the path leading to each people target to analyse their behaviour. Spoiler: the comparison of 631 distinct plots is not the most efficient way to look at our data. As obvious as it may seem, we, however, created a function to do the plot before realising that. In theory, we wanted to put the target node in evidence and all around it, each path, with the primary category colour for each node. In reality, it doesn’t look as nice as expected, for various reasons such as the presence of return in the paths or just because they are highly connected.



ADD GRAPH 
expectation: petit dessin nice de notre idée 
vs 
Reality: mettre deux ou trois plots l’un à côté de l’autre, 3 catégories de plot: c’eut avec faible, moyenne, forte population de path et un bouton random qui select les plots. 

However, we noticed something from those plots: the targets tend to be reached by a limited number of links. This observation motivated us to narrow down our research not by looking at the whole path but at only a small part of it. 

A common way to play Wikispeedia is to first reach a general concept with many outgoing links, such as country and geography, as fast as possible. Then, players narrow down the research on the subject to find articles as close as possible to the subject of the target. The first phase heavily depends on the source article, and the second phase on the target article[^5].

![Graphe](path_graph.png)
<p style="text-align: center;font-size: 0.8em;"><span style="color :blue"> Fig. X :</span> Pie chart of perfecntages blebleble</p>

Due to these two observations, we will focus on the three last links before reaching the target. In Fig.4, we can observe the behaviour of those reduced paths according to the category of their target. 



	
<script type="text/javascript"> function loadPlot() {
    var plotSelector = document.getElementById('plotSelector');
    var plotFrame = document.getElementById('plotFrame');

    var selectedPlot = plotSelector.value;
    plotFrame.src = selectedPlot;
}</script>
<iframe  width="100%" height="530px"  id="plotFrame" frameborder="0" src="bar/path_bar_People.html"></iframe>

<label for="plotSelector">Select a category to plot:</label>
<select id="plotSelector" onchange="loadPlot()">
    <option value="bar/path_bar_Art.html" >Art</option>
    <option value="bar/path_bar_Countries.html">Countries</option>
    <option value="bar/path_bar_IT.html">IT</option>
    <option value="bar/path_bar_Business_Studies.html">Business & Studies</option>
    <option value="bar/path_bar_Citizenship.html">Citizenship</option>
    <option value="bar/path_bar_Design_and_Technology.html">Design & Technology</option>
    <option value="bar/path_bar_Everyday_life.html">Everyday Life</option>
    <option value="bar/path_bar_Geography.html">Geography</option>
    <option value="bar/path_bar_History.html">History</option>
    <option value="bar/path_bar_Language_and_literature.html">Language & Litterature</option>
    <option value="bar/path_bar_Mathematics.html">Mathematics</option>
    <option value="bar/path_bar_Music.html">Music</option>
    <option value="bar/path_bar_People.html">People</option>
    <option value="bar/path_bar_Religion.html">Religion</option>
    <option value="bar/path_bar_Science.html">Science</option>
</select>

<p style="text-align: center;font-size: 0.8em;"><span style="color :blue"> Fig. X :</span> Pie chart of perfecntages blebleble</p>


In Fig. 4a, except for a few target categories such as mathematics or music that are more restricted, it seems that most of the targets are reached from articles of various categories. For the people target, the last link comes from all categories. However, the people-to-people last link seems a bit thinner than other categories targeting people. A second visualisation (Fig. 4b), confirmed those observations. Indeed, for the non-people target, the previous path stays at most in the same categories, while for people it comes from different areas and only on fourth from people. This distinction between people and non-people may be related to the second sub-categories of the article. When non-people second subcategory remains in the same genre as the primary category, the second sub-category of people varies a lot. There are 20 sub-categories of people (Fig. 5). As we can observe, the biggest sub-categories (historical figures) can be also classified as history, the most represented number of articles of this category before the path end in people.  (MAYBE; A VERIFIER).

<iframe src="people_categories.html" width="100%" height="530px" frameborder="0" position="relative">Genre plot</iframe>
<p style="text-align: center;font-size: 0.8em;"><span style="color :blue"> Fig. X :</span> Pie chart of perfecntages blebleble</p>


## Gender distribution in Wikispeedia
From the previous observations, we tend to conclude that in this dataset the people are more reached by what they achieved than by their social circle. However, we didn’t stop there. Knowing that women are underrepresented in Wikipedia articles[^6] and that they tend to be more referred to the men in their surroundings than to their accomplishments, we wonder if this tendency can be also observed in this selection of Wikipedia articles and in the choice of the players.  
First of all, we extract from Wikidataan external database the gender of people and then match them with our own dataset. As seen in Fig.???, We wanted to look at the data to see whether we have balanced data or not. And spoiler, it is not the case. As expected, the number of women is very low which provided us a really unbalanced dataset. The unknown data represents people like Pikachu for example, which are not really a people.
				
From the repartition among categories, we can see that the only group where there seems to have an equal repartition is for actors, models and celebrities. (MAYBE WE CAN LOOK AT THEM TO CONCLUDE SOMETHING ?)

<iframe src="overall_categories_gender.html" width="100%" height="530px" frameborder="0" position="relative">Genre plot</iframe>
<p style="text-align: center;font-size: 0.8em;"><span style="color :blue"> Fig. X :</span> Pie chart of perfecntages blebleble</p>
	
<script type="text/javascript"> function loadPlotPath() {
    var plotSelector = document.getElementById('plotSelectorPath');
    var plotFrame = document.getElementById('plotFramePath');

    var selectedPlot = plotSelector.value;
    plotFramePath.src = selectedPlot;
}</script>

<img  width="80%"  id="plotFramePath" frameborder="0" src="path/Art.png">

<label for="plotSelectorPath">Select a category to plot:</label>
<select id="plotSelectorPath" onchange="loadPlotPath()">
    <option value="path/Art.png" >Art</option>
    <option value="path/Business_Studies.png" >Business & Studies</option>
    <option value="path/Citizenship.png" >Citizenship</option>
    <option value="path/Countries.png" >Countries</option>
    <option value="path/Design_and_Technology.png" >Design & Technology</option>
    <option value="path/Everyday_life.png" >Everyday Life</option>
    <option value="path/Geography.png" >Geography</option>
    <option value="path/History.png" >History</option>
    <option value="path/IT.png" >IT</option>
    <option value="path/Language_and_literature.png" >Language & Litterature</option>
    <option value="path/Mathematics.png" >Mathematics</option>
    <option value="path/Music.png" >Music</option>
    <option value="path/People.png" >People</option>
    <option value="path/Religion.png" >Religion</option>
    <option value="path/Science.png" >Science</option>
</select>
<p style="text-align: center;font-size: 0.8em;"><span style="color :blue"> Fig. X :</span> Pie chart of perfecntages blebleble</p>

## PageRank and gender

To express a ranking of the Wikipedia people’s pages, we took the number of people going to their page. The more players go through a page, the more this page can be considered as “popular”. This method isn’t actually sufficient because if a page is proposed on every other page, it would be way more likely that the player goes through this page than one that is only mentioned in one or two pages. Therefore, we normalise the number of ingoing paths with the number of links going out of the page.

With these calculations, we obtain the following rankings.
If we apply gender analysis to the page rank, 




<script type="text/javascript"> function loadPlotGender() {
    var plotSelector = document.getElementById('plotSelectorGender');
    var plotFrame = document.getElementById('plotFrameGender');

    var selectedPlot = plotSelector.value;
    plotFrameGender.src = selectedPlot;
}</script>
<iframe  id="plotFrameGender" width="100%" height="530px" frameborder="0" src="bar/path_bar_women.html"></iframe>

<label for="plotSelectorGender">Select a category to plot:</label>
<select id="plotSelectorGender" onchange="loadPlotGender()">
    <option value="bar/path_bar_women.html">Women</option>
    <option value="bar/path_bar_men.html">Men</option>
    <option value="bar/path_bar_actors, models and celebrities.html" >Actors, Models and celebrities (both genders)</option>
    <option value="bar/path_bar_female actors.html">Actors, Models and celebrities (Women)</option>
    <option value="bar/path_bar_male actors.html">Actors, Models and celebrities (Men)</option>
</select>
<p style="text-align: center;font-size: 0.8em;"><span style="color :blue"> Fig. X :</span> Pie chart of perfecntages blebleble</p>

<script type="text/javascript"> function loadPlotRank() {
    var plotSelector = document.getElementById('plotSelectorRank');
    var plotFrame = document.getElementById('plotFrameRank');

    var selectedPlot = plotSelector.value;
    plotFrameRank.src = selectedPlot;
}</script>

<img  width="80%"  id="plotFrameRank" frameborder="0" src="path/Art.png">

<label for="plotSelectorRank">Select a category to plot:</label>
<select id="plotSelectorRank" onchange="loadPlotRank()">
    <option value="rank_cat/art.png" >Art</option>
    <option value="rank_cat/business.png" >Business & Studies</option>
    <option value="rank_cat/citizenhip.png" >Citizenship</option>
    <option value="rank_cat/countries.png" >Countries</option>
    <option value="rank_cat/design.png" >Design & Technology</option>
    <option value="rank_cat/everyday.png" >Everyday Life</option>
    <option value="rank_cat/geogra^hy.png" >Geography</option>
    <option value="rank_cat/history.png" >History</option>
    <option value="rank_cat/it.png" >IT</option>
    <option value="rank_cat/language.png" >Language & Litterature</option>
    <option value="rank_cat/mathematics.png" >Mathematics</option>
    <option value="rank_cat/music.png" >Music</option>
    <option value="rank_cat/people.png" >People</option>
    <option value="rank_cat/religion.png" >Religion</option>
    <option value="rank_cat/science.png" >Science</option>
</select>
<p style="text-align: center;font-size: 0.8em;"><span style="color :blue"> Fig. X :</span> Pie chart of perfecntages blebleble</p>



Overall, people targets are more reached via category articles than via a social circle. However, does that mean we remember them more by their achievement? Not necessarily. In fact, in this analysis, there are many biases to consider. 
First at all, as mentioned above, the Wikispeedia game is based on only a fraction of the Wikipedia database. Maybe this reduction in the number of articles introduced a bias of selection. Furthermore, since the players can choose the source-target pairs, they tend to choose articles they know more about which do not reflect the common knowledge everybody will have about the celebrities. Also, it may be that the way the articles are constructed to influence the choice of the players since lots of them want to play as fast as possible. Do short articles lead to wiser choices? Do people prefer to select links that are on a table summary, on a paragraph at the top of the page, or on a legend of an image? Actually, we looked a bit at the last question, unfortunately, as for the gender dataset, the position of the link dataset is highly unbalanced. Almost all of the links are contained in paragraphs and for those that are not, they are often present multiple times on the page. Since we don’t know exactly which link with the same reference the player chose, analysis cannot be clearly conducted.
Lastly, something we must not forget is that Wikispeedia is a game. As for all games, some strategies are made to reach the goal more efficiently, so it might be a huge influence on the choice made by the players. Hence, people within this article selection are not reached through their social circle. They tend to be more selected by the domained they are known for. Also (ADD SMALL CONCLUSION WITH THE GENDER BIAS)

### Bibliography
[^1]: Dunbar’s number. In: Wikipedia. ; 2023. Accessed December 18, 2023. [https://en.wikipedia.org/w/index.php?title=Dunbar%27s_number&oldid=1190501720](https://en.wikipedia.org/w/index.php?title=Dunbar%27s_number&oldid=1190501720)
[^2]: Jenkins R, Dowsett AJ, Burton AM. How many faces do people know? Proc R Soc B Biol Sci. 2018;285(1888):20181319. doi:10.1098/rspb.2018.1319
[^3]: Wikispeedia. Accessed December 18, 2023. [Pie_main_cat_people.html](Pie_main_cat_people.html)
[^4]: Lab EDS. Data Science Lab. dlab @ EPFL. Accessed December 18, 2023. [http://dlab.epfl.ch/](http://dlab.epfl.ch/)
[^5]: West R. Wikispeedia: An Online Game for Inferring Semantic Distances between Concepts.
[^6]: Wikipedia:WikiProject Women in Red. In: Wikipedia. ; 2023. Accessed December 18, 2023. [https://en.wikipedia.org/w/index.php?title=Wikipedia:WikiProject_Women_in_Red&oldid=1189903435](https://en.wikipedia.org/w/index.php?title=Wikipedia:WikiProject_Women_in_Red&oldid=1189903435)
