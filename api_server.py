#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import os
import sys
from flask import Flask, request, jsonify

# 添加项目根目录到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from config import load_config, conf
from lib.gewechat import GewechatClient
from common.log import logger

app = Flask(__name__)

class NotificationService:
    """通知服务类，用于发送消息通知到微信用户"""
    
    def __init__(self):
        """初始化通知服务"""
        load_config()
        self.base_url = conf().get("gewechat_base_url")
        self.token = conf().get("gewechat_token")
        self.app_id = conf().get("gewechat_app_id")
        
        if not all([self.base_url, self.token, self.app_id]):
            error_msg = "gewechat配置不完整，无法初始化通知服务"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        self.client = GewechatClient(self.base_url, self.token)
        logger.info(f"通知服务初始化成功，base_url: {self.base_url}, app_id: {self.app_id}")
    
    def check_online(self):
        """检查gewechat是否在线
        
        Returns:
            tuple: (是否在线, 错误信息)
        """
        try:
            online_status = self.client.check_online(self.app_id)
            if not online_status:
                return False, "获取在线状态失败"
                
            if not online_status.get('data', False):
                logger.info("Gewechat用户未在线")
                return False, "用户未登录"
                
            return True, None
        except Exception as e:
            error_msg = f"检查gewechat在线状态失败: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def send_notification(self, wxid, content):
        """发送通知消息到指定的微信用户
        
        Args:
            wxid (str): 接收者的微信ID
            content (str): 要发送的消息内容
            
        Returns:
            dict: 发送结果
        """
        is_online, error_msg = self.check_online()
        if not is_online:
            logger.error(f"发送消息失败: {error_msg}")
            return {"success": False, "message": error_msg}
        
        try:
            result = self.client.post_text(self.app_id, wxid, content)
            if result.get('ret') == 200:
                logger.info(f"消息发送成功，接收者: {wxid}, 内容: {content}")
                return {"success": True, "message": "消息发送成功", "data": result.get('data')}
            else:
                error_msg = f"消息发送失败，错误信息: {result.get('msg')}"
                logger.error(error_msg)
                return {"success": False, "message": error_msg}
        except Exception as e:
            error_msg = f"发送消息异常: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

# 初始化通知服务
notification_service = None
try:
    notification_service = NotificationService()
    logger.info("通知服务初始化成功")
except Exception as e:
    logger.error(f"通知服务初始化失败: {str(e)}")

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    if notification_service is None:
        return jsonify({"status": "error", "message": "通知服务未初始化"}), 500
    
    is_online, error_msg = notification_service.check_online()
    if not is_online:
        return jsonify({"status": "error", "message": error_msg}), 503
    
    return jsonify({"status": "ok", "message": "服务正常运行中"}), 200

@app.route('/api/notify', methods=['POST'])
def notify():
    """接收外部应用发送的通知消息并转发到微信
    
    请求体格式:
    {
        "wxid": "wxid_xxxxx",
        "content": "要发送的消息内容"
    }
    
    响应格式:
    {
        "success": true/false,
        "message": "成功或失败的消息"
    }
    """
    if notification_service is None:
        return jsonify({"success": False, "message": "通知服务未初始化"}), 500
    
    try:
        data = request.json
        
        # 验证请求数据
        if not data:
            return jsonify({"success": False, "message": "请求体不能为空"}), 400
        
        wxid = data.get('wxid')
        content = data.get('content')
        
        if not wxid:
            return jsonify({"success": False, "message": "wxid不能为空"}), 400
        if not content:
            return jsonify({"success": False, "message": "content不能为空"}), 400
        
        # 发送通知
        result = notification_service.send_notification(wxid, content)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"处理通知请求异常: {str(e)}")
        return jsonify({"success": False, "message": f"处理请求失败: {str(e)}"}), 500

if __name__ == '__main__':
    # 设置日志级别
    app.logger.setLevel(logging.INFO)
    
    # 获取端口，默认为8080
    port = int(os.environ.get('PORT', 8080))
    
    # 启动服务
    app.run(host='0.0.0.0', port=port, debug=False)
    logger.info(f"通知服务API已启动，监听端口: {port}") 