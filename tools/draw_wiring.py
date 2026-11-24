"""Sơ đồ đấu nối NNTM vào hộp gateway KD-GW (nhìn từ trên xuống, mép sau ở trên)."""
import json, html
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # gốc repo kdgw-nntm
P = json.load(open(R + "/profile.json"))
PORTS = json.load(open(R + "/kdgw-hardware/hardware/KD-GW-HW-v1.2/ports/kdgw_main_ports.json"))
info = {p["port"]: p for p in P["ports"]}
COL = {"TT": "#2e9d4e", "CN": "#e07b24", "TS": "#1f78c8", "NL": "#c99400", "DK": "#7b4fb0", "": "#9a9a9a", "NET": "#444444"}
W, H = 2800, 1900
S, X0, Y0 = 4.0, 1050, 760          # 4 px/mm; góc PCB lõi
def bx(lx): return X0 + lx * S
def by(ly): return Y0 + 400 - ly * S
o = []
def esc(t): return html.escape(t)
def text(x, y, t, size=20, col="#222", w="normal", anchor="middle"):
    o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="DejaVu Sans" font-size="{size}" fill="{col}" font-weight="{w}" text-anchor="{anchor}">{esc(t)}</text>')
def box(cx, cy, w, h, col, lines, fill=None):
    o.append(f'<rect x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w}" height="{h}" rx="12" fill="{fill or "#ffffff"}" stroke="{col}" stroke-width="3"/>')
    n = len(lines)
    for i, (t, sz, wt) in enumerate(lines):
        text(cx, cy - (n - 1) * 12 + i * 24 + 7, t, sz, col if i == 0 else "#333", wt)
def wire(x1, y1, x2, y2, col, d1, d2, dash=False):
    # đường cong: rời cổng theo hướng d1, vào thiết bị theo hướng d2
    k = 0.45
    c1 = (x1 + d1[0] * abs(y2 - y1 + x2 - x1) * k + d1[0] * 60, y1 + d1[1] * (abs(y2 - y1) * k + 60))
    c2 = (x2 + d2[0] * (abs(x2 - x1) * k + 60), y2 + d2[1] * (abs(y2 - y1) * k + 60))
    da = ' stroke-dasharray="10 8"' if dash else ""
    o.append(f'<path d="M{x1:.1f},{y1:.1f} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round"{da}/>')
    o.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="6" fill="{col}"/>')

# ---------------- hộp gateway
o.append(f'<rect x="{X0-14}" y="{Y0-14}" width="{400+28}" height="{400+28}" rx="14" fill="#dfe6ee" stroke="#5b6b7c" stroke-width="4"/>')
o.append(f'<rect x="{X0}" y="{Y0}" width="400" height="400" fill="#1d6b3a" stroke="#123" stroke-width="2"/>')
o.append(f'<rect x="{bx(18.5)}" y="{by(92.5)}" width="{28*S}" height="{55*S}" fill="#202020"/>')
o.append(f'<rect x="{bx(49)}" y="{by(100.5)}" width="{28*S}" height="{55*S}" fill="#1f3fa0"/>')
o.append(f'<rect x="{bx(55)}" y="{by(100.5)}" width="{16*S}" height="{21*S}" fill="#b8b8b8"/>')
text(bx(33), by(60), "ESP32", 18, "white", "bold"); text(bx(63), by(66), "W5500", 18, "white", "bold")
text(X0 + 200, Y0 + 300, "LÕI GATEWAY KD-GW", 22, "white", "bold")
RX, RY = X0 + 400 + 28, Y0 - 50
o.append(f'<rect x="{RX-14}" y="{RY-14}" width="{300+28}" height="{500+28}" rx="14" fill="#f3e3d2" stroke="#9b6a3c" stroke-width="4"/>')
o.append(f'<rect x="{RX}" y="{Y0}" width="300" height="400" fill="#1d4f8a" stroke="#123" stroke-width="2"/>')
for i in range(4):
    for yy in (Y0 + 46, Y0 + 270):
        o.append(f'<rect x="{RX + (9 + 16.25*i)*S + 4}" y="{yy}" width="{15.9*S - 8}" height="{80}" fill="#2a6fbf" stroke="#0c2f5c"/>')
