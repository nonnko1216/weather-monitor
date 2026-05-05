import requests
import os
import time
from urllib.parse import urlparse
from datetime import datetime, timedelta

SAVE_DIR = "files"
os.makedirs(SAVE_DIR, exist_ok=True)

# --- 前日のURLを生成する関数 ---
def get_jma_yesterday_url():
    yesterday = datetime.now() - timedelta(days=1)
    yyyy_mm = yesterday.strftime("%Y%m")
    yyyy_mm_dd = yesterday.strftime("%Y%m%d")
    # 固定時刻 1200 で生成
    base_url = f"https://www.data.jma.go.jp/yoho/data/wxchart/quick/{yyyy_mm}/ASAS_COLOR_{yyyy_mm_dd}1200.pdf"
    return base_url

files = [
    {"name": "file01_AUPQ35", "url": "https://www.jma.go.jp/bosai/numericmap/data/nwpmap/aupq35_12.pdf"},
    {"name": "file02_AUPQ78", "url": "https://www.jma.go.jp/bosai/numericmap/data/nwpmap/aupq78_12.pdf"},
    {"name": "file03_AXFE578", "url": "https://www.jma.go.jp/bosai/numericmap/data/nwpmap/axfe578_12.pdf"},
    {"name": "file07_FXFE502", "url": "https://www.jma.go.jp/bosai/numericmap/data/nwpmap/fxfe502_12.pdf"},
    {"name": "file08_FXFE5782", "url": "https://www.jma.go.jp/bosai/numericmap/data/nwpmap/fxfe5782_12.pdf"},
    {"name": "file09_FXJP854", "url": "https://www.jma.go.jp/bosai/numericmap/data/nwpmap/fxjp854_12.pdf"},
    {"name": "file11_weather_yesterday_21", "url": get_jma_yesterday_url()},
    {"name": "file12_weather_today_latest", "url": "https://www.data.jma.go.jp/yoho/data/wxchart/quick/ASAS_COLOR.pdf"}, 
    {"name": "file13_FSAS24_COLOR_ASIA", "url": "https://www.data.jma.go.jp/yoho/data/wxchart/quick/FSAS24_COLOR_ASIA.pdf"},
    {"name": "fileA_FBJP", "url": "https://www.data.jma.go.jp/airinfo/data/pict/fbjp/fbjp.png"},
    {"name": "fileB_low_level_sigwx", "url": "https://www.data.jma.go.jp/airinfo/data/pict/low-level_sigwx/fbsn39.png"},
    {"name": "fileC1_low_level_sigwx_miyagi", "url": "https://www.data.jma.go.jp/airinfo/data/pict/low-level_sigwx_p/Lsigp_Fig204.png"},
    {"name": "fileC2_low_level_sigwx_fukushima", "url": "https://www.data.jma.go.jp/airinfo/data/pict/low-level_sigwx_p/Lsigp_Fig206.png"},
    {"name": "fileD_taf", "url": "https://www.data.jma.go.jp/airinfo/data/pict/taf/QMCD98_RJSS.png"}
]

headers = {"User-Agent": "Mozilla/5.0"}

for file in files:
    try:
        # 実行直前に1秒待機
        time.sleep(1)
        
        # 安全策：URLが空の場合はスキップ
        if not file.get("url"):
            print(f"失敗: {file['name']} のURLが設定されていません。")
            continue

        # キャッシュ対策のパラメータ付与
        url_with_param = f"{file['url']}?t={time.time()}"
        
        # 保存処理（ストリームモードで開始）
        with requests.get(url_with_param, headers=headers, timeout=15, stream=True) as res:
            res.raise_for_status()

            # 拡張子の判定（URLのパス部分から取得）
            parsed_url = urlparse(file["url"])
            ext = os.path.splitext(parsed_url.path)[1]
            if not ext:
                ext = ".bin"

            # ファイル名の組み立て
            safe_name = os.path.basename(file["name"]) + ext
            filename = os.path.join(SAVE_DIR, safe_name)

            # 書き込み処理
            with open(filename, "wb") as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f"保存成功: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"失敗: {file['name']} | エラー: {e}")