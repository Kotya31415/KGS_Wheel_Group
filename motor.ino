#include <Dynamixel2Arduino.h>

#define DXL_SERIAL   Serial1
#define DEBUG_SERIAL Serial

Dynamixel2Arduino dxl(DXL_SERIAL, -1);

const uint8_t DXL_ID = 1;             
const uint32_t DXL_BAUDRATE = 57600;  
const float DXL_PROTOCOL_VERSION = 2.0;

const float VEL_UNIT = 0.229;  
const float POS_UNIT = 0.0879; 

const unsigned long RUN_DURATION_MS = 6000; 

// 時間と角度の基準点を保持する変数
unsigned long startTime = 0;
int32_t startPos_raw = 0; 

bool isRunning = false;
bool isStarted = false; 

void setup() {
  DEBUG_SERIAL.begin(115200);
  while (!DEBUG_SERIAL) { delay(10); }

  dxl.begin(DXL_BAUDRATE); 
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  delay(1000); 

  if (!dxl.ping(DXL_ID)) {
    DEBUG_SERIAL.println("[FAIL] Motor not found.");
    while (1) { delay(100); }
  }

  dxl.torqueOff(DXL_ID);
  dxl.setOperatingMode(DXL_ID, OP_VELOCITY);
  dxl.torqueOn(DXL_ID);

  DEBUG_SERIAL.println("System Ready. Waiting for 's' from PC..."); 
}

void loop() {
  // PCからの開始信号待ち
  if (DEBUG_SERIAL.available()) {
    char c = DEBUG_SERIAL.read();
    if (c == 's' || c == 'S') {
      isStarted = true;
      
      // 基準点（0地点）の記録
      startTime = millis();                          // 時刻の0地点
      startPos_raw = dxl.getPresentPosition(DXL_ID); // 角度の0地点
      
      isRunning = true;
      DEBUG_SERIAL.println("Time_ms, RPM, Position_deg"); // ヘッダー送信
    }
  }

  if (!isStarted) return; 
  if (!isRunning) return; 

  unsigned long currentTime = millis();
  
  // 経過時間（開始時点からの相対時間）
  unsigned long elapsedTime = currentTime - startTime; 

  if (elapsedTime < RUN_DURATION_MS) {
    float target_rpm = -30.0; 
    int32_t target_raw = (int32_t)(target_rpm / VEL_UNIT);
    dxl.setGoalVelocity(DXL_ID, target_raw);

    int32_t present_vel_raw = dxl.getPresentVelocity(DXL_ID);
    int32_t present_pos_raw = dxl.getPresentPosition(DXL_ID);
    
    // 相対角度の計算（現在位置 - 開始位置）
    int32_t relative_pos_raw = present_pos_raw - startPos_raw; 

    float rpm = present_vel_raw * VEL_UNIT;
    float position_deg = relative_pos_raw * POS_UNIT; // 相対角度を度に変換

    // シリアル出力（経過時間と相対角度）
    DEBUG_SERIAL.print(elapsedTime); 
    DEBUG_SERIAL.print(",");
    DEBUG_SERIAL.print(rpm);
    DEBUG_SERIAL.print(",");
    DEBUG_SERIAL.println(position_deg);

    delay(50); 
  } 
  else {
    dxl.setGoalVelocity(DXL_ID, 0); 
    DEBUG_SERIAL.println(">>> 6 seconds passed. Logging finished.");
    isRunning = false; 
  }
}