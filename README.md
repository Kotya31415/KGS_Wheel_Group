# KGS_Wheel_Group

## 概要

OpenRB-150 で Dynamixel モーターを駆動し、PC 側の Python スクリプトで速度・位置データを取得して `motor_data.csv` に保存します。

## 必要な依存関係

### PC（Python）

- Python 3.10 以降
- [pyserial](https://pypi.org/project/pyserial/)（3.5 以降推奨）  
  Python から OpenRB-150 のシリアルポートへ接続するために使用します。
- `csv`、`time`  
  Python 標準ライブラリのため、追加インストールは不要です。

インストール:

```bash
python -m pip install pyserial
```

### Arduino

- Arduino IDE
- Arduino IDE のライブラリマネージャーから **Dynamixel2Arduino** をインストール  
  OpenRB-150 から Dynamixel モーターを制御するために使用します。
- Dynamixel モーター、電源、USB 接続

## 実行方法

1. `motor.ino` を Arduino IDE で開き、ボードへ書き込みます。
2. `csv_output.py` の `COM_PORT` を OpenRB-150 が接続されているポート（例: `COM4`）に変更します。
3. OpenRB-150 を接続した状態で、次のコマンドを実行します。

```bash
python csv_output.py
```

4. OpenRB-150 から6秒間分のデータを取得し、`motor_data.csv` に保存します。

OpenRB-150 と Dynamixel の通信速度は `motor.ino` の `DXL_BAUDRATE`、PC と OpenRB-150 の通信速度は `BAUD_RATE` で設定されています。接続する機器の設定と一致させてください。
