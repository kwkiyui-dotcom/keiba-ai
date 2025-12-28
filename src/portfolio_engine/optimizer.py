import numpy as np

class PortfolioOptimizationEngine:
    """
    Portfolio Optimization Engine: リスク調整型ポートフォリオの生成。
    ケリー基準を応用し、投資比率を最適化する。
    """
    def __init__(self, risk_tolerance=0.5):
        # risk_tolerance: 0.0 (保守的) から 1.0 (積極的、フルケリー)
        self.risk_tolerance = risk_tolerance

    def calculate_kelly_fraction(self, p_win, odds):
        """
        ケリー基準による投資比率の算出
        f* = (bp - q) / b = (p(b+1) - 1) / b
        b: オッズ - 1 (純利益率)
        p: 勝率
        q: 負ける確率 (1-p)
        """
        b = odds - 1
        if b <= 0: return 0.0
        
        f_star = (p_win * (b + 1) - 1) / b
        
        # リスク許容度による調整 (Fractional Kelly)
        return max(0, f_star * self.risk_tolerance)

    def generate_portfolio(self, opportunities, total_budget):
        """
        投資機会に基づき、具体的な買い目と投資額を算出する
        """
        portfolio = []
        total_fraction = 0
        
        # PLATINUM と GOLD を優先的に評価
        target_labels = ["PLATINUM", "GOLD", "SILVER"]
        
        for opp in opportunities:
            if opp['label'] in target_labels:
                # 簡易的な勝率推定（EV/Odds）
                p_win = opp['ev'] / (opp['ev'] / 0.1) # プロトタイプ用の仮定
                # 実際には QuantCoreEngine からの P_win を使うべきだが、
                # ここでは opp に含まれていると仮定するか、再計算する
                
                # プロトタイプ用: opp に p_win が含まれていない場合は ev と odds から逆算
                # 実際の実装では process_race で p_win も渡すようにする
                
                # ここでは仮に opp['p_win'] があるとする
                p_win = opp.get('p_win', 0.1) 
                odds = opp.get('odds', 10.0)
                
                fraction = self.calculate_kelly_fraction(p_win, odds)
                
                if fraction > 0:
                    amount = total_budget * fraction
                    portfolio.append({
                        'horse_index': opp['horse_index'],
                        'label': opp['label'],
                        'fraction': fraction,
                        'suggested_amount': round(amount, -2), # 100円単位
                        'reason': opp['reason']
                    })
                    total_fraction += fraction
                    
        # 合計投資比率が100%を超える場合の調整
        if total_fraction > 1.0:
            for item in portfolio:
                item['fraction'] /= total_fraction
                item['suggested_amount'] = round(total_budget * item['fraction'], -2)
                
        return portfolio
