import csv
import math
import glob
import os

# 数字だけのファイル名を持つCSVを検索
files = glob.glob("[0-9]*.csv")

files = [
    f for f in files
    if os.path.splitext(os.path.basename(f))[0].isdigit()
]

if not files:
    print("数字のファイル名のCSVが見つかりません。")
    exit()

# ファイルを選択
print("読み込めるCSVファイル:")
for i, file in enumerate(files, 1):
    print(f"{i}: {file}")

choice = int(input("ファイル番号を選択してください: "))
filename = files[choice - 1]

# CSV読み込み
with open(filename, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    rows = list(reader)

    if not rows:
        raise ValueError("CSVにデータがありません。")

    # Position_deg列を検索（空白にも対応）
    column = next(
        (c for c in reader.fieldnames if c.strip() == "Position_deg"),
        None
    )

    if column is None:
        raise ValueError("Position_deg列が見つかりません。")

    last_position = float(rows[-1][column])

# 計算
denominator = 6 * math.pi * abs(last_position) / 360

value = float(input("計算する数値を入力してください: "))
result = 1 - (value / denominator)

# 結果表示
print(f"\n読み込みファイル: {filename}")
print(f"Position_deg最終値: {last_position}")
print(f"分母: {denominator:.6f}")
print(f"計算結果: {result:.6f}")
