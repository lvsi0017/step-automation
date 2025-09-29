#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import random
import time
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 多账号配置
ACCOUNTS = [
    {"username": "账号1", "password": "密码1"},
    {"username": "账号2", "password": "密码2"},
]

# 步数范围配置
STEP_RANGES = {
    8: {"min": 6000, "max": 10000},
    12: {"min": 8000, "max": 14000},
    16: {"min": 10000, "max": 18000},
    20: {"min": 12000, "max": 22000},
    22: {"min": 15000, "max": 24000}
}

# 默认步数（当不在指定时间段时使用）
DEFAULT_STEPS = 24465

class StepSubmitter:
    def __init__(self):
        self.session = requests.Session()
        # 设置浏览器般的请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.128 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    def login(self, username, password):
        """模拟登录"""
        url = "https://example.com/login"  # 替换为实际登录接口地址
        payload = {'username': username, 'password': password}
        response = self.session.post(url, headers=self.headers, data=payload)
        if response.status_code == 200 and response.json().get('success'):
            logger.info(f"{username} 登录成功")
            return True
        else:
            logger.error(f"{username} 登录失败: {response.text}")
            return False

    def submit_steps(self, steps):
        """提交步数"""
        url = "https://example.com/submit_steps"  # 替换为实际提交接口地址
        payload = {'steps': steps}
        response = self.session.post(url, headers=self.headers, data=payload)
        if response.status_code == 200 and response.json().get('success'):
            logger.info(f"提交步数 {steps} 成功")
        else:
            logger.error(f"提交步数 {steps} 失败: {response.text}")

    def get_random_steps(self):
        """获取随机步数"""
        current_hour = datetime.now().hour
        step_range = STEP_RANGES.get(current_hour, None)
        if step_range:
            min_steps = step_range['min']
            max_steps = step_range['max']
            return random.randint(min_steps, max_steps)
        else:
            return DEFAULT_STEPS

def main():
    step_submitter = StepSubmitter()
    for account in ACCOUNTS:
        if step_submitter.login(account['username'], account['password']):
            steps = step_submitter.get_random_steps()
            step_submitter.submit_steps(steps)
        time.sleep(random.uniform(1, 3))  # 模拟不同账号之间的时间间隔

if __name__ == "__main__":
    main()


