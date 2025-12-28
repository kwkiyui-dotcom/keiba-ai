import numpy as np
import pandas as pd

class SynergyInsightEngine:
    """
    Synergy Insight Engine: 市場の非効率性（歪み）を検出するエンジン。
    認知バイアスやSmart Moneyの兆候を特定する。
    """
    def __init__(self):
        pass

    def detect_cognitive_bias(self, p_win, odds):
        """
        認知バイアスの検出:
        - アンカリング効果: 前走の着順に過剰に反応していないか
        - 利用可能性ヒューリスティック: 直近の目立つ出来事に引きずられていないか
        """
        # 期待勝率とオッズから示唆される勝率の乖離を計算
        implied_p = 1.0 / odds
        bias_score = p_win - implied_p
        
        bias_type = "None"
        if bias_score > 0.1:
            bias_type = "Underestimated (Value)"
        elif bias_score < -0.1:
            bias_type = "Overestimated (Hype)"
            
        return bias_score, bias_type

    def detect_smart_money(self, odds_history):
        """
        Smart Moneyの検出:
        締め切り間際の不自然なオッズ低下を検出する。
        """
        if len(odds_history) < 2:
            return 0.0, False
        
        # 直近のオッズ変化率
        change_rate = (odds_history[-1] - odds_history[0]) / odds_history[0]
        
        # 急激な低下（-15%以上など）をSmart Moneyの兆候とする
        is_smart_money = change_rate < -0.15
        return change_rate, is_smart_money

    def analyze_market_distortion(self, p_win_list, odds_list, odds_histories=None):
        """
        レース全体の市場歪みを分析
        """
        distortions = []
        for i, (p_win, odds) in enumerate(zip(p_win_list, odds_list)):
            bias_score, bias_type = self.detect_cognitive_bias(p_win, odds)
            
            smart_money_score = 0.0
            is_smart_money = False
            if odds_histories and i < len(odds_histories):
                smart_money_score, is_smart_money = self.detect_smart_money(odds_histories[i])
            
            distortions.append({
                'horse_index': i,
                'bias_score': bias_score,
                'bias_type': bias_type,
                'smart_money_score': smart_money_score,
                'is_smart_money': is_smart_money,
                'distortion_intensity': abs(bias_score) + (0.5 if is_smart_money else 0)
            })
            
        return distortions
