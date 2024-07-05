# modified function to include diversity score to promote diverse content
def recommend_posts(user_id, num_recommendations=10):
    user_ratings = pred_user_ratings.loc[user_id].sort_values(ascending=False)
    user_likes = likes.loc[likes['user_id'] == user_id]['post_id']
    recommendations = pd.DataFrame(columns=['post_id', 'title', 'view_count', 'score', 'diversity_score'])

    for post_id, rating in user_ratings.iteritems():
        if post_id not in user_likes:
            post = posts.loc[posts['post_id'] == post_id]
            view_count = post['view_count'].values[0]
            content_type = post['content_type'].values[0]
            # diversity score calculated here
            diversity_score = calculate_diversity_score(content_type)
            score = rating * view_count * diversity_score
            recommendations = recommendations.append({
                'post_id': post_id,
                'title': post['title'].values[0],
                'view_count': view_count,
                'score': score,
                'diversity_score': diversity_score
            }, ignore_index=True)
            
    recommendations = recommendations.sort_values(by='score', ascending=False).head(num_recommendations)
    return recommendations

def calculate_diversity_score(content_type):
    # Example logic to assign higher scores to less frequently seen content types
    if content_type in ['news', 'opinion']:
        return 1.2
    elif content_type in ['entertainment', 'sports']:
        return 1.1
    else:
        return 1.0
