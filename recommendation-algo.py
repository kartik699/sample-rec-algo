# Import necessary libraries
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

# Load the data
# sample CSV files containing data about posts, user has interacted with (real data may vary)
likes = pd.read_csv('likes.csv')
users = pd.read_csv('users.csv')
posts = pd.read_csv('posts.csv')

# Merge the data
data = pd.merge(pd.merge(likes, users, on='user_id'), posts, on='post_id')

# Create a user-post rating matrix
user_post_ratings = data.pivot_table(index='user_id', columns='post_id', values='like').fillna(0)

# Perform matrix factorization using Singular Value Decomposition (SVD)
U, sigma, Vt = svds(user_post_ratings, k=50)
sigma = np.diag(sigma)

# Predict ratings for unseen posts
all_user_ratings = np.dot(np.dot(U, sigma), Vt)
pred_user_ratings = pd.DataFrame(all_user_ratings, columns=user_post_ratings.columns, index=user_post_ratings.index)

# Get the top recommendations for a user
def recommend_posts(user_id, num_recommendations=10):
    # get user ratings for the unseen post in desc order such that highest rated (most preferrable) post comes first
    user_ratings = pred_user_ratings.loc[user_id].sort_values(ascending=False)
    # fetch posts user has already liked
    user_likes = likes.loc[likes['user_id'] == user_id]['post_id']
    recommendations = pd.DataFrame(columns=['post_id', 'title', 'view_count', 'score'])
    for post_id, rating in user_ratings.iteritems():
        # only include posts which user has not yet interacted with
        if post_id not in user_likes:
            post = posts.loc[posts['post_id'] == post_id]
            view_count = post['view_count'].values[0]
            # calculates a score for the post by multiplying the rating by the view count, this score aims to balance the predicted rating with the popularity of the post.
            score = rating * view_count
            recommendations = recommendations.append({'post_id': post_id, 'title': post['title'].values[0], 'view_count': view_count, 'score': score}, ignore_index=True)
    # sorts the recommendations data frame by the score in descending order.
    recommendations = recommendations.sort_values(by='score', ascending=False).head(num_recommendations)
    return recommendations
