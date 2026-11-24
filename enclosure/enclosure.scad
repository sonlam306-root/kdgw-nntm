// ============================================================
//  Vỏ hộp gateway dạng module (r2 – chữ IN NỔI, nắp in ngửa không cần support)
//  part = "core_base" | "core_lid" | "relay_base" | "relay_lid" | "assembly"
// ============================================================
include <layout.scad>

part = "assembly";

// Chữ trên nắp, tên relay: lấy từ layout.scad (sinh theo profile dự án)
//   lid_texts       = [[chữ, cỡ, lệch_y], ...]   nắp lõi
//   relay_lid_texts = [[chữ, cỡ, lệch_y], ...]   nắp module relay (giữa nắp)
//   relay_labels    = [[module, kênh 0..7, số, [dòng1, dòng2?], cỡ], ...]
relay_mod = 0;      // nắp relay của module A (0) hay B (1)
explode = 8;        // khoảng nhấc nắp khi xem lắp ráp (assembly)
text_col = "#ffd54a";   // màu chữ nổi khi xem trước (không ảnh hưởng STL)
core_col = "#5d8aa8"; lid_col = "#9fc5e8"; relay_col = "#e69138"; rlid_col = "#fce5cd";

$fn  = 48;
font = "DejaVu Sans:style=Bold";

// ---------- thông số chung ----------
wall    = 2.4;
floor_t = 2.4;
lid_t   = 4.0;      // nắp phẳng mặt dưới, có rãnh nhận gờ của hộp
clr     = 0.5;      // khe hở PCB - vách
standoff_h = 6;     // trụ dưới PCB
above   = 30;       // khoảng trống trên mặt PCB
relief  = 0.6;      // chữ nổi cao 0.6 mm (5 lớp 0.12 mm)
tongue_w = 1.0;     // gờ trên miệng hộp (nửa trong của vách)
tongue_h = 2.0;
gclr    = 0.2;      // khe hở gờ - rãnh nắp

inner_h  = standoff_h + pcb_t + above;   // 37.6
base_h   = floor_t + inner_h;            // 40
pcb_z    = floor_t + standoff_h;         // đáy PCB
pcb_top  = pcb_z + pcb_t;

// ---------- lõi ----------
core_in  = [pcb_size.x + 2*clr, pcb_size.y + 2*clr];
core_out = [core_in.x + 2*wall, core_in.y + 2*wall];
pcb_off  = [wall + clr, wall + clr];

// ---------- module relay ----------
rpcb     = rpcb_size;
wire_gap = 10;               // khoảng luồn dây trước/sau domino 220 V
dt_depth = 3;                // ray đuôi én nhô ra 3 mm
rwall_l  = wall + dt_depth;  // vách trái dày hơn để chứa rãnh
relay_in  = [rpcb.x + 2*clr, rpcb.y + 2*clr + 2*wire_gap];
relay_out = [rwall_l + relay_in.x + wall, relay_in.y + 2*wall];
rpcb_off  = [rwall_l + clr, wall + clr + wire_gap];
rdy       = (relay_out.y - core_out.y) / 2;   // module relay lệch tâm so với lõi

rail_y = [8, 96];            // vị trí ray (toạ độ hộp lõi), tránh cửa sổ dây bẹ

// ============================================================
//  tiện ích
// ============================================================
module rbox(s, r=3) {
  linear_extrude(s.z)
    offset(r) offset(-r) square([s.x, s.y]);
}

// Biên dạng đuôi én (mặt phẳng XY): gốc rộng 6 tại x=0, ngọn rộng 9 tại x=3
module dovetail_2d(c=0) {
  polygon([[-0.01, -3 - c], [dt_depth + c, -4.5 - c],
           [dt_depth + c, 4.5 + c], [-0.01, 3 + c]]);
}
module rail_male(h)  { linear_extrude(h) dovetail_2d(0); }
module rail_slot(h)  { translate([0, 0, -1]) linear_extrude(h + 2) dovetail_2d(0.25); }

// Chữ NỔI trên mặt ngoài vách. edge: F/L/B/R; pos theo trục cạnh, z tuyệt đối
module wall_text(edge, pos, z, size, txt, out) {
  e = 0.01;
  t = [
    edge == "F" ? [pos, e, z] :
    edge == "B" ? [pos, out.y - e, z] :
    edge == "L" ? [e, pos, z] :
                  [out.x - e, pos, z]
  ][0];
  rz = edge == "F" ? 0 : edge == "B" ? 180 : edge == "L" ? -90 : 90;
  color(text_col) translate(t) rotate([90, 0, rz])
    linear_extrude(relief + e)
      text(txt, size = size, font = font, halign = "center", valign = "baseline");
}

