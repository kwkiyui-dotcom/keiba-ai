from flask import Flask, request, jsonify
import sys
import os

# パスを追加して各モジュールをインポート可能にする
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quant_engine.core import QuantCoreEngine
from synergy_engine.insight import SynergyInsightEngine
from arbitrager_module.arbitrager import ArbitragerModule
from portfolio_engine.optimizer import PortfolioOptimizationEngine

app = Flask(__name__)

# エンジンの初期化
quant_engine = QuantCoreEngine()
synergy_engine = SynergyInsightEngine()
arbitrager_module = ArbitragerModule()
portfolio_engine = PortfolioOptimizationEngine()

@app.route('/predict', methods=['POST'])
def predict():
    """
    レースデータを入力として受け取り、統合的な予測とポートフォリオを返す
    """
    data = request.json
    race_id = data.get('race_id')
    horses_data = data.get('horses') # リスト形式
    odds_list = [h['odds'] for h in horses_data]
    odds_histories = [h.get('odds_history', []) for h in horses_data]
    budget = data.get('budget', 10000)
    
    # 1. Quant Core Engine: 真の勝率予測
    # プロトタイプでは簡易的なDataFrameを作成
    import pandas as pd
    df = pd.DataFrame(horses_data)
    p_wins = quant_engine.predict_proba(df)
    
    # 2. Synergy Insight Engine: 市場歪み検出
    distortions = synergy_engine.analyze_market_distortion(p_wins, odds_list, odds_histories)
    
    # 3. Arbitrager Module: 投資機会特定
    # p_win を含めるように調整
    for i, dist in enumerate(distortions):
        dist['p_win'] = p_wins[i]
        dist['odds'] = odds_list[i]
        
    opportunities = arbitrager_module.process_race(p_wins, odds_list, distortions)
    
    # 4. Portfolio Optimization Engine: ポートフォリオ生成
    # opportunities に p_win と odds を追加して渡す
    for opp in opportunities:
        idx = opp['horse_index']
        opp['p_win'] = p_wins[idx]
        opp['odds'] = odds_list[idx]
        
    portfolio = portfolio_engine.generate_portfolio(opportunities, budget)
    
    return jsonify({
        'race_id': race_id,
        'opportunities': opportunities,
        'recommended_portfolio': portfolio
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'system': 'MH-AI UAS'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
