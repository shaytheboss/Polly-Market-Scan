import requests
import pandas as pd
from datetime import datetime
import os
import sys

def fetch_and_save_leaderboard():
    # זו הכתובת החדשה והפעילה שהאתר משתמש בה כרגע ל-Leaderboard
    url = "https://leaderboard-api.polymarket.com/leaderboard"
    
    # הפרמטרים המדויקים שהדפדפן שולח
    params = {
        "window": "24h",
        "limit": 50,
        "type": "profit" # שים לב: כאן זה נקרא 'type' ולא 'column'
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://polymarket.com",
        "Referer": "https://polymarket.com/"
    }
    
    try:
        print(f"Connecting to: {url}")
        # פולימרקט משתמשים ב-API הזה תחת דומיין ייעודי
        response = requests.get(url, headers=headers, params=params, timeout=20)
        
        if response.status_code != 200:
            print(f"Failed! Status: {response.status_code}")
            print(f"Body: {response.text}")
            response.raise_for_status()
            
        data = response.json()
        
        # המבנה החדש מחזיר אובייקט עם שדה בשם 'data' או רשימה ישירה
        leaderboard_list = data.get('data', data) if isinstance(data, dict) else data
        
        if not leaderboard_list:
            print("Error: No data in response.")
            sys.exit(1)
            
        df = pd.DataFrame(leaderboard_list)
        df['snapshot_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # בכתובת הזו השדה לרוב נקרא 'address' או 'id'
        addr_col = 'address' if 'address' in df.columns else 'name'
        if addr_col in df.columns:
            df['profile_link'] = df[addr_col].apply(lambda x: f"https://polymarket.com/profile/{x}")
        
        file_path = 'daily_winners.csv'
        
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, index=False)
            
        print(f"Success! Captured {len(df)} top traders.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_and_save_leaderboard()
