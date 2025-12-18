#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import datetime
import re
import requests
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from tenacity import retry, wait_exponential, stop_after_attempt
import logging
import argparse
from io import StringIO

# ログ設定
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )

# 設定ファイル読み込み
def load_config(path='config.json'):
    with open(path) as f:
        return json.load(f)

# HTMLテーブル取得
def get_html_tables(url):
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'html.parser')
    return bs.find_all('table')

# 値抽出（StringIOを使い、FutureWarningを回避）
def extract_value(tables, table_idx, row_idx, time_idx):
    table = tables[table_idx]
    df = pd.read_html(StringIO(str(table)), header=0)[0]
    val = df.iloc[row_idx].iat[-1]
    if not re.match(r"^-?\d+(\.\d+)?$", str(val)):
        logging.warning(f"非数値データをスキップ: {val}")
        return None, None
    time_str = df.iloc[time_idx].iat[-1]
    return time_str, float(val)

# 時刻文字列を datetime に変換
def convert_to_datetime(time_str):
    time_str = time_str.replace('：', ':')
    if time_str == '24:00':
        time_str = '00:00'
    h, m = map(int, re.findall(r"\d+", time_str))
    now = datetime.datetime.now()
    dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
    if time_str == '00:00':
        dt += datetime.timedelta(days=1)
    return dt

# InfluxDB書き込み（再試行付き）
@retry(wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
def write_to_influx(time_obj, value, measurement, location, influx_conf):
    url = influx_conf['url']
    token = influx_conf['token']
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/octet-stream'
    }
    line = f"{measurement},location={location} value={value} {int(time_obj.timestamp())}"
    resp = requests.post(url, headers=headers, data=line)
    if resp.status_code not in (200, 204):
        logging.error(f"InfluxDB書き込み失敗: {resp.status_code} {resp.text}")
        resp.raise_for_status()
    return resp.status_code

# 定期実行ジョブ
def job():
    logging.info("ジョブ開始")
    cfg = load_config(os.getenv('KASEN2INFLUXDB_CONFIG_PATH', 'config.json'))
    df = pd.read_csv(cfg['csv']['path'])
    influx_conf = cfg['influxdb']

    for _, row in df.iterrows():
        meas = row['measurement']
        loc = row['location']
        url = row['url']
        tbl = int(row['table_number'])
        t_idx = int(row['time_row_position'])
        v_idx = int(row['row_position'])
        try:
            tables = get_html_tables(url)
            t_str, val = extract_value(tables, tbl, v_idx, t_idx)
            if val is None:
                continue
            dt = convert_to_datetime(t_str)
            status = write_to_influx(dt, val, meas, loc, influx_conf)
            logging.info(f"{meas}@{loc}: {val} at {dt} -> HTTP {status}")
        except Exception as e:
            logging.exception(f"エラー: {meas} 処理中に例外発生: {e}")

# メインループ
def main_loop(config_path: str, once: bool = False, dry_run: bool = False):
    """
    設定ファイルパスを指定し、一度だけ実行 or 定期実行を切り替える
    :param config_path: 設定ファイル(json) のパス
    :param once: True なら一回だけ job() を実行
    :param dry_run: True なら DB 書き込みをスキップして結果を出力
    """
    setup_logging()
    os.environ['KASEN2INFLUXDB_CONFIG_PATH'] = config_path

    if once:
        cfg = load_config(config_path)
        df = pd.read_csv(cfg['csv']['path'])
        influx_conf = cfg['influxdb']
        for _, row in df.iterrows():
            meas = row['measurement']
            loc = row['location']
            url = row['url']
            tbl = int(row['table_number'])
            t_idx = int(row['time_row_position'])
            v_idx = int(row['row_position'])
            t_str, val = extract_value(get_html_tables(url), tbl, v_idx, t_idx)
            if val is None:
                continue
            dt = convert_to_datetime(t_str)
            if dry_run:
                print(f"[DRY-RUN] {meas}@{loc}: {val} at {dt}")
            else:
                status = write_to_influx(dt, val, meas, loc, influx_conf)
                logging.info(f"{meas}@{loc}: {val} at {dt} -> HTTP {status}")
        return

    scheduler = BlockingScheduler()
    scheduler.add_job(
        job, 'interval', minutes=10,
        max_instances=1, coalesce=True, misfire_grace_time=300,
        next_run_time=datetime.datetime.now()
    )
    logging.info("Scheduler起動: 10分間隔でジョブ実行")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler停止")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kasen2InfluxDB Runner')
    parser.add_argument('--config', '-c', default='config.json', help='設定ファイルのパス')
    parser.add_argument('--once', action='store_true', help='一度だけ実行')
    parser.add_argument('--dry-run', action='store_true', help='DB書き込みをスキップ')
    args = parser.parse_args()
    main_loop(config_path=args.config, once=args.once, dry_run=args.dry_run)
