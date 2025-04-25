# encoding:utf-8

import os
import time
from http import HTTPStatus

from dashscope import Application

from bot.bot import Bot
from bot.ali_bailey.ali_bailey_session import AliBaileySession
from bot.session_manager import SessionManager
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from common import const
from config import conf, load_config

class AliBaileyBot(Bot):
    def __init__(self):
        super().__init__()
        self.sessions = SessionManager(AliBaileySession, model="ali_bailey")
    
    def api_key(self):
        """获取阿里百炼 API Key"""
        return conf().get("ali_bailey_api_key", "")
    
    def app_id(self):
        """获取应用 ID"""
        return conf().get("ali_bailey_app_id", "")
    
    def api_base(self):
        """获取 API 基础 URL"""
        return conf().get("ali_bailey_api_base", "https://api.ali-bailey.com")

    def reply(self, query, context=None):
        """处理用户输入并返回回复"""
        if context.type == ContextType.TEXT:
            logger.info("[ALI_BAILEY] query={}".format(query))
            
            session_id = context["session_id"]
            reply = None
            
            # 处理特殊命令
            clear_memory_commands = conf().get("clear_memory_commands", ["#清除记忆"])
            if query in clear_memory_commands:
                self.sessions.clear_session(session_id)
                reply = Reply(ReplyType.INFO, "记忆已清除")
                return reply
            elif query == "#清除所有":
                self.sessions.clear_all_session()
                reply = Reply(ReplyType.INFO, "所有人记忆已清除")
                return reply
            elif query == "#更新配置":
                load_config()
                reply = Reply(ReplyType.INFO, "配置已更新")
                return reply
                
            # 获取会话
            session = self.sessions.session_query(query, session_id)
            
            # 调用 API 获取回复
            reply_content = self.reply_text(session)
            
            if reply_content.get("status_code") != HTTPStatus.OK:
                error_msg = f"API 调用失败：{reply_content.get('message', '未知错误')}"
                logger.error(f"[ALI_BAILEY] {error_msg}")
                reply = Reply(ReplyType.ERROR, error_msg)
            else:
                content = reply_content.get("text", "")
                if content:
                    # 保存回复到会话
                    self.sessions.session_reply(content, session_id)
                    reply = Reply(ReplyType.TEXT, content)
                else:
                    reply = Reply(ReplyType.ERROR, "未获取到有效回复")
            
            return reply
        else:
            reply = Reply(ReplyType.ERROR, f"Bot 不支持处理{context.type}类型的消息")
            return reply

    def reply_text(self, session: AliBaileySession, retry_count=0):
        """调用阿里百炼 API 获取回复"""
        try:
            # 获取最后一条用户消息
            prompt = session.messages[-1]["content"]
            
            # 是否有会话 ID
            dashscope_session_id = session.get_dashscope_session_id()
            
            # 准备 API 调用参数
            params = {
                "api_key": self.api_key(),
                "app_id": self.app_id(),
                "prompt": prompt
            }
            
            # 如果有会话 ID，添加到参数中
            if dashscope_session_id:
                params["session_id"] = dashscope_session_id
            
            # 调用阿里百炼 API
            response = Application.call(**params)
            
            result = {
                "status_code": response.status_code,
                "request_id": getattr(response, "request_id", "")
            }
            
            if response.status_code == HTTPStatus.OK:
                # 保存会话 ID
                session.set_dashscope_session_id(response.output.session_id)
                
                result["text"] = response.output.text
                result["session_id"] = response.output.session_id
                
                if hasattr(response, "usage"):
                    result["usage"] = response.usage
            else:
                result["message"] = getattr(response, "message", "未知错误")
                
            return result
        except Exception as e:
            need_retry = retry_count < 2
            logger.exception(f"[ALI_BAILEY] Exception: {e}")
            
            if need_retry:
                logger.warn(f"[ALI_BAILEY] 第{retry_count + 1}次重试")
                time.sleep(2)
                return self.reply_text(session, retry_count + 1)
            else:
                return {
                    "status_code": 500,
                    "message": f"调用异常：{str(e)}"
                }
