# -*- coding: utf-8 -*-
"""
發送每月 1 號資料更新通報郵件
"""

import os
import sys
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PROJECT_DIR, 'data', 'taitung_database.json')

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
TO_EMAIL = os.getenv("REPORT_TO_EMAIL", "wujeff520@gmail.com")

if not SMTP_USER or not SMTP_PASSWORD:
    print("[SKIP] 未設定 SMTP_USER 或 SMTP_PASSWORD，略過郵件發送。")
    sys.exit(0)

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    db = json.load(f)

today_str = datetime.now().strftime("%Y年%m月01日")
subject = f"【自動通報】臺東協會與文健站外勤巡訪地圖 - {today_str} 資料更新報告"

html_body = f"""
<html>
<body style="font-family:'Noto Sans TC',sans-serif; color:#0F172A; line-height:1.6;">
  <div style="background:#0F172A; color:white; padding:18px 24px; border-radius:8px 8px 0 0;">
    <h2 style="margin:0;">🏢 臺東協會與文健站·事務設備巡訪地圖</h2>
    <p style="margin:4px 0 0 0; color:#94A3B8; font-size:14px;">每月 1 號定時自動巡檢與資料同步報告</p>
  </div>
  <div style="padding:20px; border:1px solid #E2E8F0; border-top:none; background:#F8FAFC;">
    <p>您好：</p>
    <p>系統已於 <strong>{today_str}</strong> 完成臺東縣立案協會與原住民文化健康站 (文健站) 最新名冊的審計與同步，成果如下：</p>
    
    <table style="width:100%; border-collapse:collapse; margin:16px 0; background:white;">
      <tr style="background:#F1F5F9;">
        <th style="padding:10px; border:1px solid #CBD5E1; text-align:left;">項目</th>
        <th style="padding:10px; border:1px solid #CBD5E1; text-align:right;">數量</th>
      </tr>
      <tr>
        <td style="padding:10px; border:1px solid #CBD5E1;">🏡 原住民文化健康站 (文健站)</td>
        <td style="padding:10px; border:1px solid #CBD5E1; text-align:right; font-weight:bold; color:#059669;">{db['wjs_units']} 站</td>
      </tr>
      <tr>
        <td style="padding:10px; border:1px solid #CBD5E1;">🏛️ 社會團體與立案協會</td>
        <td style="padding:10px; border:1px solid #CBD5E1; text-align:right; font-weight:bold; color:#4F46E5;">{db['ass_units']} 所</td>
      </tr>
      <tr style="background:#F8FAFC; font-weight:bold;">
        <td style="padding:10px; border:1px solid #CBD5E1;">合計全縣拜訪點</td>
        <td style="padding:10px; border:1px solid #CBD5E1; text-align:right; color:#0F172A;">{db['total_units']} 家</td>
      </tr>
    </table>

    <p>🌐 <strong>線上即時地圖</strong>：<a href="https://gyuyu2002-jeff.github.io/taitung-field-map/">https://gyuyu2002-jeff.github.io/taitung-field-map/</a></p>
    <p style="font-size:12px; color:#64748B;">本郵件由 GitHub Actions 每月定時排程自動發送。</p>
  </div>
</body>
</html>
"""

msg = MIMEMultipart()
msg['From'] = f"臺東外勤巡訪系統 <{SMTP_USER}>"
msg['To'] = TO_EMAIL
msg['Subject'] = subject
msg.attach(MIMEText(html_body, 'html', 'utf-8'))

try:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())
    print(f"[OK] 已成功發送通報郵件至 {TO_EMAIL}")
except Exception as e:
    print(f"[WARN] 郵件發送失敗: {e}")
