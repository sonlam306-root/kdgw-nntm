# Nông nghiệp thông minh vì tương lai xanh — bảng cổng KD-GW

Phần cứng: **KD-GW-HW-v1.2** (không sửa). Dự án: `nntm`. Trạng thái profile: **đã duyệt**.

| Cổng | Loại | Nhãn trên vỏ | Khu | Thiết bị | Nguồn | Ghi chú |
|---|---|---|---|---|---|---|
| AI1 | analog | ẨM ĐẤT | Trồng trọt | Cảm biến độ ẩm đất điện dung v1.2 | 3V3 | Cắm vào giá thể luống tưới |
| AI2 | analog | TDS | Trồng trọt | DFRobot Gravity TDS (dinh dưỡng thủy canh) | 3V3 | Đầu dò trong bể dung dịch thủy canh |
| AI3 | analog | pH | Thủy sản | DFRobot Gravity pH V2 | 3V3 | Hiệu chuẩn pH 4.0 / 7.0 |
| AI4 | analog | DO | Thủy sản | DFRobot Gravity DO (oxy hòa tan) – tuỳ chọn | 3V3 | Giá cao; có thể lắp sau |
| AI5 | analog | KHÍ | Chăn nuôi | MQ-135 (khí NH3/khí độc chuồng) | 5V (rail) + chia áp 10k/20k | Lấy 5V từ cổng 3V3/5V/G; ngõ ra qua cầu chia áp |
| AI6 | analog | DP | — | Trống | — |  |
| OW | 1wire | T°NƯỚC | Thủy sản | DS18B20 chống nước ×2 (bể cá, bể thủy canh) | 3V3 | 2 cảm biến chung 1 dây |
| LOAD | hx711 | CÂN | Chăn nuôi | Load cell 1 kg dưới máng ăn | E+ 4.3V | Biết lượng thức ăn còn lại |
| DI1 | digital_in | 1 | Trạm điều khiển | Nút TRỒNG TRỌT | — | Nút nhấn tiếp điểm khô |
| DI2 | digital_in | 2 | Trạm điều khiển | Nút CHĂN NUÔI | — |  |
| DI3 | digital_in | 3 | Trạm điều khiển | Nút THỦY SẢN | — |  |
| DI4 | digital_in | 4 | Trạm điều khiển | Nút TẮT/BẬT TỔNG | — | Nút nấm có khoá |
| DI5 | digital_in | 5 | Thủy sản | Phao mực nước bể cá – THẤP | — | Phao từ tiếp điểm khô |
| DI6 | digital_in | 6 | Thủy sản | Phao mực nước bể cá – CAO | — |  |
| DI7 | digital_in | 7 | Trồng trọt | Phao bể dung dịch thủy canh – THẤP | — | Chống bơm chạy khô |
| DI8 | digital_in | 8 | Chăn nuôi | Phao máng uống gà | — |  |
| DI-F | pulse_in | L.LƯỢNG | Trồng trọt | Cảm biến lưu lượng YF-S201 (đường tưới) | 5V (rail) | Đo nước tưới tiêu thụ |
| RS485 | modbus_rtu | DỰ PHÒNG | — | Dự phòng: cảm biến đất NPK Modbus | — |  |
| PWR1 | pwm_12v | QUẠT | Chăn nuôi | Quạt thông gió 12V (chỉnh tốc độ theo nhiệt độ) | 12V PWM |  |
| PWR2 | pwm_12v | LED | Trồng trọt | LED dây trồng cây 12V (chỉnh độ sáng) | 12V PWM |  |
| SERVO | servo | MÁNG ĂN | Chăn nuôi | Servo MG90S mở cửa máng ăn | 5V |  |
| I2C | i2c | I2C | — | Hub I2C 4 cổng: SHT31 nhà kính (0x44), SHT31 chuồng gà (0x45), BH1750 ánh sáng (0x23), INA226 trạm năng lượng (0x40) | 3V3 | Dây I2C ≤ 1.5 m |
| RLY1 | relay | BƠM TƯỚI | Trồng trọt | Bơm tưới nhỏ giọt 12V | 12V |  |
| RLY2 | relay | BƠM THỦY CANH | Trồng trọt | Bơm tuần hoàn thủy canh 12V | 12V |  |
| RLY3 | relay | BƠM LỌC | Thủy sản | Bơm lọc / tuần hoàn bể cá 12V | 12V |  |
| RLY4 | relay | SỤC KHÍ | Thủy sản | Máy sục khí 12V | 12V |  |
| RLY5 | relay | NƯỚC UỐNG | Chăn nuôi | Van điện từ / bơm mini cấp máng uống 12V | 12V |  |
| RLY6 | relay | ĐÈN SƯỞI | Chăn nuôi | Đèn sưởi chuồng gà 12V | 12V |  |
| RLY7 | relay | ĐÈN BÁO | Trạm điều khiển | Đèn xoay cảnh báo 12V | 12V |  |
| RLY8 | relay | CÒI HÚ | Trạm điều khiển | Còi hú 12V | 12V |  |

Cổng chưa dùng: không có

## Mạng, camera, nguồn

- **LAN:** Switch/router → Raspberry Pi 5 (edge, chạy dashboard + màn hình 7" ở trạm điều khiển) → VPS
- **camera:** Camera đếm gà (ESP32-CAM hoặc webcam USB trên Pi 5) – luồng RTSP thẳng lên Pi 5, không qua gateway
- **power:** Pin mặt trời 12V 30W → bộ sạc 10A → ắc quy 12V 7Ah → cầu chì → jack 12V gateway + nguồn 12V cho tải qua relay
