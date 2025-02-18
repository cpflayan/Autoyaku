import ccxt
import pandas as pd
import time

# === 🟢 設定參數 ===
symbol = 'BTC/USDT'   # 交易對
timeframe = '1h'      # K 線時間周期（選擇 '1m', '5m', '15m', '1h', '4h', '1d'）
start_date = '2010-01-01T00:00:00Z'  # 起始時間（UTC）
end_date = '2025-01-01T00:00:00Z'    # 結束時間（UTC）
save_path = f'binance_{symbol.replace("/", "")}_{timeframe}.csv'  # 儲存檔案名稱

# === 🟢 連接 Binance API ===
exchange = ccxt.binance()

# 轉換時間格式
since = exchange.parse8601(start_date)
end_time = exchange.parse8601(end_date)

# 記錄下載的 K 線數據
all_klines = []

# === 🔵 下載 K 線數據 ===
while since < end_time:
    try:
        # 🟠 下載 1000 根 K 線數據（Binance 限制）
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit=1000)

        if not ohlcv:
            break  # 沒有更多數據，停止

        all_klines.extend(ohlcv)

        # ✅ 更新下一次下載的起始時間（+1 ms 避免重複）
        since = ohlcv[-1][0] + 1

        # 🌟 避免 API 過載（幣安請求速率限制）
        time.sleep(0.5)

    except Exception as e:
        print(f"⚠️ 下載失敗，錯誤：{e}，5 秒後重試...")
        time.sleep(5)

# === 🟢 轉換為 DataFrame ===
df = pd.DataFrame(all_klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # 轉換時間格式
df.set_index('timestamp', inplace=True)  # 設定時間索引

# === 🔵 數據清理（檢查缺失值並補全） ===
df = df[~df.index.duplicated(keep='first')]  # 刪除重複時間戳
df = df.resample(timeframe).ffill()  # 確保時間序列完整，缺失數據向前填補

# === 🟢 儲存數據 ===
df.to_csv(save_path)
print(f"✅ K 線數據下載完成，儲存至 {save_path}")
