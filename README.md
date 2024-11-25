# Pygame 遊戲合集

這是一個使用Python和Pygame開發的遊戲合集，包含多個經典小遊戲。

## 遊戲列表

1. **五子棋 (Gomoku)**
   - 人機對戰
   - 支持繁體中文界面
   - 實時遊戲統計
   - 功能：
     - 新局開始
     - 投降功能
     - 遊戲記錄
     - 勝率統計

2. **貪吃蛇 (GluttonousSnake)**
   - 經典貪吃蛇遊戲
   - 支持速度調整
   - 即時得分顯示

3. **踩地雷 (MineSweeping)**
   - 經典踩地雷遊戲
   - 支持繁體中文界面
   - 功能：
     - 多種難度選擇
     - 計時功能
     - 剩餘地雷計數
   - 操作說明：
     - 左鍵：打開格子
     - 右鍵：標記地雷（旗幟）/問號
     - 左右鍵同時按：快速打開周圍格子
     - 笑臉按鈕：返回選單

4. **俄羅斯方塊 (Tetris)**
   - 經典俄羅斯方塊
   - 支持速度調整
   - 即時得分顯示

## 安裝要求

```bash
pip install -r requirements.txt
```

## 運行環境
- Python 3.8+
- Pygame 2.5.2
- Windows作業系統（推薦Windows 10/11）

## 遊戲操作說明

### 五子棋
- 滑鼠左鍵：落子
- 按鈕功能：
  - 再來一局：開始新的遊戲
  - 棄權投降：結束當前局並認輸
  - 結束：退出遊戲
- 右側面板顯示：
  - 當前局步數統計
  - 黑白方步數
  - 總局數
  - 勝率統計

### 貪吃蛇
- 方向鍵：控制蛇的移動方向
- 遊戲界面顯示當前速度和得分

### 踩地雷
- 滑鼠左鍵：翻開方塊
- 滑鼠右鍵：標記地雷

### 俄羅斯方塊
- 方向鍵：控制方塊移動和旋轉
- 遊戲界面顯示下一個方塊和當前得分

## 開發說明
- 使用Pygame遊戲引擎開發
- 支持繁體中文界面
- 使用microsoftyaheiui字體確保中文顯示
- 模組化設計，便於維護和擴展

## 貢獻
歡迎提交Issue和Pull Request來改進遊戲。

## 授權
本項目採用MIT授權協議。
