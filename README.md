# NNTM — Nông nghiệp thông minh vì tương lai xanh

- Phần cứng: **KD-GW-HW-v1.2** (1 mạch chính + 1 module relay 8 kênh)
- Profile: `profile.json` — **đã duyệt** (23/11/2026)
- Khu: Trồng trọt · Chăn nuôi · Thủy sản · Trạm năng lượng · Trạm điều khiển
- Vỏ hộp: `enclosure/stl/` (nắp khắc "Trường THCS Kim Đồng / Nông nghiệp thông minh")
- Tài liệu: `docs/` — bảng cổng + sơ đồ đấu nối + mô phỏng 3D
- Firmware: `firmware/` — giai đoạn tiếp theo (firmware lõi + profile NNTM)
- Dashboard: `dashboard/` — giai đoạn tiếp theo (3D Digital Twin theo kiến trúc KimDong IOC, chạy Pi 5 + VPS)

## Lấy mã nguồn

Repo này dùng phần cứng chung qua submodule `kdgw-hardware/` (ghim đúng bản KD-GW-HW-v1.2, vỏ hộp r2):

```bash
git clone --recurse-submodules <url>/kdgw-nntm.git
cd kdgw-nntm
```

## Sinh lại vỏ hộp và tài liệu sau khi sửa `profile.json`

```bash
python3 kdgw-hardware/platform/make_project.py .          # kiểm tra nhãn + xuất STL vào enclosure/stl/
python3 kdgw-hardware/platform/make_project.py . --no-stl # chỉ kiểm tra nhãn (nhanh)
python3 kdgw-hardware/platform/make_ports_pdf.py .        # PDF bảng cổng
python3 kdgw-hardware/platform/draw_walls.py .            # ảnh nhãn các vách
python3 kdgw-hardware/platform/draw_lids.py .             # ảnh nắp chữ nổi
python3 kdgw-hardware/platform/render_preview.py enclosure/enclosure.scad enclosure/xem_truoc "Tên dự án"
```

Cần: Python 3, OpenSCAD, Pillow, reportlab, cairosvg (xvfb-run để chụp ảnh 3D trên máy không có màn hình).

Cập nhật lên bản phần cứng mới (khi có): `cd kdgw-hardware && git fetch --tags && git checkout <tag mới>`, rồi đổi `hardware` trong `profile.json` và sinh lại.
