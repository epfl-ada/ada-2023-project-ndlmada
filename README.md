# ada-2023-project-ndlmada
ada-2023-project-ndlmada created by GitHub Classroom




## Method

### Ranking 

#### Defining our problem 

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



