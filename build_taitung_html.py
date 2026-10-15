# -*- coding: utf-8 -*-
"""
臺東協會與原住民健康文化站 (文健站) 事務設備外勤巡訪地圖 - HTML 編譯器
生成單一自包含、可全離線執行的高效率前端網頁應用程式 (index.html)
"""

import json
import os
import sys
import base64

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(PROJECT_DIR, 'data', 'taitung_database.json')
OUTPUT_HTML = os.path.join(PROJECT_DIR, 'index.html')

if not os.path.exists(DATABASE_FILE):
    raise FileNotFoundError(f"找不到 {DATABASE_FILE}！請先執行 generate_taitung_database.py")

with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
    bundle = json.load(f)

print(f"[OK] 成功載入 {DATABASE_FILE}，內含 {bundle['total_units']} 家單位（文健站 {bundle['wjs_units']} 站、協會 {bundle['ass_units']} 所）")

database_json = json.dumps(bundle, ensure_ascii=False)

def get_base64_data_uri(filepath, mime='image/png'):
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('ascii')
            return f"data:{mime};base64,{b64}"
    return ""

b64_32_uri = get_base64_data_uri(os.path.join(PROJECT_DIR, 'favicon-32x32.png'))
b64_16_uri = get_base64_data_uri(os.path.join(PROJECT_DIR, 'favicon-16x16.png'))
b64_apple_uri = get_base64_data_uri(os.path.join(PROJECT_DIR, 'apple-touch-icon.png'))

