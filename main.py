import requests
import pandas as pd
from datetime import datetime
import os
import sys

def fetch_and_save_leaderboard():
    # זו הכתובת היציבה ביותר של ה-Leaderboard נכון לעכשיו
    url = "https://gamma-api.polymarket.com/events/leaderboard?limit=50&window=24h"
    
    # הוספת Headers כדי להיראות כמו דפדפן אמיתי ולמנוע חסימות
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Origin": "https://polymarket.com",
        "Referer": "https://polymarket.com/"
    }
    
    try:
        print(f"Connecting to: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        
        # אם יש שגיאה (404, 403, וכו'), זה יזרוק חריגה
        response.raise_for_status()
        
        data = response.json()
        
        # בכתובת הזו הנתונים בדרך כלל מגיעים כרשימה ישירה
        if not data or len(data) == 0:
            print("Error: Received empty data from API.")
            sys.exit(1)
            
        df = pd.DataFrame(data)
        df['snapshot_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # בניית לינקים לפי השדות הקיימים ב-Gamma API
        # בדרך כלל השדה הוא 'proxyAddress' או 'user'
        user_col = 'proxyAddress' if 'proxyAddress' in df.columns else ('user' if 'user' in df.columns else None)
        
        if user_col:
            df['profile_link'] = df[user_col].apply(lambda x: f"https://polymarket.com/profile/{x}")
        
        file_path = 'daily_winners.csv'
        
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, index=False)
            
        print(f"Success! Saved {len(df)} records.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        # מוודא שה-GitHub Action יסומן ב-X אדום
        sys.exit(1)

if __name__ == "__main__":
    fetch_and_save_leaderboard()
