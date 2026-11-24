import json
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # gốc repo kdgw-nntm
FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FD + "DejaVuSans.ttf")); pdfmetrics.registerFont(TTFont("DVB", FD + "DejaVuSans-Bold.ttf"))
P = json.load(open(R + "/profile.json"))
COL = {"TT": "#2e9d4e", "CN": "#e07b24", "TS": "#1f78c8", "NL": "#c99400", "DK": "#7b4fb0", "": "#9a9a9a"}
S = ParagraphStyle("s", fontName="DV", fontSize=7.8, leading=9.6)
SW = ParagraphStyle("w", fontName="DVB", fontSize=8, leading=10, textColor=colors.white)
c = canvas.Canvas(R + "/docs/NNTM_Bo-cam-bien-va-dau-noi_v1.1.pdf")
c.setTitle("NNTM – Bộ cảm biến, thiết bị và sơ đồ đấu nối KD-GW")

def table_page(rows, title, sub):
    c.setPageSize(landscape(A4)); W, H = landscape(A4)
    c.setFont("DVB", 15); c.drawString(12 * mm, H - 14 * mm, title)
    c.setFont("DV", 9); c.drawString(12 * mm, H - 20 * mm, sub)
    data = [[Paragraph(h, SW) for h in ["Cổng", "Nhãn trên vỏ", "Khu", "Thiết bị đề xuất", "Nguồn", "Ghi chú lắp đặt"]]]
    st = [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f5d8a")), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#999")),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]
    for i, p in enumerate(rows, 1):
        data.append([Paragraph(f"<b>{p['port']}</b>", S), Paragraph(p["label"], S), Paragraph(P["zones"].get(p["zone"], "—"), S),
                     Paragraph(p["device"], S), Paragraph(p["power"] or "—", S), Paragraph(p["note"] or "", S)])
        cc = colors.HexColor(COL[p["zone"]])
        tint = colors.Color(1 - (1 - cc.red) * 0.25, 1 - (1 - cc.green) * 0.25, 1 - (1 - cc.blue) * 0.25)
        st.append(("BACKGROUND", (2, i), (2, i), tint if p["zone"] else colors.HexColor("#eeeeee")))
    t = Table(data, colWidths=[16 * mm, 30 * mm, 26 * mm, 95 * mm, 32 * mm, 70 * mm], repeatRows=1)
    t.setStyle(TableStyle(st)); w, h = t.wrap(W, H); t.drawOn(c, 12 * mm, H - 26 * mm - h); c.showPage()

ports = P["ports"]
table_page([p for p in ports if not p["port"].startswith("RLY")], "NNTM – Cảm biến và thiết bị theo cổng KD-GW (1/2)",
           "Cổng chung của KD-GW v1.2 được đặt tên theo dự án Nông nghiệp thông minh. Nhãn trên vỏ khắc đúng cột 'Nhãn trên vỏ'.")
table_page([p for p in ports if p["port"].startswith("RLY")], "NNTM – Tải đóng cắt qua relay + mạng & nguồn (2/2)",
           "Relay Songle SRD-05VDC-SL-C: tải 12V DC đi qua tiếp điểm COM–NO. Dùng 1 module relay (RLY1–8); RLY9–16 để trống.")
# ghi chú mạng/nguồn ở cuối trang 2 (vẽ trên trang mới gọn hơn)
c.setPageSize(landscape(A4)); W, H = landscape(A4)
c.setFont("DVB", 15); c.drawString(12 * mm, H - 14 * mm, "NNTM – Nguồn, mạng và lưu ý")
lines = [
 ("Nguồn", P["network"]["power"] + ". Tải 12V (bơm, quạt, đèn, còi) lấy trực tiếp từ ắc quy qua cầu chì riêng 10 A, không đi qua jack gateway."),
 ("Ước tính dòng 12V", "Gateway ~0.5 A; bơm 4 × 0.4 A; sục khí 0.3 A; van 0.3 A; đèn sưởi ~1 A; quạt 0.3 A; LED trồng ~1 A; đèn báo + còi 0.5 A → tối đa ~5.5 A khi bật cùng lúc."),
 ("Mạng", P["network"]["LAN"] + "."),
 ("Camera", P["network"]["camera"] + "."),
 ("Cảm biến 5V", "MQ-135 và YF-S201 lấy 5V từ cổng 3V3/5V/G. Ngõ ra MQ-135 phải qua cầu chia áp 10k/20k trước khi vào AI5 (ESP32 chỉ chịu 3.3V). YF-S201 đã có điện trở hạn dòng + diode kẹp trên mạch."),
 ("I2C", "Dùng hub I2C 4 cổng. SHT31 chuồng gà nối chân ADDR lên VCC để đổi địa chỉ 0x45. Tổng chiều dài dây I2C ≤ 1.5 m, chạy 100 kHz."),
 ("Cảm biến nước", "pH và DO cần hiệu chuẩn trước khi dùng; tháo đầu dò pH ngâm dung dịch bảo quản khi không dùng lâu. DO (AI4) giá cao – có thể lắp sau."),
 ("Nhãn vỏ", "Mọi chữ trên vỏ là chữ IN NỔI 0.6 mm: tên dự án trên nắp lõi, tên cổng trên vách, tên 8 relay trên nắp relay. In nắp đặt ngửa, không cần support; lớp 0.12 mm. Muốn chữ khác màu: đổi nhựa ở z = 4.0 mm khi in nắp."),
]
y = H - 26 * mm
for k, v in lines:
    p = Paragraph(f"<b>{k}:</b> {v}", ParagraphStyle("n", fontName="DV", fontSize=10, leading=14))
    w, h = p.wrap(W - 24 * mm, H); p.drawOn(c, 12 * mm, y - h); y -= h + 4 * mm
c.showPage()
for img, title in ((R + "/docs/nntm_wiring.png", "Sơ đồ đấu nối vào hộp gateway (nhìn từ trên xuống)"), (R + "/docs/nntm_lap_dat_3d.png", "Mô phỏng 3D cắm dây vào hộp")):
    c.setPageSize(landscape(A3)); W, H = landscape(A3)
    from reportlab.lib.utils import ImageReader
    ir = ImageReader(img); iw, ih = ir.getSize()
    s = min((W - 20 * mm) / iw, (H - 30 * mm) / ih)
    c.setFont("DVB", 14); c.drawString(10 * mm, H - 12 * mm, "NNTM – " + title)
    c.drawImage(ir, 10 * mm, H - 18 * mm - ih * s, iw * s, ih * s); c.showPage()
c.save(); print("ok")
