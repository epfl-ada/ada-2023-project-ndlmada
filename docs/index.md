Have you ever wondered how many people you know? Well, the answer depends on what you mean by "knowing," and even like this, it’s not an easy question to answer. Quite a few scientists have tackled this question. Firstly, let’s consider the people you really know—the ones you could have a drink with when you cross them in the street. This question was answered in the 1990s by the British anthropologist Robin Dunbar. He linked the size of the primates’ brains to their ability to remember their peers. Given this, he concluded that we know around 150 people[^1]. 

But that seems rather small, right? Think about all the people you went to school with or all of your coworkers; that’s definitely more than 150. Then, let’s consider a new category. Can you tell me how many faces you remember? Whether it be your favourite singer, whom you never met but would definitely recognise, or the cashier you see every week at the supermarket but whose name you don’t know, these are all faces that you recognise in a crowd. In this case, studies showed that humans remember around 5,000 faces, which makes sense already[^2].

<div align="center"><iframe src="https://giphy.com/embed/3oEduNGzfmQkYtT916" align-items="center" display="block" width="350" height="350" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/suitsusanetwork-suits-donna-paulsen-3oEduNGzfmQkYtT916">via GIPHY</a></p></div>


And then there’s an even larger category, comprising all the names that you know: all your relatives, colleagues, neighbours, politicians, historical figures, artists, musicians, scientists, etc. Sadly, we didn’t find any studies that managed to determine this number.

Now let’s forget the people you really know and focus on those we might call celebrities—our stars. There are so many names that we know: the scientist whose theorem you studied in high school, the politician who made reforms in your country three years ago, or the athlete that you followed since primary school. Say you are a fan of Taylor Swift. You know so much about her: where she comes from, all her albums, her personal life, and the name of her cats. However, you’ve only ever vaguely heard about Napoleon and only know that he’s French. And then there’s that painter, Turner, and you only know that he was friends with Monet. Or Michelle Obama; you definitely know her because of her husband, but can you list anything that she accomplished?

Overall, we remember different people for different reasons. There are those whom we know everything about, those we learned about in school, those we know for what they did, where they lived, or who they knew. This is what we want to try and understand: how do we remember people?

# Wikispeedia and exploration of our data:
To answer our question, we used data from the Wikispeedia Game3 developed by the Data Science Lab (dLab), a research group at EPFL4. The aim of this game is to navigate from one Wikipedia page to another using the links between them and create the shortest path you can. The number of articles available is only a fraction of the Wikipedia database. The choice of source and target articles is either randomly assigned by the game or chosen by the player.

To gain insights into how people are remembered, we studied the data and first started by looking into the different article categories. Each category is a grouping of sub-categories. Fig.1.a is the representation of the three first sub-categories. We will refer to the first nodes of the category path as categories and the second nodes as sub-categories.

<img src="graph_1.png" width="100%">
<p style="text-align: center;font-size: 0.8em; font-style: italic"> [Fig. 1] : Visualisation of the first three subcategories of all articles </p>

<iframe src="overall_dataset_bar.html" width="1100" height="530" frameborder="0" ></iframe>
<p style="text-align: center;font-size: 0.8em; font-style: italic">[Fig. 2] : Distribution of the first two subcategories.</p>

The category that interests us the most is the People one. To compare it with others, we need a better overview of their distribution across all articles. We found out that only 14.7% of the articles are about people. Even so, this category still represents the third most prominent category (Fig. 2). However, not all articles are selected as targets. Within target articles, around 11.5% of them are people, which is close to the article distribution. Looking at the paths leading to those selected targets, 25.5% of the articles visited are People, which is lower than those of non-People. Thislow proportion is not surprising given the distribution of People/non-People articles. Yet, somehow the proportion of people in paths almost doubles compared to the proportion of articles about people in Wikipedia.


<iframe src="Pie_paths_percentages.html" width="100%" height="400px" frameborder="0" position="relative"></iframe>
<p style="text-align: center;font-size: 0.8em; font-style: italic"> [Fig. 3] : People and non-People distribution, from left to right, within all articles, within all the paths, and within all the paths leading to a People target</p>



# How can we analyse such a dataset?
A common way to play Wikispeedia is to first reach a general concept with many outgoing links, such as countries or topics related to geography (Fig.4), as fast as possible. Then, players narrow down the research on the subject to find articles as close as possible to the subject of the target. The first phase heavily depends on the source article, and the second phase on the target article5. 


![Graphe](path_graph.png)
<p style="text-align: center;font-size: 0.8em; font-style: italic"> [Fig. 4] : Representation of the number of links between categories. The plot does not take into account the self-linking, and the categories that do not have enough linking numbers between them are not shown. It means, for example, that IT, Art and Mathematics mainly stay in their categories and that Geography is reached by a large number of other categories.</p>

Due to these two observations, we will focus on the last three links before reaching the target. In Fig.5, we can observe the behaviour of those reduced paths according to the category of their target.