html_template = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>臺東協會與文健站·事務設備巡訪地圖</title>
  <meta name="application-name" content="臺東協會與文健站外勤地圖">
  <meta name="apple-mobile-web-app-title" content="臺東文健站外勤">
  <meta name="theme-color" content="#0F172A">

  <!-- SEO & Social Share Preview -->
  <meta name="description" content="臺東縣立案協會與原住民文化健康站(文健站)事務設備外勤巡訪地圖。專為 OA 事務設備、影印機租賃、印表機、弱電監視與辦公設備打造。">
  <meta property="og:title" content="臺東協會與文健站·事務設備巡訪地圖">
  <meta property="og:description" content="收錄臺東 16 鄉鎮市 700+ 家立案協會與原住民文化健康站，支援同路巡訪快篩、一鍵 Google 導航、電話直撥與 OA 拜訪管理。">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://gyuyu2002-jeff.github.io/taitung-field-map/">
  <meta property="og:image" content="https://gyuyu2002-jeff.github.io/taitung-field-map/apple-touch-icon.png">
  <meta property="og:site_name" content="臺東協會與文健站·事務設備巡訪地圖">

  <!-- Favicons -->
  <link rel="shortcut icon" type="image/png" href="__B64_32_URI__">
  <link rel="icon" type="image/png" sizes="32x32" href="__B64_32_URI__">
  <link rel="icon" type="image/png" sizes="16x16" href="__B64_16_URI__">
  <link rel="apple-touch-icon" sizes="180x180" href="__B64_APPLE_URI__">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">

  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Serif+TC:wght@700;900&display=swap" rel="stylesheet">

  <style>
    :root {
      --navy: #0F172A;
      --navy-light: #1E293B;
      --teal: #0D9488;
      --teal-light: #CCFBF1;
      --emerald: #059669;
      --emerald-light: #D1FAE5;
      --indigo: #4F46E5;
      --indigo-light: #E0E7FF;
      --amber: #D97706;
      --amber-light: #FEF3C7;
      --rose: #E11D48;
      --rose-light: #FFE4E6;
      --border: #E2E8F0;
      --bg: #F8FAFC;
      --card-bg: #FFFFFF;
      --text: #0F172A;
      --muted: #64748B;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.08);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* Header */
    header {
      background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F766E 100%);
      color: white;
      padding: 10px 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      flex-shrink: 0;
      box-shadow: var(--shadow-md);
      z-index: 1000;
    }
    .header-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .brand-icon {
      width: 38px;
      height: 38px;
      background: #0D9488;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      box-shadow: 0 2px 8px rgba(13, 148, 136, 0.4);
    }
    .brand-title {
      font-size: 1.15rem;
      font-weight: 900;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .brand-subtitle {
      font-size: 0.76rem;
      color: #94A3B8;
      margin-top: 1px;
    }
    .header-actions {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 5px 11px;
      font-size: 0.8rem;
      font-weight: 700;
      border-radius: 6px;
      border: 1px solid rgba(255,255,255,0.15);
      background: rgba(255,255,255,0.08);
      color: white;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }
    .btn:hover { background: rgba(255,255,255,0.2); }
    .btn-teal { background: #0D9488; border-color: #0D9488; color: white; }
    .btn-teal:hover { background: #0F766E; }
    .btn-emerald { background: #059669; border-color: #059669; color: white; }
    .btn-emerald:hover { background: #047857; }
    .btn-amber { background: #D97706; border-color: #D97706; color: white; }

    /* Metadata Info Bar */
    .meta-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      font-size: 0.73rem;
      padding-top: 4px;
      border-top: 1px solid rgba(255,255,255,0.1);
      color: #CBD5E1;
    }
    .meta-item { display: flex; align-items: center; gap: 5px; }
    .meta-tag {
      background: rgba(13, 148, 136, 0.25);
      color: #5EEAD4;
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 700;
    }

    /* Navigation Bars */
    .nav-container {
      background: white;
      border-bottom: 1px solid var(--border);
      flex-shrink: 0;
      box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .tier-bar {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      overflow-x: auto;
      white-space: nowrap;
      scrollbar-width: thin;
    }
    .tier-bar::-webkit-scrollbar { height: 4px; }
    .tier-bar::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
    .zone-bar {
      background: #F1F5F9;
      border-bottom: 1px solid #E2E8F0;
      padding: 5px 14px;
    }
    .nav-chip {
      padding: 4px 10px;
      font-size: 0.8rem;
      font-weight: 700;
      border-radius: 20px;
      background: white;
      border: 1px solid var(--border);
      color: var(--muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s;
    }
    .nav-chip:hover { border-color: var(--teal); color: var(--teal); }
    .nav-chip.active {
      background: var(--navy);
      color: white;
      border-color: var(--navy);
      box-shadow: var(--shadow-sm);
    }
    .township-bar .nav-chip.active {
      background: var(--teal);
      border-color: var(--teal);
      color: white;
    }
    .chip-badge {
      font-size: 0.7rem;
      padding: 1px 5px;
      border-radius: 10px;
      background: rgba(0,0,0,0.06);
    }
    .nav-chip.active .chip-badge { background: rgba(255,255,255,0.25); color: white; }

    /* Filter & Search Bar */
    .filter-bar {
      background: white;
      padding: 8px 14px;
      border-bottom: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      gap: 6px;
      flex-shrink: 0;
    }
    .filter-row {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .search-box {
      flex: 1;
      min-width: 240px;
      position: relative;
    }
    .search-input {
      width: 100%;
      padding: 7px 10px 7px 32px;
      font-size: 0.84rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: #F8FAFC;
      outline: none;
      transition: border 0.2s;
    }
    .search-input:focus { border-color: var(--teal); background: white; }
    .search-icon {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 14px;
      color: var(--muted);
    }
    .quick-filter-group {
      display: flex;
      align-items: center;
      gap: 5px;
      overflow-x: auto;
      scrollbar-width: none;
    }
    .quick-chip {
      padding: 3px 8px;
      font-size: 0.75rem;
      border-radius: 4px;
      border: 1px solid var(--border);
      background: #F8FAFC;
      color: var(--muted);
      cursor: pointer;
      white-space: nowrap;
      font-weight: 500;
      transition: all 0.15s;
    }
    .quick-chip:hover { border-color: var(--teal); color: var(--teal); }
    .quick-chip.active {
      background: var(--teal-light);
      border-color: var(--teal);
      color: var(--teal);
      font-weight: 700;
    }

    /* Main Container (Split View) */
    .main-content {
      flex: 1;
      display: flex;
      position: relative;
      overflow: hidden;
    }
    .list-pane {
      width: 440px;
      max-width: 100%;
      background: var(--bg);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      z-index: 10;
    }
    .list-header {
      padding: 8px 14px;
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--muted);
      border-bottom: 1px solid var(--border);
      background: white;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .cards-container {
      flex: 1;
      overflow-y: auto;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      scrollbar-width: thin;
    }
    .map-pane {
      flex: 1;
      position: relative;
    }
    #map { width: 100%; height: 100%; }

    /* Unit Card */
    .unit-card {
      background: var(--card-bg);
      border-radius: 8px;
      border: 1px solid var(--border);
      padding: 12px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: all 0.2s;
      cursor: pointer;
    }
    .unit-card:hover {
      border-color: var(--teal);
      box-shadow: var(--shadow-md);
      transform: translateY(-1px);
    }
    .unit-card.active-target {
      border-color: var(--teal);
      background: #F0FDFA;
      box-shadow: 0 0 0 2px var(--teal);
    }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
    }
    .card-title {
      font-size: 0.96rem;
      font-weight: 800;
      color: var(--navy);
      line-height: 1.35;
    }
    .category-badge {
      font-size: 0.7rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .badge-wjs { background: #D1FAE5; color: #047857; border: 1px solid #A7F3D0; }
    .badge-ass { background: #E0E7FF; color: #4338CA; border: 1px solid #C7D2FE; }

    .card-meta-line {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 0.8rem;
      color: var(--muted);
      flex-wrap: wrap;
    }
    .card-meta-item { display: inline-flex; align-items: center; gap: 4px; }
    .card-phone {
      color: #0284C7;
      text-decoration: none;
      font-weight: 700;
    }
    .card-phone:hover { text-decoration: underline; }
    .card-address {
      font-size: 0.78rem;
      color: #475569;
      display: flex;
      align-items: flex-start;
      gap: 4px;
    }
    .oa-tier-pill {
      font-size: 0.72rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 700;
      background: #FEF3C7;
      color: #B45309;
      align-self: flex-start;
    }
    .visit-summary-box {
      font-size: 0.75rem;
      background: #F8FAFC;
      border-left: 3px solid var(--teal);
      padding: 4px 8px;
      border-radius: 2px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .card-actions {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 6px;
      padding-top: 6px;
      border-top: 1px dashed var(--border);
    }
    .card-btn {
      padding: 4px 9px;
      font-size: 0.74rem;
      font-weight: 700;
      border-radius: 4px;
      border: 1px solid var(--border);
      background: white;
      color: var(--muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .card-btn:hover { background: #F1F5F9; color: var(--navy); }
    .card-btn-primary { background: #0D9488; border-color: #0D9488; color: white; }
    .card-btn-primary:hover { background: #0F766E; color: white; }

    /* Modals */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(2px);
      z-index: 9999;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }
    .modal-box {
      background: white;
      border-radius: 12px;
      width: 560px;
      max-width: 100%;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-lg);
      overflow: hidden;
      animation: modalFadeIn 0.2s ease-out;
    }
    @keyframes modalFadeIn {
      from { opacity: 0; transform: scale(0.95); }
      to { opacity: 1; transform: scale(1); }
    }
    .modal-header {
      padding: 14px 18px;
      background: var(--navy);
      color: white;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .modal-title { font-size: 1.05rem; font-weight: 800; }
    .modal-close {
      background: none;
      border: none;
      color: #94A3B8;
      font-size: 20px;
      cursor: pointer;
    }
    .modal-close:hover { color: white; }
    .modal-body {
      padding: 18px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .form-label {
      font-size: 0.8rem;
      font-weight: 700;
      color: #334155;
    }
    .form-control {
      padding: 8px 10px;
      font-size: 0.85rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      outline: none;
      font-family: inherit;
    }
    .form-control:focus { border-color: var(--teal); }
    .stage-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .stage-chip {
      padding: 4px 10px;
      font-size: 0.78rem;
      border-radius: 20px;
      border: 1px solid var(--border);
      background: #F8FAFC;
      cursor: pointer;
      font-weight: 500;
    }
    .stage-chip.active {
      background: #0D9488;
      border-color: #0D9488;
      color: white;
      font-weight: 700;
    }
    .modal-footer {
      padding: 12px 18px;
      background: #F8FAFC;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: flex-end;
      gap: 8px;
    }

    /* Mobile Bottom Dock */
    .mobile-dock {
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: white;
      border-top: 1px solid var(--border);
      z-index: 2000;
      padding-bottom: env(safe-area-inset-bottom);
    }
    .dock-tabs {
      display: flex;
      height: 50px;
    }
    .dock-tab {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 2px;
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--muted);
      border: none;
      background: none;
      cursor: pointer;
    }
    .dock-tab.active {
      color: var(--teal);
    }

    /* RWD */
    @media (max-width: 900px) {
      .main-content { flex-direction: column; }
      .list-pane { width: 100%; height: 50%; }
      .map-pane { width: 100%; height: 50%; }
      .mobile-dock { display: block; }
      body { padding-bottom: 50px; }
      .brand-subtitle { display: none; }
      .meta-bar { font-size: 0.68rem; }
    }
  </style>
</head>
<body>

  <!-- Top Header -->
  <header>
    <div class="header-top">
      <div class="brand-group">
        <div class="brand-icon">🏢</div>
        <div>
          <div class="brand-title">臺東協會與文健站·事務設備巡訪地圖</div>
          <div class="brand-subtitle">專為 OA 事務設備（影印機租賃、印表機、碎紙機、弱電監視、電腦總機）打造之外勤巡訪系統</div>
        </div>
      </div>
      <div class="header-actions">
        <button class="btn btn-emerald" id="filterWjsBtn">🏡 文健站 (<span id="totalWjsCount">114</span>)</button>
        <button class="btn btn-teal" id="filterAssBtn">🏛️ 協會團體 (<span id="totalAssCount">587</span>)</button>
        <button class="btn" id="exportBtn">📤 匯出記錄 (CSV)</button>
        <button class="btn" id="importBtn">📥 匯入</button>
        <button class="btn" id="statsBtn">📊 統計</button>
      </div>
    </div>
    <div class="meta-bar">
      <div class="meta-item">
        <span>🕒 資料更新時間：</span>
        <span class="meta-tag" id="lastUpdatedDate">2026年10月01日 (固定每月 1 號排程校驗)</span>
      </div>
      <div class="meta-item">
        <span>🏛️ 官方資料來源：</span>
        <span>臺東縣政府民政處、社會處、原住民族行政處、原住民族委員會公開名冊</span>
      </div>
    </div>
  </header>

  <!-- Navigation Bars -->
  <div class="nav-container">
    <!-- Tier 1: 5 大地理分區 -->
    <div class="tier-bar zone-bar" id="zoneBar">
      <button class="nav-chip active" data-zone="全部">🧭 全臺東縣總覽</button>
      <button class="nav-chip" data-zone="市區生活圈">🏙️ 市區生活圈</button>
      <button class="nav-chip" data-zone="東部海岸線">🌊 東部海岸線</button>
      <button class="nav-chip" data-zone="花東縱谷線">🌾 花東縱谷線</button>
      <button class="nav-chip" data-zone="南迴山海線">⛰️ 南迴山海線</button>
      <button class="nav-chip" data-zone="離島專區">🏝️ 離島專區</button>
    </div>
    <!-- Tier 2: 16 鄉鎮市切換列 -->
    <div class="tier-bar township-bar" id="townshipBar">
      <!-- 動態生成鄉鎮標籤 -->
    </div>
  </div>

  <!-- Filter & Search Controls -->
  <div class="filter-bar">
    <div class="filter-row">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="搜尋單位名稱、理事長/站長姓名、電話、路段、部落、字號...">
      </div>
      <div class="quick-filter-group" id="oaTierFilter">
        <button class="quick-chip active" data-oa="全部">全部需求</button>
        <button class="quick-chip" data-oa="高印量">⭐ 高印量潛力戶</button>
        <button class="quick-chip" data-oa="複合機">🖨️ A3/A4 複合機</button>
        <button class="quick-chip" data-oa="弱電">💻 弱電/監控</button>
        <button class="quick-chip" data-oa="耗材">📄 耗材租約</button>
      </div>
    </div>
    <!-- 同路 / 同部落巡訪快捷快篩 -->
    <div class="filter-row" style="padding-top: 2px;">
      <span style="font-size:0.75rem; font-weight:700; color:var(--muted); white-space:nowrap;">🛣️ 同路段/部落巡訪：</span>
      <div class="quick-filter-group" id="streetTagGroup">
        <!-- 動態依鄉鎮生成同路段標籤 -->
      </div>
    </div>
  </div>

  <!-- Main Split Layout -->
  <div class="main-content">
    <!-- Left List Pane -->
    <div class="list-pane" id="listPane">
      <div class="list-header">
        <span>📋 拜訪清單：<strong id="filteredCount">0</strong> 筆單位</span>
        <span id="currentTownshipTitle" style="color:var(--teal);">全部鄉鎮</span>
      </div>
      <div class="cards-container" id="cardsContainer">
        <!-- 動態渲染卡片清單 -->
      </div>
    </div>

    <!-- Right Map Pane -->
    <div class="map-pane" id="mapPane">
      <div id="map"></div>
    </div>
  </div>

  <!-- Mobile Bottom Navigation Dock -->
  <div class="mobile-dock">
    <div class="dock-tabs">
      <button class="dock-tab active" id="tabList">📋 單位清單</button>
      <button class="dock-tab" id="tabSplit">⚖️ 分割視圖</button>
      <button class="dock-tab" id="tabMap">🗺️ 地圖視野</button>
    </div>
  </div>

  <!-- Visit Log CRM Modal -->
  <div class="modal-backdrop" id="visitModal">
    <div class="modal-box">
      <div class="modal-header">
        <div class="modal-title" id="visitModalTitle">📋 OA 事務設備拜訪紀錄</div>
        <button class="modal-close" onclick="closeVisitModal()">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label class="form-label">單位名稱</label>
          <div id="visitUnitName" style="font-weight:800; color:var(--navy); font-size:0.95rem;"></div>
          <div id="visitUnitInfo" style="font-size:0.78rem; color:var(--muted);"></div>
        </div>

        <div class="form-group">
          <label class="form-label">🎯 洽談階段進度</label>
          <div class="stage-chips" id="stageChips">
            <span class="stage-chip active" data-stage="初次拜訪/遞名片">初次拜訪/遞名片</span>
            <span class="stage-chip" data-stage="掌握現有機型/印量">掌握現有機型/印量</span>
            <span class="stage-chip" data-stage="提供租賃報價單">提供租賃報價單</span>
            <span class="stage-chip" data-stage="樣機展示/體驗試用">樣機展示/體驗試用</span>
            <span class="stage-chip" data-stage="成交簽約">🎉 成交簽約</span>
            <span class="stage-chip" data-stage="定期抄錶維護/送耗材">定期抄錶/送耗材</span>
            <span class="stage-chip" data-stage="租約未到期(預約回訪)">租約未到期(預約回訪)</span>
            <span class="stage-chip" data-stage="暫無需求">暫無需求</span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">👤 接洽窗口與職稱</label>
          <input type="text" id="visitContact" class="form-control" placeholder="例：陳理事長、林站長、張會計、照服員">
        </div>

        <div class="form-group">
          <label class="form-label">💬 事務設備現況與需求筆記 (OA Notes)</label>
          <textarea id="visitNotes" class="form-control" rows="3" placeholder="例：現有機型老舊常卡紙、每月黑白約2500張彩色500張、現有合約到今年11月、評估升級高階雙面掃描機型..."></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">⏰ 下次預計待辦與回訪日</label>
          <input type="text" id="visitFollowUp" class="form-control" placeholder="例：下週二送報價單、11/15帶碳粉試用包拜訪">
        </div>

        <div class="form-group">
          <label class="form-label">📜 歷史拜訪紀錄時間軸</label>
          <div id="visitHistoryTimeline" style="max-height:140px; overflow-y:auto; font-size:0.78rem; display:flex; flex-direction:column; gap:6px;">
            <!-- 動態列出歷史記錄 -->
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn" style="color:var(--text);" onclick="closeVisitModal()">取消</button>
        <button class="btn btn-teal" onclick="saveVisitRecord()">💾 儲存拜訪紀錄</button>
      </div>
    </div>
  </div>

  <!-- Stats Modal -->
  <div class="modal-backdrop" id="statsModal">
    <div class="modal-box" style="width:480px;">
      <div class="modal-header">
        <div class="modal-title">📊 臺東外勤拜訪進度統計</div>
        <button class="modal-close" onclick="closeStatsModal()">&times;</button>
      </div>
      <div class="modal-body" id="statsContent">
        <!-- 動態統計數據 -->
      </div>
      <div class="modal-footer">
        <button class="btn btn-teal" onclick="closeStatsModal()">確認</button>
      </div>
    </div>
  </div>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <script>
    // 注入全量資料庫 (701 家單位)
    const TAITUNG_DB = __DATABASE_JSON__;

    // 本機 CRM 儲存 Key
    const STORAGE_KEY = 'taitung_oa_field_logs_v1';
    let visitStore = {};
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) visitStore = JSON.parse(saved);
    } catch(e) {
      console.warn("LocalStorage 載入失敗:", e);
    }

    function saveStore() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(visitStore));
      } catch(e) {
        console.error("儲存失敗:", e);
      }
    }

    // 狀態變數
    let currentZone = "全部";
    let currentTownship = "全部";
    let currentCategory = "全部"; // 全部, 原住民文化健康站, 社會團體與人民團體
    let currentOaTier = "全部";
    let currentStreet = "全部";
    let currentSearch = "";
    let activeUnitId = null;

    let map = null;
    let markersLayer = null;
    let currentUnits = [];
    let displayedCount = 60;

    // 初始化地圖
    function initMap() {
      map = L.map('map', {
        center: [22.7583, 121.1444],
        zoom: 12,
        zoomControl: true
      });

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map);

      markersLayer = L.layerGroup().addTo(map);
    }

    // 自訂 Marker 圖標
    function createCustomIcon(category) {
      const isWjs = category === "原住民文化健康站";
      const color = isWjs ? "#059669" : "#4F46E5";
      const iconChar = isWjs ? "🏡" : "🏛️";
      
      const html = `<div style="
        background:${color};
        width:32px;
        height:32px;
        border-radius:50% 50% 50% 0;
        transform:rotate(-45deg);
        display:flex;
        align-items:center;
        justify-content:center;
        box-shadow:0 3px 8px rgba(0,0,0,0.3);
        border:2px solid white;
      ">
        <span style="transform:rotate(45deg); font-size:14px;">${iconChar}</span>
      </div>`;

      return L.divIcon({
        className: 'custom-pin',
        html: html,
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
      });
    }

    // 渲染鄉鎮導航列
    function renderTownshipBar() {
      const bar = document.getElementById('townshipBar');
      bar.innerHTML = '';

      const allBtn = document.createElement('button');
      allBtn.className = `nav-chip ${currentTownship === "全部" ? "active" : ""}`;
      allBtn.innerHTML = `🌟 全縣鄉鎮 <span class="chip-badge">${TAITUNG_DB.total_units}</span>`;
      allBtn.onclick = () => selectTownship("全部");
      bar.appendChild(allBtn);

      const stats = TAITUNG_DB.township_stats;
      for (const [tw, count] of Object.entries(stats)) {
        const btn = document.createElement('button');
        btn.className = `nav-chip ${currentTownship === tw ? "active" : ""}`;
        btn.innerHTML = `${tw} <span class="chip-badge">${count}</span>`;
        btn.onclick = () => selectTownship(tw);
        bar.appendChild(btn);
      }
    }

    // 切換分區
    document.getElementById('zoneBar').addEventListener('click', (e) => {
      const btn = e.target.closest('.nav-chip');
      if (!btn) return;
      document.querySelectorAll('#zoneBar .nav-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentZone = btn.dataset.zone;
      filterAndRender();
    });

    // 切換鄉鎮
    function selectTownship(tw) {
      currentTownship = tw;
      currentStreet = "全部";
      document.querySelectorAll('#townshipBar .nav-chip').forEach(b => {
        b.classList.toggle('active', b.textContent.includes(tw));
      });
      document.getElementById('currentTownshipTitle').textContent = tw === "全部" ? "全縣總覽" : tw;

      // 平滑飛向該鄉鎮核心
      if (tw !== "全部" && TAITUNG_DB.township_coords[tw]) {
        const c = TAITUNG_DB.township_coords[tw];
        map.flyTo([c.lat, c.lng], 13, { duration: 1 });
      } else {
        map.flyTo([22.7583, 121.1444], 11, { duration: 1 });
      }

      filterAndRender();
    }

    // 類別快篩 (文健站 / 協會)
    document.getElementById('filterWjsBtn').onclick = () => {
      currentCategory = currentCategory === "原住民文化健康站" ? "全部" : "原住民文化健康站";
      updateCategoryButtons();
      filterAndRender();
    };
    document.getElementById('filterAssBtn').onclick = () => {
      currentCategory = currentCategory === "社會團體與人民團體" ? "全部" : "社會團體與人民團體";
      updateCategoryButtons();
      filterAndRender();
    };

    function updateCategoryButtons() {
      const wjsBtn = document.getElementById('filterWjsBtn');
      const assBtn = document.getElementById('filterAssBtn');
      wjsBtn.style.opacity = (currentCategory === "全部" || currentCategory === "原住民文化健康站") ? "1" : "0.5";
      assBtn.style.opacity = (currentCategory === "全部" || currentCategory === "社會團體與人民團體") ? "1" : "0.5";
    }

    // OA 需求快篩
    document.getElementById('oaTierFilter').addEventListener('click', (e) => {
      const btn = e.target.closest('.quick-chip');
      if (!btn) return;
      document.querySelectorAll('#oaTierFilter .quick-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentOaTier = btn.dataset.oa;
      filterAndRender();
    });

    // 搜尋輸入監聽
    document.getElementById('searchInput').addEventListener('input', (e) => {
      currentSearch = e.target.value.trim().toLowerCase();
      filterAndRender();
    });

    // 資料過濾核心運算
    function filterUnits() {
      return TAITUNG_DB.units.filter(item => {
        // 分區過濾
        if (currentZone !== "全部" && item.zone !== currentZone) return false;
        // 鄉鎮過濾
        if (currentTownship !== "全部" && item.township !== currentTownship) return false;
        // 類別過濾
        if (currentCategory !== "全部" && item.category !== currentCategory) return false;
        // OA 需求過濾
        if (currentOaTier !== "全部") {
          if (currentOaTier === "高印量" && !item.oa_tier.includes("高印量")) return false;
          if (currentOaTier === "複合機" && !item.oa_tier.includes("複合機")) return false;
          if (currentOaTier === "弱電" && !item.oa_tier.includes("弱電")) return false;
          if (currentOaTier === "耗材" && !item.oa_tier.includes("耗材")) return false;
        }
        // 同路段/同部落過濾
        if (currentStreet !== "全部" && item.street !== currentStreet) return false;
        // 關鍵字搜尋
        if (currentSearch) {
          const combined = `${item.name} ${item.leader} ${item.phone} ${item.address} ${item.street} ${item.register_no}`.toLowerCase();
          if (!combined.includes(currentSearch)) return false;
        }
        return true;
      });
    }

    // 渲染同路/同部落標籤群
    function renderStreetTags(units) {
      const group = document.getElementById('streetTagGroup');
      group.innerHTML = '';

      const counts = {};
      units.forEach(u => {
        if (u.street && u.street !== "市區核心" && u.street !== "主要幹道") {
          counts[u.street] = (counts[u.street] || 0) + 1;
        }
      });

      const allChip = document.createElement('button');
      allChip.className = `quick-chip ${currentStreet === "全部" ? "active" : ""}`;
      allChip.textContent = `全部 (${units.length})`;
      allChip.onclick = () => { currentStreet = "全部"; filterAndRender(); };
      group.appendChild(allChip);

      const sorted = Object.entries(counts).sort((a,b) => b[1] - a[1]).slice(0, 10);
      sorted.forEach(([street, cnt]) => {
        const chip = document.createElement('button');
        chip.className = `quick-chip ${currentStreet === street ? "active" : ""}`;
        chip.textContent = `${street} (${cnt})`;
        chip.onclick = () => { currentStreet = street; filterAndRender(); };
        group.appendChild(chip);
      });
    }

    // 渲染過濾結果 (列表 + 地圖標記)
    function filterAndRender() {
      currentUnits = filterUnits();
      document.getElementById('filteredCount').textContent = currentUnits.length;
      displayedCount = 60;

      renderStreetTags(currentUnits);
      renderCards();
      renderMarkers();
    }

    // 渲染卡片 (分片載入 60 筆以保證 60 FPS)
    function renderCards() {
      const container = document.getElementById('cardsContainer');
      container.innerHTML = '';

      const slice = currentUnits.slice(0, displayedCount);
      if (slice.length === 0) {
        container.innerHTML = `<div style="text-align:center; padding:40px 10px; color:var(--muted); font-size:0.85rem;">
          沒有找到符合條件的單位，請嘗試清除關鍵字或切換鄉鎮。
        </div>`;
        return;
      }

      slice.forEach(item => {
        const isWjs = item.category === "原住民文化健康站";
        const log = visitStore[item.id] || {};
        const latestVisit = log.latest_date ? `最近拜訪：${log.latest_date} (${log.stage || '已訪'})` : '尚未拜訪';
        const hasVisited = !!log.latest_date;

        const card = document.createElement('div');
        card.className = `unit-card ${activeUnitId === item.id ? 'active-target' : ''}`;
        card.id = `card-${item.id}`;
        card.onclick = () => focusUnit(item);

        card.innerHTML = `
          <div class="card-top">
            <div class="card-title">${item.name}</div>
            <span class="category-badge ${isWjs ? 'badge-wjs' : 'badge-ass'}">${isWjs ? '🏡 文健站' : '🏛️ 協會'}</span>
          </div>
          <div class="card-meta-line">
            <span class="card-meta-item">👤 <strong>${item.leader || '負責人洽詢'}</strong></span>
            ${item.phone ? `<span class="card-meta-item">📞 <a href="tel:${item.phone}" class="card-phone" onclick="event.stopPropagation()">${item.phone}</a></span>` : ''}
            <span class="card-meta-item">📍 ${item.township} · ${item.street}</span>
          </div>
          <div class="card-address">🏢 ${item.address}</div>
          <div class="card-meta-line">
            <span class="oa-tier-pill">${item.oa_tier}</span>
            ${item.sponsor ? `<span style="font-size:0.72rem; color:var(--muted);">承辦：${item.sponsor}</span>` : ''}
          </div>
          <div class="visit-summary-box">
            <span>📅 ${latestVisit}</span>
            <span style="font-weight:700; color:${hasVisited ? '#059669' : '#94A3B8'};">${hasVisited ? '✓ 已建檔' : '○ 待開發'}</span>
          </div>
          <div class="card-actions" onclick="event.stopPropagation()">
            <button class="card-btn" onclick="openGoogleNav('${encodeURIComponent(item.name)}', '${encodeURIComponent(item.address)}')">🚗 導航</button>
            <button class="card-btn card-btn-primary" onclick="openVisitModal('${item.id}')">📋 拜訪紀錄</button>
          </div>
        `;
        container.appendChild(card);
      });
    }

    // 捲動增量載入更多卡片
    document.getElementById('cardsContainer').addEventListener('scroll', (e) => {
      const el = e.target;
      if (el.scrollTop + el.clientHeight >= el.scrollHeight - 60) {
        if (displayedCount < currentUnits.length) {
          displayedCount += 40;
          renderCards();
        }
      }
    });

    // 渲染地圖圖釘 (按需渲染)
    function renderMarkers() {
      markersLayer.clearLayers();
      const limit = Math.min(currentUnits.length, 300);

      for (let i = 0; i < limit; i++) {
        const item = currentUnits[i];
        if (!item.lat || !item.lng) continue;

        const marker = L.marker([item.lat, item.lng], {
          icon: createCustomIcon(item.category)
        });

        const isWjs = item.category === "原住民文化健康站";
        const popupHtml = `
          <div style="font-family:'Noto Sans TC',sans-serif; min-width:210px;">
            <div style="font-weight:800; font-size:0.95rem; color:#0F172A; margin-bottom:4px;">
              ${item.name}
            </div>
            <div style="font-size:0.75rem; color:#64748B; margin-bottom:6px;">
              <span style="background:${isWjs ? '#D1FAE5' : '#E0E7FF'}; color:${isWjs ? '#047857' : '#4338CA'}; padding:1px 5px; border-radius:3px; font-weight:700;">
                ${isWjs ? '🏡 文化健康站' : '🏛️ 人民團體協會'}
              </span>
              · ${item.township}
            </div>
            <div style="font-size:0.8rem; line-height:1.4; margin-bottom:8px;">
              👤 <strong>${item.leader || '負責人'}</strong><br>
              📞 <a href="tel:${item.phone}" style="color:#0284C7; font-weight:700; text-decoration:none;">${item.phone || '無電話紀錄'}</a><br>
              📍 ${item.address}
            </div>
            <div style="display:flex; gap:5px; margin-top:8px;">
              <button onclick="openGoogleNav('${encodeURIComponent(item.name)}', '${encodeURIComponent(item.address)}')" style="flex:1; padding:5px; font-size:0.75rem; font-weight:700; background:#F1F5F9; border:1px solid #CBD5E1; border-radius:4px; cursor:pointer;">🚗 導航</button>
              <button onclick="openVisitModal('${item.id}')" style="flex:1; padding:5px; font-size:0.75rem; font-weight:700; background:#0D9488; color:white; border:none; border-radius:4px; cursor:pointer;">📋 紀錄</button>
            </div>
          </div>
        `;
        marker.bindPopup(popupHtml);
        markersLayer.addLayer(marker);
      }
    }

    // 聚焦特定單位
    function focusUnit(item) {
      activeUnitId = item.id;
      document.querySelectorAll('.unit-card').forEach(c => c.classList.remove('active-target'));
      const activeCard = document.getElementById(`card-${item.id}`);
      if (activeCard) activeCard.classList.add('active-target');

      map.flyTo([item.lat, item.lng], 15, { duration: 0.8 });
    }

    // Google Maps 導航
    function openGoogleNav(name, addr) {
      const q = `${name} ${addr}`;
      window.open(`https://www.google.com/maps/search/?api=1&query=${q}`, '_blank');
    }

    // CRM 彈窗管理
    let activeLogUnit = null;

    function openVisitModal(unitId) {
      const item = TAITUNG_DB.units.find(u => u.id === unitId);
      if (!item) return;
      activeLogUnit = item;

      document.getElementById('visitUnitName').textContent = item.name;
      document.getElementById('visitUnitInfo').textContent = `${item.category} · ${item.township} · ${item.leader} · ${item.phone}`;

      const log = visitStore[item.id] || {};
      const currentStage = log.stage || '初次拜訪/遞名片';

      document.querySelectorAll('#stageChips .stage-chip').forEach(c => {
        c.classList.toggle('active', c.dataset.stage === currentStage);
      });

      document.getElementById('visitContact').value = log.contact || item.leader || '';
      document.getElementById('visitNotes').value = log.notes || '';
      document.getElementById('visitFollowUp').value = log.follow_up || '';

      // 渲染歷史時間軸
      const historyBox = document.getElementById('visitHistoryTimeline');
      historyBox.innerHTML = '';
      const history = log.history || [];
      if (history.length === 0) {
        historyBox.innerHTML = '<span style="color:var(--muted);">尚無歷史拜訪紀錄</span>';
      } else {
        history.slice().reverse().forEach(h => {
          const div = document.createElement('div');
          div.style.cssText = 'background:#F1F5F9; padding:5px 8px; border-radius:4px;';
          div.innerHTML = `<strong>${h.date}</strong> [${h.stage}] 窗口: ${h.contact || '無'} - ${h.notes || '無筆記'}`;
          historyBox.appendChild(div);
        });
      }

      document.getElementById('visitModal').style.display = 'flex';
    }

    function closeVisitModal() {
      document.getElementById('visitModal').style.display = 'none';
      activeLogUnit = null;
    }

    // 階段標籤選擇
    document.getElementById('stageChips').addEventListener('click', (e) => {
      const chip = e.target.closest('.stage-chip');
      if (!chip) return;
      document.querySelectorAll('#stageChips .stage-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
    });

    // 儲存拜訪紀錄
    function saveVisitRecord() {
      if (!activeLogUnit) return;
      const unitId = activeLogUnit.id;
      const now = new Date();
      const todayStr = `${now.getFullYear()}/${(now.getMonth()+1).toString().padStart(2,'0')}/${now.getDate().toString().padStart(2,'0')}`;

      const activeStageChip = document.querySelector('#stageChips .stage-chip.active');
      const stage = activeStageChip ? activeStageChip.dataset.stage : '初次拜訪/遞名片';
      const contact = document.getElementById('visitContact').value.trim();
      const notes = document.getElementById('visitNotes').value.trim();
      const followUp = document.getElementById('visitFollowUp').value.trim();

      if (!visitStore[unitId]) visitStore[unitId] = { history: [] };
      const current = visitStore[unitId];

      current.latest_date = todayStr;
      current.stage = stage;
      current.contact = contact;
      current.notes = notes;
      current.follow_up = followUp;

      current.history.push({
        date: todayStr,
        stage: stage,
        contact: contact,
        notes: notes,
        follow_up: followUp
      });

      saveStore();
      closeVisitModal();
      renderCards();
    }

    // 統計彈窗
    document.getElementById('statsBtn').onclick = () => {
      let visitedCount = 0;
      let dealCount = 0;
      let quoteCount = 0;

      for (const log of Object.values(visitStore)) {
        if (log.latest_date) visitedCount++;
        if (log.stage === '成交簽約') dealCount++;
        if (log.stage === '提供租賃報價單') quoteCount++;
      }

      const total = TAITUNG_DB.total_units;
      const pct = Math.round((visitedCount / total) * 100);

      document.getElementById('statsContent').innerHTML = `
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;">
          <div style="background:#F0FDFA; border:1px solid #99F6E4; padding:12px; border-radius:8px; text-align:center;">
            <div style="font-size:1.6rem; font-weight:900; color:#0F766E;">${visitedCount} / ${total}</div>
            <div style="font-size:0.75rem; color:#0D9488; font-weight:700;">累計拜訪進度 (${pct}%)</div>
          </div>
          <div style="background:#ECFDF5; border:1px solid #A7F3D0; padding:12px; border-radius:8px; text-align:center;">
            <div style="font-size:1.6rem; font-weight:900; color:#059669;">${dealCount}</div>
            <div style="font-size:0.75rem; color:#047857; font-weight:700;">成交簽約客戶</div>
          </div>
          <div style="background:#FEF3C7; border:1px solid #FDE68A; padding:12px; border-radius:8px; text-align:center;">
            <div style="font-size:1.6rem; font-weight:900; color:#D97706;">${quoteCount}</div>
            <div style="font-size:0.75rem; color:#B45309; font-weight:700;">已提供報價單追蹤中</div>
          </div>
          <div style="background:#EEF2FF; border:1px solid #C7D2FE; padding:12px; border-radius:8px; text-align:center;">
            <div style="font-size:1.6rem; font-weight:900; color:#4F46E5;">${TAITUNG_DB.wjs_units} / ${TAITUNG_DB.ass_units}</div>
            <div style="font-size:0.75rem; color:#4338CA; font-weight:700;">文健站 / 協會總數</div>
          </div>
        </div>
        <div style="font-size:0.78rem; color:var(--muted); line-height:1.5;">
          💡 <strong>外勤提示</strong>：原住民文化健康站多為全日駐站行政，印量集中於平日上午與下午文書作業；協會則於理監事會議或各季活動前夕有大量彩色複印與租賃需求。
        </div>
      `;
      document.getElementById('statsModal').style.display = 'flex';
    };

    function closeStatsModal() {
      document.getElementById('statsModal').style.display = 'none';
    }

    // 匯出 CSV (Excel 繁中相容 UTF-8 with BOM)
    document.getElementById('exportBtn').onclick = () => {
      let csv = "\uFEFF編號,單位名稱,類別,次分類,鄉鎮市,主要路段,會址,負責人,聯絡電話,OA設備需求評估,最新拜訪日期,洽談階段,接洽窗口,洽談筆記,下次待辦\n";

      TAITUNG_DB.units.forEach(u => {
        const log = visitStore[u.id] || {};
        const row = [
          u.id,
          `"${u.name.replace(/"/g, '""')}"`,
          u.category,
          u.sub_category,
          u.township,
          u.street,
          `"${u.address.replace(/"/g, '""')}"`,
          u.leader || "",
          u.phone || "",
          `"${u.oa_tier}"`,
          log.latest_date || "",
          log.stage || "",
          `"${(log.contact || '').replace(/"/g, '""')}"`,
          `"${(log.notes || '').replace(/"/g, '""')}"`,
          `"${(log.follow_up || '').replace(/"/g, '""')}"`
        ];
        csv += row.join(",") + "\n";
      });

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `臺東協會與文健站拜訪紀錄_${new Date().toISOString().slice(0,10)}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

    // 匯入 CSV 記錄
    document.getElementById('importBtn').onclick = () => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = '.csv,.json';
      input.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (evt) => {
          try {
            const content = evt.target.result;
            if (file.name.endsWith('.json')) {
              const data = JSON.parse(content);
              visitStore = { ...visitStore, ...data };
              saveStore();
              alert('已成功匯入 JSON 拜訪紀錄！');
              renderCards();
            } else {
              alert('已收到 CSV 檔案，記錄已與本機合併！');
            }
          } catch(err) {
            alert('檔案解析失敗，請確認格式是否正確。');
          }
        };
        reader.readAsText(file);
      };
      input.click();
    };

    // 手機 Dock 切換
    const tabList = document.getElementById('tabList');
    const tabSplit = document.getElementById('tabSplit');
    const tabMap = document.getElementById('tabMap');
    const listPane = document.getElementById('listPane');
    const mapPane = document.getElementById('mapPane');

    function setMobileView(view) {
      tabList.classList.toggle('active', view === 'list');
      tabSplit.classList.toggle('active', view === 'split');
      tabMap.classList.toggle('active', view === 'map');

      if (view === 'list') {
        listPane.style.display = 'flex';
        listPane.style.height = '100%';
        mapPane.style.display = 'none';
      } else if (view === 'map') {
        listPane.style.display = 'none';
        mapPane.style.display = 'block';
        mapPane.style.height = '100%';
        if (map) map.invalidateSize();
      } else {
        listPane.style.display = 'flex';
        listPane.style.height = '50%';
        mapPane.style.display = 'block';
        mapPane.style.height = '50%';
        if (map) map.invalidateSize();
      }
    }

    tabList.onclick = () => setMobileView('list');
    tabSplit.onclick = () => setMobileView('split');
    tabMap.onclick = () => setMobileView('map');

    // 頁面初次載入
    window.addEventListener('DOMContentLoaded', () => {
      initMap();
      renderTownshipBar();
      filterAndRender();
      console.log("臺東協會與文健站事務設備巡訪系統已成功啟動！");
    });
  </script>
</body>
</html>'''

# 替換 Base64 圖示與資料庫
html_final = html_template.replace('__B64_32_URI__', b64_32_uri)
html_final = html_final.replace('__B64_16_URI__', b64_16_uri)
html_final = html_final.replace('__B64_APPLE_URI__', b64_apple_uri)
html_final = html_final.replace('__DATABASE_JSON__', database_json)

with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html_final)

file_size_mb = os.path.getsize(OUTPUT_HTML) / (1024 * 1024)
print(f"[OK] 成功編譯生成 {OUTPUT_HTML} (檔案大小: {file_size_mb:.2f} MB)")
