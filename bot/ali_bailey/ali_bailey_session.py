# encoding:utf-8

from bot.session_manager import Session
from common.log import logger

class AliBaileySession(Session):
    def __init__(self, session_id, system_prompt=None, model="ali_bailey"):
        super().__init__(session_id, system_prompt)
        self.model = model
        self._session_id = session_id
        self._dashscope_session_id = None  # 阿里百炼 API 返回的 session_id
        self.reset()

    def get_dashscope_session_id(self):
        return self._dashscope_session_id
    
    def set_dashscope_session_id(self, session_id):
        self._dashscope_session_id = session_id
    
    def reset(self):
        super().reset()
        self._dashscope_session_id = None
