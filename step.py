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

ACCOUNTS   = json.loads(os.getenv("ACCOUNTS", "[]"))
STEP_RANGES = {5: {"min": 60000, "max": 70000}, 6: {"min": 60000, "max": 70000}}
DEFAULT_STEPS = 65535
results = []

def wx_push(title, content):
    token = os.getenv("PUSHPLUS_TOKEN")
    if not token:
        logger.warning("未设置 PUSHPLUS_TOKEN，跳过推送")
        return
    url = "https://www.pushplus.plus/send"
    data = {"token": token, "title": title, "content": content, "template": "txt"}
    try:
        rsp = requests.post(url, json=data, timeout=5)
        logger.info("PushPlus 推送结果：%s", rsp.text)
    except Exception as e:
        logger.error("PushPlus 推送异常：%s", e)

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
        ok = fail = 0
        for idx, acc in enumerate(ACCOUNTS, 1):
            logger.info(f'[{idx}/{len(ACCOUNTS)}] 账号 {acc["username"]}')
            steps = self.get_steps()
            success, msg = self.submit(acc['username'], acc['password'], steps)
            results.append({'user': acc['username'], 'steps': steps, 'ok': success})
            if success:
                ok += 1
                logger.info('✓ %s', msg)
            else:
                fail += 1
                logger.error('✗ %s', msg)
            if idx < len(ACCOUNTS):
                time.sleep(5)

        lines = ["步数提交日报", f"成功 {ok} 账号，失败 {fail} 账号。"]
        for r in results:
            lines.append(f"{r['user']}: {r['steps']} 步")
        wx_push("步数提交日报", "<br>".join(lines))

        logger.info('全部完成 → 成功 %d / 失败 %d', ok, fail)
        return ok, fail

if __name__ == '__main__':
    if not ACCOUNTS:
        logger.error('未设置 ACCOUNTS 环境变量')
        exit(1)
    submitter = StepSubmitter()
    ok, fail = submitter.run()
    exit(0 if fail == 0 else 1)
