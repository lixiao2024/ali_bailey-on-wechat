#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import requests
import time
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mock_external_app")

class MockExternalApp:
    """模拟外部应用，用于测试通知接口"""
    
    def __init__(self, api_url):
        """初始化模拟外部应用
        
        Args:
            api_url (str): 通知接口的URL，例如 http://localhost:8080/api/notify
        """
        self.api_url = api_url
        logger.info(f"模拟外部应用初始化，API地址: {api_url}")
    
    def check_service_health(self):
        """检查通知服务的健康状态
        
        Returns:
            bool: 服务是否健康
        """
        try:
            health_url = self.api_url.replace("/api/notify", "/health")
            response = requests.get(health_url, timeout=5)
            
            if response.status_code == 200:
                logger.info("通知服务健康检查通过")
                return True
            else:
                logger.error(f"通知服务健康检查失败，状态码: {response.status_code}")
                logger.error(f"响应内容: {response.text}")
                return False
        
        except requests.RequestException as e:
            logger.error(f"健康检查请求异常: {str(e)}")
            return False
    
    def send_notification(self, wxid, content):
        """发送通知消息
        
        Args:
            wxid (str): 接收者的微信ID
            content (str): 要发送的消息内容
            
        Returns:
            dict: 发送结果
        """
        try:
            payload = {
                "wxid": wxid,
                "content": content
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            logger.info(f"发送通知，接收者: {wxid}, 内容: {content}")
            
            response = requests.post(
                self.api_url,
                data=json.dumps(payload),
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"通知发送成功: {result}")
                return result
            else:
                logger.error(f"通知发送失败，状态码: {response.status_code}")
                logger.error(f"响应内容: {response.text}")
                return {
                    "success": False,
                    "message": f"请求失败，状态码: {response.status_code}"
                }
        
        except requests.RequestException as e:
            error_msg = f"发送通知请求异常: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": error_msg
            }
    
    def simulate_task_completion(self, wxid, task_name, interval=5):
        """模拟任务完成并发送通知
        
        Args:
            wxid (str): 接收者的微信ID
            task_name (str): 任务名称
            interval (int): 模拟任务执行的时间间隔（秒）
            
        Returns:
            dict: 发送结果
        """
        logger.info(f"开始模拟任务 '{task_name}' 执行...")
        
        # 模拟任务执行
        time.sleep(interval)
        
        # 构造通知消息
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = f"【任务完成通知】\n您的任务「{task_name}」已经完成！\n完成时间: {current_time}\n请及时查看处理结果。"
        
        # 发送通知
        logger.info(f"任务 '{task_name}' 已完成，发送通知...")
        return self.send_notification(wxid, content)

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="模拟外部应用通知测试工具")
    parser.add_argument("--url", type=str, default="http://localhost:8080/api/notify", 
                       help="通知接口URL")
    parser.add_argument("--wxid", type=str, required=True, 
                       help="接收者的微信ID")
    parser.add_argument("--task", type=str, default="数据处理", 
                       help="模拟的任务名称")
    parser.add_argument("--interval", type=int, default=2, 
                       help="模拟任务执行的时间间隔（秒）")
    parser.add_argument("--message", type=str, 
                       help="直接发送指定消息，不使用任务模拟模式")
    
    args = parser.parse_args()
    
    # 初始化模拟应用
    app = MockExternalApp(args.url)
    
    # 检查服务健康状态
    if not app.check_service_health():
        logger.error("服务健康检查失败，退出测试")
        return 1
    
    # 发送通知
    if args.message:
        # 直接发送指定消息
        result = app.send_notification(args.wxid, args.message)
    else:
        # 使用任务模拟模式
        result = app.simulate_task_completion(args.wxid, args.task, args.interval)
    
    # 输出结果
    if result["success"]:
        logger.info("测试成功完成")
        return 0
    else:
        logger.error(f"测试失败: {result.get('message')}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 