// Gờ trên miệng hộp: dải rộng tongue_w ôm sát mép trong vách
module tongue(o, s) {
  translate([0, 0, base_h]) linear_extrude(tongue_h)
    translate(o) difference() {
      offset(delta = tongue_w) square(s);
      square(s);
    }
}
// Rãnh dưới nắp nhận gờ (nắp in ngửa: trần rãnh chỉ bắc cầu 1.4 mm)
module groove(o, s) {
  translate([0, 0, -1]) linear_extrude(tongue_h + 0.3 + 1)
    translate(o) difference() {
      offset(delta = tongue_w + gclr) square(s);
      offset(delta = -gclr) square(s);
    }
}
// Chữ nổi trên mặt nắp
module lid_text(cx, cy, rows) {
  color(text_col) for (r = rows) translate([cx, cy + r[2], lid_t - 0.01])
    linear_extrude(relief + 0.01) text(r[0], size = r[1], font = font, halign = "center", valign = "center");
}

// Cắt cửa sổ trên vách lõi theo bảng windows
module core_window(w) {
  e = w[0]; s = w[1]; l = w[2]; z0 = w[3]; h = w[4];
  if (e == "F") translate([pcb_off.x + s, -1, pcb_top + z0]) cube([l, wall + 2, h]);
  if (e == "B") translate([pcb_off.x + s, core_out.y - wall - 1, pcb_top + z0]) cube([l, wall + 2, h]);
  if (e == "L") translate([-1, pcb_off.y + s, pcb_top + z0]) cube([wall + 2, l, h]);
  if (e == "R") translate([core_out.x - wall - 1, pcb_off.y + s, pcb_top + z0]) cube([wall + 2, l, h]);
}

// Trụ dưới PCB có lỗ cho đai ốc ren cấy M3 (heat-set, Ø4.2)
module standoff_boss(p) {
  translate([p.x, p.y, 0]) difference() {
    cylinder(d = 8, h = floor_t + standoff_h);
    translate([0, 0, floor_t + standoff_h - 5]) cylinder(d = 4.2, h = 6);
  }
}

// ============================================================
//  ĐÁY LÕI
// ============================================================
module core_base() {
  difference() {
    union() {
      color(core_col) difference() {
        rbox([core_out.x, core_out.y, base_h]);
        translate([wall, wall, floor_t]) cube([core_in.x, core_in.y, base_h]);
      }
      color(core_col) for (h = pcb_holes) standoff_boss([pcb_off.x + h.x, pcb_off.y + h.y]);
      // ray đực bên phải để gắn module relay
      color(core_col) for (y = rail_y) translate([core_out.x, y, 0]) rail_male(base_h);
      color(core_col) tongue([wall, wall], core_in);
      for (lb = labels) {
        pos = (lb[0] == "F" || lb[0] == "B") ? pcb_off.x + lb[1] : pcb_off.y + lb[1];
        wall_text(lb[0], pos, pcb_top + lb[2], lb[3], lb[4], core_out);
      }
    }
    for (w = windows) core_window(w);
    // lỗ giá cầu chì trên vách sau
    translate([pcb_off.x + fuse_hole[0], core_out.y + 1, pcb_top + fuse_hole[1]])
      rotate([90, 0, 0]) cylinder(d = fuse_hole[2], h = wall + 2);
    // khe thoáng đáy
    for (i = [0:5]) translate([30 + i*9, 38, -1]) cube([4, 30, floor_t + 2]);
  }
}

// ============================================================
//  NẮP LÕI (bắt 4 vít M3 vào trụ đồng 30 mm)
// ============================================================
module core_lid() {
  color(lid_col) difference() {
    rbox([core_out.x, core_out.y, lid_t]);
    groove([wall, wall], core_in);
    // lỗ vít bắt chìm (côn mở lên trên – in ngửa được)
    for (h = pcb_holes) translate([pcb_off.x + h.x, pcb_off.y + h.y, -1]) {
      cylinder(d = 3.4, h = lid_t + 2);
      translate([0, 0, lid_t + 1 - 1.8]) cylinder(d1 = 3.4, d2 = 7.0, h = 1.81);
    }
  }
  lid_text(core_out.x/2, core_out.y/2, lid_texts);
}

// ============================================================
//  ĐÁY MODULE RELAY (8 kênh) – ghép nối tiếp được
// ============================================================
gland_x = [rpcb_off.x + 20, rpcb_off.x + 55];   // lỗ siết cáp PG7 trên vách trước/sau
gland_z = pcb_top + 14;

