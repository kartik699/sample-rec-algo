# Content-Based Recommendation Algorithm

In this sample, we load the likes, users, and posts data into dataframes, merge them, and create a user-post rating matrix. We then perform matrix factorization using SVD to reduce the dimensionality of the data and predict ratings for unseen posts. Finally, we define a function to recommend posts for a given user, which sorts the predicted ratings by score (rating times view count) and returns the top recommendations.

We can make a hybrid model by merging *Collaborative Filtering* technique with this algorithm. Collaborative Filtering aims to predict ratings for posts based on the taste of other users who also have interacted with similar kind of posts in the past as our target user. In a nutshell, it is the method of recommending posts based on the similarity of interactions of more than one users.

### Modified Algorithm to include Diversity Factor
In the modified file called algo-with-diversity.py, calculate_diversity_score gives a high score to content types categorized as diverse or occurring less often. The resultant score will be then used to advise on diversity and personalization concurrently.

### Architecture of Proposed Recommender System
![image](https://github.com/kartik699/sample-rec-algo/assets/58633671/b30cb81d-dad6-45a1-abab-2f17b1612f60)
