import requests
import pandas as pd
from datetime import datetime
import os

def fetch_and_save_leaderboard():
    # הכתובת המעודכנת של ה-Leaderboard
    url = "https://activity-api.polymarket.com/leaderboard?limit=50&window=24h"
    
    try:
        print(f"Connecting to: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        # ב-API הזה הנתונים נמצאים תחת המפתח 'data' או שהם מגיעים כרשימה ישירה
        data = response.json()
        
        # תלוי במבנה ה-API, לפעמים זה רשימה ולפעמים דיקט
        if isinstance(data, dict) and 'data' in data:
            data = data['data']
            
        df = pd.DataFrame(data)
        
        if df.empty:
            print("No data found.")
            return

        df['snapshot_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # שם העמודה ב-API החדש הוא 'user' או 'address'
        # ננסה לזהות את הכתובת כדי ליצור לינק
        addr_col = 'user' if 'user' in df.columns else 'proxyAddress'
        if addr_col in df.columns:
            df['profile_link'] = df[addr_col].apply(lambda x: f"https://polymarket.com/profile/{x}")
        
        file_path = 'daily_winners.csv'
        
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, index=False)
            
        print(f"Successfully saved {len(df)} records to {file_path}")
        
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    fetch_and_save_leaderboard()
