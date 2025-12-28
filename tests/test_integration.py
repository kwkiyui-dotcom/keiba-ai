import requests
import json
import time
import subprocess
import os

def run_test():
    # APIサーバーをバックグラウンドで起動
    print("Starting API server...")
    server_process = subprocess.Popen(
        ["python3", "src/api_gateway/app.py"],
        cwd="/home/ubuntu/keiba-ai",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # サーバーの起動を待つ
    for i in range(10):
        try:
            requests.get("http://localhost:5000/health")
            print("Server is up!")
            break
        except:
            print(f"Waiting for server... ({i+1}/10)")
            time.sleep(2)
    
    try:
        # テストデータ
        test_data = {
            "race_id": "202512280101",
            "budget": 50000,
            "horses": [
                {"name": "Horse A", "odds": 2.5, "last_rank": 1, "last_popularity": 1, "odds_history": [2.8, 2.6, 2.5]},
                {"name": "Horse B", "odds": 15.0, "last_rank": 8, "last_popularity": 3, "odds_history": [20.0, 18.0, 15.0]}, # Smart Money?
                {"name": "Horse C", "odds": 5.0, "last_rank": 2, "last_popularity": 2, "odds_history": [5.0, 5.0, 5.0]},
                {"name": "Horse D", "odds": 50.0, "last_rank": 12, "last_popularity": 10, "odds_history": [60.0, 55.0, 50.0]}
            ]
        }
        
        print("Sending request to /predict...")
        response = requests.post("http://localhost:5000/predict", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("Test Passed!")
            print(f"Race ID: {result['race_id']}")
            print("\nOpportunities:")
            for opp in result['opportunities']:
                print(f"  Horse {opp['horse_index']}: Label={opp['label']}, EV={opp['ev']:.2f}, Reason={opp['reason']}")
            
            print("\nRecommended Portfolio:")
            for item in result['recommended_portfolio']:
                print(f"  Horse {item['horse_index']}: Amount={item['suggested_amount']} yen ({item['label']})")
        else:
            print(f"Test Failed with status code: {response.status_code}")
            print(response.text)
            
    finally:
        # サーバーを停止
        server_process.terminate()
        print("API server stopped.")

if __name__ == "__main__":
    run_test()
