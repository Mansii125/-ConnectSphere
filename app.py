# -------------------------
# ConnectSphere - app.py
# -------------------------

import streamlit as st
import pandas as pd
from recommendation_engine import recommend_items
from streamlit_folium import folium_static
import folium
import streamlit_authenticator as stauth
import os

# -------------------------
# LOGIN
# -------------------------
credentials = {
    "usernames": {
        "mansi": {"name": "Mansi", "password": "1234"},
        "namish": {"name": "Namish", "password": "abcd"}
    }
}

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="connectsphere_cookie",
    cookie_key="connectsphere_secret_key",  # required
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("main", fields={"Form name": "Login"})

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    user_df = pd.read_csv("user_profiles.csv")
    pg_df = pd.read_csv("pg_data.csv")
    food_df = pd.read_csv("food_data.csv")
    event_df = pd.read_csv("event_data.csv")

    # Auto-rename if username column is missing
    if 'username' not in user_df.columns:
        possible_cols = ['Name', 'User', 'user']
        for col in possible_cols:
            if col in user_df.columns:
                user_df.rename(columns={col:'username'}, inplace=True)
                break
        else:
            st.error("user_profiles.csv must have a 'username' column.")
    
    # Create favorites.csv if not exists
    if not os.path.exists("favorites.csv"):
        pd.DataFrame(columns=["username","item_type","item_name"]).to_csv("favorites.csv", index=False)
    return user_df, pg_df, food_df, event_df

user_df, pg_df, food_df, event_df = load_data()

# -------------------------
# MAIN APP
# -------------------------
if authentication_status:
    st.sidebar.success(f"Welcome {name}!")
    authenticator.logout("Logout", "sidebar")
    st.title("ConnectSphere 🌐")
    st.write("Find PGs, Food Places, and Events that match your preferences!")

    # --- Tabs ---
    tabs = st.tabs(["PGs 🏠", "Food 🍔", "Events 🎉", "Favorites ⭐"])

    # ---------------- FUNCTION TO ADD FAVORITE ----------------
    def add_favorite(username, item_type, item_name):
        fav_df = pd.read_csv("favorites.csv")
        if not ((fav_df['username']==username) & (fav_df['item_type']==item_type) & (fav_df['item_name']==item_name)).any():
            fav_df = pd.concat([fav_df, pd.DataFrame([{"username":username,"item_type":item_type,"item_name":item_name}])])
            fav_df.to_csv("favorites.csv", index=False)

    # ---------------- PG TAB ----------------
    with tabs[0]:
        st.subheader("Recommended PGs")
        search = st.text_input("Search PG by name or location")
        pg_recs = recommend_items(user_df, pg_df, username, item_type="PG")
        if search:
            pg_recs = pg_recs[pg_recs['name'].str.contains(search, case=False) | pg_recs['location'].str.contains(search, case=False)]
        for idx, row in pg_recs.iterrows():
            st.write(f"**{row['name']}** - {row['location']}")
            if st.button(f"⭐ Add {row['name']} to Favorites", key=f"pg_{idx}"):
                add_favorite(username, "PG", row['name'])
                st.success(f"{row['name']} added to favorites!")
            if 'latitude' in row and 'longitude' in row:
                m = folium.Map(location=[row['latitude'], row['longitude']], zoom_start=14)
                folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)
                folium_static(m)

    # ---------------- FOOD TAB ----------------
    with tabs[1]:
        st.subheader("Recommended Food Places")
        search = st.text_input("Search Food by name or location", key="food_search")
        food_recs = recommend_items(user_df, food_df, username, item_type="Food")
        if search:
            food_recs = food_recs[food_recs['name'].str.contains(search, case=False) | food_recs['location'].str.contains(search, case=False)]
        for idx, row in food_recs.iterrows():
            st.write(f"**{row['name']}** - {row['location']}")
            if st.button(f"⭐ Add {row['name']} to Favorites", key=f"food_{idx}"):
                add_favorite(username, "Food", row['name'])
                st.success(f"{row['name']} added to favorites!")
            if 'latitude' in row and 'longitude' in row:
                m = folium.Map(location=[row['latitude'], row['longitude']], zoom_start=14)
                folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)
                folium_static(m)

    # ---------------- EVENTS TAB ----------------
    with tabs[2]:
        st.subheader("Recommended Events")
        search = st.text_input("Search Events by name or location", key="event_search")
        event_recs = recommend_items(user_df, event_df, username, item_type="Event")
        if search:
            event_recs = event_recs[event_recs['name'].str.contains(search, case=False) | event_recs['location'].str.contains(search, case=False)]
        for idx, row in event_recs.iterrows():
            st.write(f"**{row['name']}** - {row['location']} - {row['date']}")
            if st.button(f"⭐ Add {row['name']} to Favorites", key=f"event_{idx}"):
                add_favorite(username, "Event", row['name'])
                st.success(f"{row['name']} added to favorites!")
            if 'latitude' in row and 'longitude' in row:
                m = folium.Map(location=[row['latitude'], row['longitude']], zoom_start=14)
                folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)
                folium_static(m)

    # ---------------- FAVORITES TAB ----------------
    with tabs[3]:
        st.subheader("My Favorites")
        fav_df = pd.read_csv("favorites.csv")
        user_favs = fav_df[fav_df['username']==username]
        if user_favs.empty:
            st.info("No favorites added yet!")
        else:
            for idx, row in user_favs.iterrows():
                st.write(f"**{row['item_name']}** ({row['item_type']})")

elif authentication_status == False:
    st.error("Username/password is incorrect")
else:
    st.warning("Please enter your username and password")
