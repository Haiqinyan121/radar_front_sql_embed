#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证数据从主函数传输到数据库的功能
"""

import sys
import os
import time
import random

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入数据库模块
from db import MySQLHelper

def test_data_transfer():
    """测试数据从主函数传输到数据库的功能"""
    print("=== 开始测试数据传输功能 ===")
    
    try:
        # 1. 初始化数据库连接
        print("1. 正在连接数据库...")
        db = MySQLHelper('localhost', 'root', 'root', 'hmbld')
        print("   ✅ 数据库连接成功")
        
        # 2. 创建测试数据（模拟雷达处理后的数据）
        print("2. 正在生成测试数据...")
        process_start_time = time.time()
        time.sleep(0.1)  # 模拟处理时间
        process_end_time = time.time()
        
        # 模拟主函数中生成的数据
        test_data = {
            'record_time': process_end_time,
            'heart_rate': random.uniform(60, 100),  # 随机心率 (60-100 bpm)
            'breathe_speed': random.uniform(1.0, 5.0),  # 随机呼吸速度 
            'target_distance': random.uniform(0.5, 5.0),  # 随机距离 (0.5-5.0米)
            'target_bin': random.randint(10, 100),  # 随机距离索引
            'presence_detected': True,  # 模拟检测到稳定存在
            'processing_time_ms': (process_end_time - process_start_time) * 1000  # 计算处理时间
        }
        
        print(f"   ✅ 生成的测试数据:")
        for key, value in test_data.items():
            print(f"      {key}: {value}")
        
        # 3. 将数据插入到数据库（模拟主函数中的保存逻辑）
        print("3. 正在将数据插入数据库...")
        inserted_id = db.insert('heart_rate', test_data)
        print(f"   ✅ 数据插入成功，记录ID: {inserted_id}")
        
        # 4. 验证数据是否成功插入
        print("4. 正在验证数据是否成功保存...")
        # 查询刚插入的数据
        result = db.query("SELECT * FROM heart_rate WHERE id = %s", (inserted_id,))
        
        if result:
            print(f"   ✅ 数据验证成功!")
            print(f"   从数据库查询到的记录:")
            for key, value in result[0].items():
                print(f"      {key}: {value}")
        else:
            print("   ❌ 数据验证失败，未查询到插入的记录")
        
        # 5. 查询最近10条记录，确认数据库功能正常
        print("5. 查询最近10条记录:")
        recent_data = db.query("SELECT * FROM heart_rate ORDER BY id DESC LIMIT 10")
        for i, record in enumerate(recent_data, 1):
            print(f"   记录 {i}: ID={record['id']}, 心率={record['heart_rate']}, 时间戳={record['record_time']}")
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False
    finally:
        # 关闭数据库连接
        try:
            db.close()
            print("6. 数据库连接已关闭")
        except:
            pass
    
    print("=== 数据传输功能测试完成 ===")
    return True

if __name__ == "__main__":
    test_data_transfer()