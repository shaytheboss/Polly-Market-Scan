import requests
import pandas as pd
from datetime import datetime
import os

def fetch_and_save_leaderboard():
    # שליפת הנתונים מה-API הציבורי של פולימרקט
    url = "https://gamma-api.polymarket.com/leaderboard?limit=50&window=daily"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data)
        
        # הוספת חותמת זמן של הבדיקה
        df['snapshot_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # יצירת לינק ישיר לפרופיל המשתמש לצורך מעקב מהיר
        # הכתובת ב-Polymarket בנויה מה-proxyAddress של המשתמש
        df['profile_link'] = df['proxyAddress'].apply(lambda x: f"https://polymarket.com/profile/{x}")
        
        # סידור העמודות כך שהלינק יהיה בולט
        cols = ['snapshot_date', 'rank', 'pnl', 'volume', 'profile_link', 'proxyAddress']
        df = df[cols]
        
        file_path = 'daily_winners.csv'
        
        # שמירה או הוספה לקובץ קיים
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, index=False)
            
        print(f"נשמרו {len(df)} רשומות בהצלחה.")
        
    except Exception as e:
        print(f"אירעה שגיאה: {e}")

if __name__ == "__main__":
    fetch_and_save_leaderboard()