module relay_base() {
  difference() {
    union() {
      color(relay_col) difference() {
        rbox([relay_out.x, relay_out.y, base_h]);
        translate([rwall_l, wall, floor_t]) cube([relay_in.x, relay_in.y, base_h]);
      }
      color(relay_col) for (h = rholes) standoff_boss([rpcb_off.x + h.x, rpcb_off.y + h.y]);
      // ray đực bên phải (cho module B)
      color(relay_col) for (y = rail_y) translate([relay_out.x, y + rdy, 0]) rail_male(base_h);
      color(relay_col) tongue([rwall_l, wall], relay_in);
      wall_text("F", relay_out.x/2 - 0.5, gland_z + 9, 2.6, "220V", relay_out);
      wall_text("B", relay_out.x/2 - 0.5, gland_z + 9, 2.6, "220V", relay_out);
    }
    // rãnh đuôi én bên trái (trượt từ trên xuống vào ray của lõi)
    for (y = rail_y) translate([0, y + rdy, 0]) rail_slot(base_h);
    // cửa sổ dây bẹ (khớp với cửa sổ "R" của lõi)
    translate([-1, rdy + pcb_off.y + ribbon_win[0], pcb_top + ribbon_win[2]]) cube([rwall_l + 2, ribbon_win[1], ribbon_win[3]]);
    // cửa sổ phía phải để dây bẹ đi tiếp sang module B
    translate([relay_out.x - wall - 1, rdy + pcb_off.y + ribbon_win[0], pcb_top + ribbon_win[2]]) cube([wall + 2, ribbon_win[1], ribbon_win[3]]);
    // lỗ siết cáp 220 V trước và sau
    for (x = gland_x) {
      translate([x, -1, gland_z]) rotate([-90, 0, 0]) cylinder(d = 12.5, h = wall + 2);
      translate([x, relay_out.y - wall - 1, gland_z]) rotate([-90, 0, 0]) cylinder(d = 12.5, h = wall + 2);
    }
    // khấc khoá nắp cài: lõm 0.5 mm ở mặt ngoài gờ (vách trước/sau)
    for (y = [wall - tongue_w - 1, relay_out.y - wall + tongue_w - 0.5])
      for (x = [rwall_l + 15, rwall_l + relay_in.x - 15])
        translate([x - 4, y, base_h + 0.5]) cube([8, 1.5, 1.0]);
    // khe thoáng đáy
    for (i = [0:4]) translate([rwall_l + 10 + i*12, 30, -1]) cube([4, 40, floor_t + 2]);
  }
}

// ============================================================
//  NẮP MODULE RELAY (cài, không cần vít)
// ============================================================
module relay_lid(mod = 0) {
  color(rlid_col) difference() {
    rbox([relay_out.x, relay_out.y, lid_t]);
    groove([rwall_l, wall], relay_in);
  }
  // mấu cài: nêm 0.4 mm trên thành ngoài rãnh, vát dưới để ấn vào dễ
  for (y = [0, 1]) for (x = [rwall_l + 15, rwall_l + relay_in.x - 15]) {
    yy = y == 0 ? wall - tongue_w - gclr : relay_out.y - wall + tongue_w + gclr;
    s  = y == 0 ? 1 : -1;
    color(rlid_col) translate([x - 3, yy, 0.5]) rotate([90, 0, 90]) linear_extrude(6)
      polygon([[0, 0], [0, 1.0], [0.4 * s, 1.0]]);
  }
  lid_text(relay_out.x/2, relay_out.y/2, relay_lid_texts);
  // tên từng kênh relay, đặt ngay trên cụm domino của kênh đó
  for (l = relay_labels) if (l[0] == mod) {
    ch = l[1];
    x = rpcb_off.x + relay_com_x[ch % 4];
    y = ch < 4 ? rpcb_off.y + 7 : rpcb_off.y + rpcb.y - 7;
    color(text_col) translate([x, y, lid_t - 0.01]) linear_extrude(relief + 0.01) {
      n = len(l[3]); s = l[4];
      H = 3.2 + 1.0 + n * s * 1.65;
      translate([0, H/2 - 1.6]) text(l[2], size = 3.2, font = font, halign = "center", valign = "center");
      for (i = [0 : n - 1])
        translate([0, H/2 - 4.2 - s * 0.825 - i * s * 1.65]) text(l[3][i], size = s, font = font, halign = "center", valign = "center");
    }
  }
}

// ============================================================
module assembly() {
  core_base();
  translate([0, 0, base_h + explode]) core_lid();
  for (i = [0 : n_relay_mod - 1]) {
    x0 = core_out.x + i * relay_out.x;
    translate([x0, -rdy, 0]) relay_base();
    translate([x0, -rdy, base_h + explode]) relay_lid(i);
  }
}

if (part == "core_base")  core_base();
if (part == "core_lid")   core_lid();          // in ngửa, chữ nổi hướng lên
if (part == "relay_base") relay_base();
if (part == "relay_lid")  relay_lid(relay_mod);
if (part == "assembly")   assembly();
