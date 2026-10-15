# -*- coding: utf-8 -*-
"""
生成臺東協會與文健站外勤巡訪地圖專屬圖示 (Favicons & App Icons)
設計意象：臺東山海綠意 (翡翠綠/海洋藍) + 辦公事務與部落文健站標誌
"""

import os
from PIL import Image, ImageDraw

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_icon(size):
    # 背景圓角漸層翡翠綠/深藍 (象徵臺東自然山海與專業科技)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = size * 0.04
    rect = [margin, margin, size - margin, size - margin]
    radius = size * 0.22

    # 主底色：深青碧海綠 (#064E3B -> #0F766E)
    draw.rounded_rectangle(rect, radius=radius, fill=(15, 118, 110, 255), outline=(52, 211, 153, 255), width=max(1, int(size * 0.03)))

    # 繪製圖騰：簡約房屋(文健站據點) + 事務影印機/文件幾何
    center_x = size / 2
    center_y = size / 2

    # 屋頂 (文健站/協會)
    roof_top = (center_x, size * 0.22)
    roof_left = (size * 0.25, size * 0.44)
    roof_right = (size * 0.75, size * 0.44)
    draw.polygon([roof_top, roof_left, roof_right], fill=(52, 211, 153, 255))

    # 屋身/事務設備主體
    body_rect = [size * 0.30, size * 0.44, size * 0.70, size * 0.78]
    draw.rounded_rectangle(body_rect, radius=max(2, int(size * 0.05)), fill=(255, 255, 255, 255))

    # 出紙口/文檔線條 (象徵 OA 事務機出紙與文件傳遞)
    slot_y1 = size * 0.54
    slot_y2 = size * 0.60
    draw.rounded_rectangle([size * 0.38, slot_y1, size * 0.62, slot_y2], radius=max(1, int(size * 0.02)), fill=(15, 118, 110, 255))

    line_y = size * 0.68
    draw.line([size * 0.38, line_y, size * 0.62, line_y], fill=(52, 211, 153, 255), width=max(1, int(size * 0.03)))

    return img

sizes = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "apple-touch-icon.png": 180,
    "icon-192.png": 192,
    "icon-512.png": 512
}

for filename, sz in sizes.items():
    out_path = os.path.join(PROJECT_DIR, filename)
    icon = create_icon(sz)
    icon.save(out_path, format="PNG")
    print(f"Created {filename} ({sz}x{sz})")

# 製作 favicon.ico
icon_16 = create_icon(16)
icon_32 = create_icon(32)
icon_48 = create_icon(48)
ico_path = os.path.join(PROJECT_DIR, "favicon.ico")
icon_32.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
print("Created favicon.ico")

# 製作 favicon.svg
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="92" height="92" x="4" y="4" rx="20" fill="#0F766E" stroke="#34D399" stroke-width="3"/>
  <polygon points="50,20 22,44 78,44" fill="#34D399"/>
  <rect x="28" y="44" width="44" height="34" rx="4" fill="#FFFFFF"/>
  <rect x="36" y="52" width="28" height="6" rx="2" fill="#0F766E"/>
  <line x1="36" y1="68" x2="64" y2="68" stroke="#34D399" stroke-width="3" stroke-linecap="round"/>
</svg>'''

with open(os.path.join(PROJECT_DIR, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(svg_content)
print("Created favicon.svg")
