import requests
import pandas as pd
from datetime import datetime
import os
import sys

def fetch_and_save_leaderboard():
    # הכתובת המאומתת
    url = "https://gamma-api.polymarket.com/leaderboard"
    
    # הפרמטרים שפולימרקט דורשת כיום כדי לא להחזיר 422
    params = {
        "window": "24h",
        "column": "pnl",  # קריטי: מגדיר שאנחנו מחפשים הצלחה (רווח)
        "limit": 50
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://polymarket.com/"
    }
    
    try:
        print(f"Connecting to: {url}")
        response = requests.get(url, headers=headers, params=params, timeout=20)
        
        # אם השרת מחזיר שגיאה, נדפיס את התוכן שלה לפני שנקרוס
        if response.status_code != 200:
            print(f"Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            response.raise_for_status()
            
        data = response.json()
        
        # ה-API מחזיר רשימה של אובייקטים
        if not data or not isinstance(data, list):
            print("Error: API returned empty or invalid data format.")
            sys.exit(1)
            
        df = pd.DataFrame(data)
        
        # הוספת נתוני זמן ולינקים
        df['snapshot_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # ב-Gamma API העמודה לכתובת הארנק היא 'proxyAddress'
        if 'proxyAddress' in df.columns:
            df['profile_link'] = df['proxyAddress'].apply(lambda x: f"https://polymarket.com/profile/{x}")
        
        file_path = 'daily_winners.csv'
        
        # שמירה לקובץ (מניח שהקובץ קיים ב-Repo כפי שיצרת)
        if os.path.exists(file_path):
            # מוודא שסדר העמודות נשמר
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, index=False)
            
        print(f"Success! {len(df)} traders recorded.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1) # מכשיל את ה-Action בגיטהאב

if __name__ == "__main__":
    fetch_and_save_leaderboard()
