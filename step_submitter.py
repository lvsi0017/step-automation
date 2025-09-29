#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import random
import time
import logging
import requests
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 从环境变量读取账号
ACCOUNTS = json.loads(os.getenv("ACCOUNTS", "[]"))
STEP_RANGES = {5: {"min": 60000, "max": 70000}, 6: {"min": 60000, "max": 70000}}
DEFAULT_STEPS = 65535

class StepSubmitter:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.128 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://m.cqzz.top',
            'Referer': 'https://m.cqzz.top/',
            'X-Requested-With': 'XMLHttpRequest'
        })
        self.url = 'https://wzz.wangzouzou.com/motion/api/motion/Xiaomi'

    def get_steps(self):
        h = datetime.now().hour
        closest = min(STEP_RANGES.keys(), key=lambda x: abs(x - h))
        if abs(h - closest) <= 2:
            cfg = STEP_RANGES[closest]
            return random.randint(cfg['min'], cfg['max'])
        return DEFAULT_STEPS

    def submit(self, phone, pwd, steps):
        try:
            rsp = self.s.post(self.url, data={'phone': phone, 'pwd': pwd, 'num': steps}, timeout=30)
            if rsp.status_code != 200:
                return False, f'HTTP {rsp.status_code}'
            res = rsp.json()
            if res.get('code') == 200:
                return True, f'提交成功 → {steps} 步'
            return False, res.get('data', '未知错误')
        except Exception as e:
            return False, str(e)

    def run(self):
        ok, fail = 0, 0
        for idx, acc in enumerate(ACCOUNTS, 1):
            logger.info(f'[{idx}/{len(ACCOUNTS)}] 账号 {acc["username"]}')
            steps = self.get_steps()
            succ, msg = self.submit(acc['username'], acc['password'], steps)
            if succ:
                ok += 1
                logger.info(f'✓ {msg}')
            else:
                fail += 1
                logger.error(f'✗ {msg}')
            if idx < len(ACCOUNTS):
                time.sleep(5)
        logger.info(f'全部完成 → 成功 {ok} / 失败 {fail}')
        exit(0 if fail == 0 else 1)

if __name__ == '__main__':
    if not ACCOUNTS:
        logger.error('未检测到 ACCOUNTS 环境变量，请检查 GitHub Secrets 配置')
        exit(1)
    StepSubmitter().run()
