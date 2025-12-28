# MH-AI: Ultimate Arbitrage System (UAS)

## 概要
「Synergy」と「Quant」の融合による、次世代統合競馬予想システム。市場の非効率性（歪み）を最大限に活用し、リスク調整された高回収率を長期的に実現することを目指します。

## システムアーキテクチャ
1. **Quant Core Engine**: 真の勝利確率 (P_win) の予測。
2. **Synergy Insight Engine**: 市場の歪み（認知バイアス、Smart Money）の検出。
3. **Arbitrager Module**: 期待値 (EV) とレースバリューインデックス (RVI) に基づく投資機会の特定。
4. **Portfolio Optimization Engine**: ケリー基準を用いたリスク調整型ポートフォリオの生成。
5. **API Gateway / Flask API**: 各エンジンを統合するインターフェース。

## ディレクトリ構造
- `src/`: ソースコード
  - `quant_engine/`: 量的分析モジュール
  - `synergy_engine/`: 質的分析モジュール
  - `arbitrager_module/`: 投資機会特定モジュール
  - `portfolio_engine/`: 資金管理モジュール
  - `api_gateway/`: APIインターフェース
- `data/`: データレイク
- `docs/`: 設計書・ドキュメント
- `tests/`: テストコード
