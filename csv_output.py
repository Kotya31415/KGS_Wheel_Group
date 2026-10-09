import serial
import csv
import time

# 設定
COM_PORT = 'COM4'  # あなたの環境のポート名に変更してください
BAUD_RATE = 115200
CSV_FILE = 'motor_data.csv'

print(f"{COM_PORT} に接続します。")

# シリアルポートを開く
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
time.sleep(2) # Arduinoの初期化待ち

try:
    # Arduinoに開始信号（'s'）を送信
    print("Arduinoに開始信号を送信します...")
    ser.write(b's')
    
    # ヘッダーが送られてくるまで少し待つ
    time.sleep(0.5)

    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        print(f"データ取得開始。{CSV_FILE} に保存します。")
        
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # ">>>" で始まる終了メッセージが来たらループを抜ける
                if line.startswith(">>>"):
                    print(line)
                    break
                
                data = line.split(',')
                if len(data) == 3:
                    writer.writerow(data)
                    # print(f"取得: {data}") # 必要に応じてコメントアウト解除
                    
    print("6秒間のデータ取得が完了しました。")

except KeyboardInterrupt:
    print("\nデータ取得を手動で停止しました。")
finally:
    ser.close()
    print(f"シリアルポートを閉じました。{CSV_FILE} を確認してください。")