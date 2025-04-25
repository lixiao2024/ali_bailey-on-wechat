import json
import web
from common.log import logger
from channel.chat_message import ChatMessage
from bridge.context import Context, ContextType
from channel.chat_channel import ChatChannel
from common.singleton import singleton
from config import conf

class NurseAssistantMessage(ChatMessage):
    def __init__(
        self,
        msg_id,
        content,
        ctype=ContextType.TEXT,
        from_user_id="NurseAssistant",
        to_user_id="",  # 这将是wxid
        other_user_id="NurseAssistant",
    ):
        self.msg_id = msg_id
        self.ctype = ctype
        self.content = content
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.other_user_id = other_user_id

@singleton
class NurseAssistantChannel(ChatChannel):
    def __init__(self):
        super().__init__()
        self.handlers = {}
        
    def register_handler(self, wxid, handler):
        """注册一个消息处理器对应特定wxid"""
        self.handlers[wxid] = handler
        
    def receive_message(self):
        """接收护理助手app发送的消息"""
        try:
            data = web.data()
            json_data = json.loads(data)
            
            wxid = json_data.get('wxid')
            content = json_data.get('content')
            
            if not wxid or not content:
                return json.dumps({
                    "status": "error", 
                    "message": "Missing required fields (wxid or content)"
                })
                
            logger.info(f"收到护理助手消息: wxid={wxid}, content={content}")
            
            # 如果有对应的处理器，将消息转发给它
            if wxid in self.handlers:
                self.handlers[wxid](content)
                
            # 如果我们想要通过现有的聊天渠道进行处理
            self._process_through_channel(wxid, content)
                
            return json.dumps({"status": "success", "message": "Message processed successfully"})
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return json.dumps({"status": "error", "message": "Invalid JSON format"})
        except Exception as e:
            logger.error(f"Error processing nurse assistant message: {e}")
            return json.dumps({"status": "error", "message": str(e)})
    
    def _process_through_channel(self, wxid, content):
        """通过现有的聊天渠道处理消息"""
        try:
            # 创建上下文对象
            msg_id = f"nurse_{int(web.ctx.env.get('REQUEST_TIME', 0))}"
            msg = NurseAssistantMessage(msg_id, content, to_user_id=wxid)
            context = self._compose_context(ContextType.TEXT, content, msg)
            context["receiver"] = wxid  # 设置接收者ID为wxid
            context["isgroup"] = False
            
            # 使用现有的处理管道处理消息
            self.produce(context)
        except Exception as e:
            logger.error(f"Error forwarding message through channel: {e}")

    def startup(self):
        """启动护理助手消息接收服务"""
        logger.info("启动护理助手消息接收服务...")
        
        # 注册URL路由
        urls = (
            '/api/nurse-assistant/message', 'NurseAssistantMessageHandler',
        )
        
        # 获取配置的端口，默认为9898
        port = conf().get("nurse_assistant_port", 9898)
        
        # 启动Web服务
        app = web.application(urls, globals(), autoreload=False)
        
        try:
            web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))
            logger.info(f"护理助手消息接收服务已启动，监听端口: {port}")
        except Exception as e:
            logger.error(f"启动护理助手消息接收服务失败: {e}")

class NurseAssistantMessageHandler:
    def POST(self):
        return NurseAssistantChannel().receive_message() 