text(RX + 150, Y0 + 210, "MODULE RELAY 8 KÊNH", 20, "white", "bold")
o.append(f'<path d="M{X0+400},{Y0+120} L{RX},{Y0+120}" stroke="#999" stroke-width="10"/>')
text(X0 + 200, Y0 - 40, "MÉP SAU", 22, "#5b6b7c", "bold"); text(X0 + 200, Y0 + 460, "MÉP TRƯỚC", 22, "#5b6b7c", "bold")


lab = {}
for l in PORTS["labels"]:
    lab.setdefault(l["text"], []).append(l)
def port_xy(name):
    extra = {"USB": {"side": "B", "at": 33.03}, "LAN": {"side": "B", "at": 63.0}}
    l = extra[name] if name in extra else lab[name][0]
    if l["side"] == "F": return bx(l["at"]), Y0 + 400 + 14
    if l["side"] == "B": return bx(l["at"]), Y0 - 14
    return X0 - 14, by(l["at"])

def dev(port, short=None):
    p = info[port]
    z = p["zone"]
    return z, [(f"{port} · {p['label']}", 18, "bold"), *[(t, 15, "normal") for t in wrap(p["device"], 22)]]
def wrap(t, n):
    words, out, cur = t.split(), [], ""
    for w_ in words:
        if len(cur) + len(w_) + 1 > n and cur:
            out.append(cur); cur = w_
        else:
            cur = (cur + " " + w_).strip()
    out.append(cur)
    return out[:3]

# ---------------- mép trước: AI1-6, OW, LOAD
front = ["AI1", "AI2", "AI3", "AI4", "AI5", "AI6", "OW", "LOAD"]
for i, pt in enumerate(front):
    x1, y1 = port_xy(pt)
    cx, cy = 660 + i * 195, 1690
    z, lines = dev(pt)
    wire(x1, y1, cx, cy - 62, COL[z], (0, 1), (0, -1), dash=(z == ""))
    box(cx, cy, 185, 124, COL[z], lines)

# ---------------- mép trái: nguồn, DI-F, RS485, DI1-8
lx_ = 470
items = [("3V3 5V G", "", [("3V3·5V·G", 18, "bold"), ("Nguồn 5V cho MQ-135", 15, "normal"), ("và YF-S201", 15, "normal")]),
         ("DI-F", None, None), ("RS485", None, None)]
ys = [470, 610, 750]
for (pt, z, lines), yy in zip(items, ys):
    x1, y1 = port_xy(pt)
    if lines is None:
        key = "DI-F" if pt == "DI-F" else "RS485"
        z, lines = dev(key)
    wire(x1, y1, lx_ + 115, yy, COL[z], (-1, 0), (1, 0), dash=(z == ""))
    box(lx_, yy, 230, 118, COL[z], lines)
# bảng nút DI1-4
yb = 920
for k in range(1, 5):
    x1, y1 = port_xy(f"DI{k}")
    wire(x1, y1, lx_ + 115, yb - 45 + (k - 1) * 30, COL["DK"], (-1, 0), (1, 0))
box(lx_, yb, 230, 150, COL["DK"], [("DI1–4 · NÚT BẤM", 18, "bold"), ("Trồng trọt · Chăn nuôi", 15, "normal"),
                                   ("Thủy sản · Tắt/Bật tổng", 15, "normal"), ("(bảng trạm điều khiển)", 15, "normal")])
for k, yy in zip(range(5, 9), (1090, 1210, 1330, 1450)):
    x1, y1 = port_xy(f"DI{k}")
    z, lines = dev(f"DI{k}")
    lines[0] = (f"DI{k} · PHAO", 18, "bold")
    wire(x1, y1, lx_ + 115, yy, COL[z], (-1, 0), (1, 0))
    box(lx_, yy, 230, 100, COL[z], lines)
text(160, 1190, "G = GND chung", 16, "#666")

# ---------------- mép sau
back = [("PWR2", 680), ("PWR1", 920), ("SERVO", 1160)]
for pt, cx in back:
    x1, y1 = port_xy(pt)
    z, lines = dev(pt)
    wire(x1, y1, cx, 410 + 60, COL[z], (0, -1), (0, 1))
    box(cx, 410, 225, 120, COL[z], lines)
