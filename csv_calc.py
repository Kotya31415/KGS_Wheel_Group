import csv
import math

# CSVファイルを読み込む
with open("1.csv", "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    # 最後のPosition_degを取得
    rows = list(reader)
    last_position = float(rows[-1][" Position_deg"].strip())

# 分母を計算
denominator = 6 * math.pi * abs(last_position) / 360

# ユーザー入力
value = float(input("計算する数値を入力してください: "))

# 計算
result = value / denominator

print(f"\nPosition_deg 最終値: {last_position}")
print(f"分母: {denominator:.6f}")
print(f"計算結果: {result:.6f}")