# What do these last three links tell us?
In Fig. 5, we can look at the category distribution of the three last steps for each finished path. We separated each plot according to the target category. The colours of the lines correspond to the category visited by the node (N-1) just before reaching the target. This colour choice allows us to notice, for example, that in Science for most of the paths, whatever the category in N-3, most of them finished in the Science category in N-1. Most of the targets are reached from articles of various categories, but there are some exceptions, such as for the Mathematics or Music targets, which mostly stay in their own categories, which is coherent with Fig.4.
	
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
<p style="text-align: center;font-size: 0.8em; font-style: italic"> Fig. 5 : The categories of the last three articles visited, grouped by target categories. Each line corresponds to a path, and its colour corresponds to the category visited by the path in N-1 a) People target: within the last links, all the categories are more or less used to reach the target.  b) History target: mainly comes from History articles or often closely related subjects such as Countries, Geography, People and Religion. c) Science target: almost all of the paths come from Science-related subjects.  d) Mathematics target: almost all of the paths come from Mathematics-related subjects.</p>


# What about the People?
For the People target, the last links come from all categories (Fig. 5). However, the People-to-People last link is less used than other categories. Indeed, for the non-People target, the previous path stays at most in the same categories, while for People target, the most frequent previous link category is History, while People only come in fourth. (Fig. 6).



	
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

<p style="text-align: center;font-size: 0.8em; font-style: italic"> Fig. 6 : Distribution of the N-3 articles leading to a target in people (change target in selection box). The count per step was normalised by the total number of articles in each category. </p>

This distinction between People and non-People may be related to their sub-categories. In comparison to those of non-People that remain in the same genre as their respective categories, the sub-categories of People vary a lot. There are 20 sub-categories of People (Fig. 6). As we can observe, the biggest sub-categories (Historical figures) can be associated with History, the most represented last article’s category before the path ends in People. 



<iframe src="people_categories.html" width="100%" height="530px" frameborder="0" position="relative">Genre plot</iframe>
<p style="text-align: center;font-size: 0.8em; font-style: italic"> Fig. 7 :</span> Distribution of people first subcategories</p>
Based on the results above, we concluded that, to access a target of a certain category, players tend to reach it using other articles within the same categories, even when those categories are less represented, such as Music, Religion, or Art (Fig. 1.b). This trend is particularly evident in certain categories, such as Science, where almost all the preceding links are also within the science domain. In other cases, it is less obvious, as for History, where many categories lead to it, but history remains the dominant one. However, these paths exhibit a similar tendency. The only exception is observed for the People target, as mentioned earlier. This suggests that, contrary to our initial assumption about our research question, individuals are not remembered for their social circles but rather for their achievements. This is indicated by the fact that they are frequently reached through links associated with other subcategories rather than through other People.
 


Can we find out People’s fame with our dataset? 

We did a lot of counting, but a count isn't perfect to really affirm a global trend. Indeed, imagine there are 550 people trying to find Hitler [7], then one would expect that most of the player's path's penultimate page will be WW2. But now let's imagine that:
 
250 layers went from the “WW2” page to find him
100 players went from the “Germany” page to find him
100 players went from the “Austria” page to find him  
50 players went from the “Poland” page to find him
50 players went from the “France” page to find him
 
If you now count the different categories, you will find that 250 pages have the category history and 300 pages have the category Country. But the truth is that he is most known for what he did and not for where he came from. 
 
How can one resolve this problem and devise a kind of ranking for the pages?
 
Use Pagerank ! 

![captain_obvious.jpg](Captain_obvious)





<iframe src="overall_categories_gender.html" width="100%" height="530px" frameborder="0" position="relative">Genre plot</iframe>
<p style="text-align: center;font-size: 0.8em; font-style: italic"> Fig. X :</span> Pie chart of perfecntages blebleble</p>





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
<p style="text-align: center;font-size: 0.8em; font-style: italic"> Fig. X :</span> Pie chart of perfecntages blebleble</p>

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
<p style="text-align: center;font-size: 0.8em; font-style: italic"> Fig. X :</span> Pie chart of perfecntages blebleble</p>


### References
[^1]: Dunbar’s number. In: Wikipedia. ; 2023. Accessed December 18, 2023. [https://en.wikipedia.org/w/index.php?title=Dunbar%27s_number&oldid=1190501720](https://en.wikipedia.org/w/index.php?title=Dunbar%27s_number&oldid=1190501720)
[^2]: Jenkins R, Dowsett AJ, Burton AM. How many faces do people know? Proc R Soc B Biol Sci. 2018;285(1888):20181319. doi:10.1098/rspb.2018.1319
[^3]: Wikispeedia. Accessed December 18, 2023. [Pie_main_cat_people.html](Pie_main_cat_people.html)
[^4]: Lab EDS. Data Science Lab. dlab @ EPFL. Accessed December 18, 2023. [http://dlab.epfl.ch/](http://dlab.epfl.ch/)
[^5]: West R. Wikispeedia: An Online Game for Inferring Semantic Distances between Concepts.
[^6]: Wikipedia:WikiProject Women in Red. In: Wikipedia. ; 2023. Accessed December 18, 2023. [https://en.wikipedia.org/w/index.php?title=Wikipedia:WikiProject_Women_in_Red&oldid=1189903435](https://en.wikipedia.org/w/index.php?title=Wikipedia:WikiProject_Women_in_Red&oldid=1189903435)