# hub I2C + 4 cảm biến
x1, y1 = port_xy("I2C")
wire(x1, y1, 1400, 465, "#555", (0, -1), (0, 1))
box(1400, 420, 170, 90, "#555", [("I2C-EXT", 18, "bold"), ("Hub I2C 4 cổng", 15, "normal")])
subs = [("SHT31 nhà kính", "nhiệt/ẩm KK · 0x44", "TT", 1050), ("BH1750", "ánh sáng · 0x23", "TT", 1280),
        ("SHT31 chuồng gà", "nhiệt/ẩm · 0x45", "CN", 1510), ("INA226 năng lượng", "V/A ắc quy · 0x40", "NL", 1740)]
for t1, t2, z, cx in subs:
    wire(1400, 375, cx, 200 + 45, COL[z], (0, -1), (0, 1))
    box(cx, 200, 205, 90, COL[z], [(t1, 17, "bold"), (t2, 15, "normal")])
x1, y1 = port_xy("USB")
wire(x1, y1, 1200, 620, "#9a9a9a", (0, -1), (0, 1), dash=True)
text(1200, 640, "USB: chỉ dùng khi nạp code", 14, "#777")
# LAN
x1, y1 = port_xy("LAN")
wire(x1, y1, 1900, 485, COL["NET"], (0, -1), (0, 1))
box(1900, 420, 230, 130, COL["NET"], [("LAN → Switch", 18, "bold"), ("Pi 5 + màn hình 7\"", 15, "normal"),
                                      ("trạm điều khiển → VPS", 15, "normal"), ("Camera đếm gà → Pi 5", 15, "normal")])
# 12V
x1, y1 = port_xy("12V")
wire(x1, y1, 2200, 485, COL["NL"], (0, -1), (0, 1))
box(2200, 420, 270, 130, COL["NL"], [("12V ← NĂNG LƯỢNG", 17, "bold"), ("Pin mặt trời 30W → sạc 10A", 15, "normal"),
                                     ("→ ắc quy 12V 7Ah → cầu chì", 15, "normal"), ("→ jack gateway + tải 12V", 15, "normal")])

# ---------------- relay
rx_dev = 2580
for k in range(1, 9):
    i = (k - 1) % 4
    tx = RX + (9 + 16.25 * i + 8.1) * S
    if k <= 4:
        ty, yy, d1 = Y0 + 400 + 64, 1260 + (k - 1) * 125, (0, 1)
    else:
        ty, yy, d1 = Y0 - 64, 580 + (8 - k) * 110, (0, -1)
    z, lines = dev(f"RLY{k}")
    wire(tx, ty, rx_dev - 130, yy, COL[z], d1, (-1, 0))
    box(rx_dev, yy, 260, 100 if k > 4 else 110, COL[z], lines)
text(rx_dev, 1800, "Tải 12V: dây (+) vào COM, NO ra tải,", 16, "#555")
text(rx_dev, 1824, "(−) tải về GND nguồn 12V", 16, "#555")

# ---------------- tiêu đề + chú giải
text(40, 60, "NÔNG NGHIỆP THÔNG MINH – Sơ đồ đấu nối vào hộp gateway KD-GW", 34, "#123", "bold", "start")
text(40, 100, "Nhìn từ trên xuống · mép sau ở trên · mỗi dây nối từ đúng cổng trên vách hộp tới cảm biến/thiết bị", 20, "#444", "normal", "start")
lx0 = 40
for i, (k, t) in enumerate([("TT", "Trồng trọt"), ("CN", "Chăn nuôi"), ("TS", "Thủy sản"), ("NL", "Năng lượng"),
                             ("DK", "Trạm điều khiển"), ("", "Dự phòng (nét đứt)")]):
    x = lx0 + i * 230
    o.append(f'<line x1="{x}" y1="140" x2="{x+50}" y2="140" stroke="{COL[k]}" stroke-width="8" stroke-linecap="round"/>')
    text(x + 62, 147, t, 20, "#333", "normal", "start")

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="white"/>' + "".join(o) + "</svg>"
open(R + "/docs/nntm_wiring.svg", "w").write(svg)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(), write_to=R + "/docs/nntm_wiring.png", output_width=W)
print("ok")
