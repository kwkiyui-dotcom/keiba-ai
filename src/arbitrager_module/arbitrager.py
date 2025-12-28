class ArbitragerModule:
    """
    Arbitrager Module: 期待値 (EV) と市場の歪みを統合し、投資機会を特定する。
    PLATINUM, GOLD, SILVER, BRONZE のラベリングを行う。
    """
    def __init__(self):
        pass

    def calculate_ev(self, p_win, odds):
        """期待値の算出"""
        return p_win * odds

    def evaluate_opportunity(self, p_win, odds, distortion_info):
        """
        投資機会の総合評価とラベリング
        """
        ev = self.calculate_ev(p_win, odds)
        intensity = distortion_info['distortion_intensity']
        is_smart_money = distortion_info['is_smart_money']
        
        # レースバリューインデックス (RVI) の簡易計算
        rvi = ev * (1 + intensity)
        
        label = "BRONZE"
        reason = "Standard opportunity"
        
        if ev > 2.0 and intensity > 0.5:
            label = "PLATINUM"
            reason = "High EV with significant market distortion"
        elif ev > 1.5 and (intensity > 0.3 or is_smart_money):
            label = "GOLD"
            reason = "Solid EV with clear bias or smart money"
        elif ev > 1.2:
            label = "SILVER"
            reason = "Moderate EV"
            
        if is_smart_money:
            reason += " + Smart Money detected"
            
        return {
            'ev': ev,
            'rvi': rvi,
            'label': label,
            'reason': reason
        }

    def process_race(self, p_wins, odds_list, distortions):
        """
        レース内の全馬を評価し、投資機会をリスト化する
        """
        opportunities = []
        for i, (p_win, odds, distortion) in enumerate(zip(p_wins, odds_list, distortions)):
            opp = self.evaluate_opportunity(p_win, odds, distortion)
            opp['horse_index'] = i
            opportunities.append(opp)
            
        # 期待値順にソート
        opportunities.sort(key=lambda x: x['ev'], reverse=True)
        return opportunities
