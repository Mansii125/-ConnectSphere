import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base  # Assuming models.py has User model defined

# Step 1: Connect to DB
engine = create_engine('sqlite:///connectsphere.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Step 2: Load your CSV
df_users = pd.read_csv('users.csv')

# Optional: Show columns for debug
print("Loaded columns:", df_users.columns)

# Step 3: Insert rows into DB
for _, row in df_users.iterrows():
    session.add(User(
        name=row['Name'],
        profession=row['Profession'],
        city=row['City'],
        state=row['State'],
        language=row['Language'],
        food=row['Food']
    ))

session.commit()
print("Users loaded successfully!")

