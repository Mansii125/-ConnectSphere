import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_items(user_df, item_df, username, item_type="PG", top_n=5):
    if 'username' not in user_df.columns:
        raise ValueError("user_profiles.csv must have a 'username' column.")
        
    user_row = user_df[user_df['username'] == username]
    if user_row.empty:
        return item_df.head(top_n)

    user_tags = user_row.iloc[0]['cultural_tags'].split(',')

    all_tags = sorted(list({t for sub in item_df['cultural_tags'].dropna() for t in sub.split(',')}))
    def tag_vector(tags, all_tags):
        return [1 if t in tags else 0 for t in all_tags]

    user_vec = tag_vector(user_tags, all_tags)
    sim_scores = []
    for idx, row in item_df.iterrows():
        item_vec = tag_vector(row['cultural_tags'].split(','), all_tags)
        sim = cosine_similarity([user_vec], [item_vec])[0][0]
        sim_scores.append(sim)
    item_df['similarity'] = sim_scores
    return item_df.sort_values(by='similarity', ascending=False).head(top_n)
