"""
channel factory
"""
from common import const


def create_bot(bot_type):
    """
    create a bot_type instance
    :param bot_type: bot type code
    :return: bot instance
    """
    if bot_type == const.BAIDU:
        # 替换 Baidu Unit 为 Baidu 文心千帆对话接口
        # from bot.baidu.baidu_unit_bot import BaiduUnitBot
        # return BaiduUnitBot()
        from bot.baidu.baidu_wenxin import BaiduWenxinBot
        return BaiduWenxinBot()

    elif bot_type == const.CHATGPT:
        # ChatGPT 网页端 web 接口
        from bot.chatgpt.chat_gpt_bot import ChatGPTBot
        return ChatGPTBot()

    elif bot_type == const.OPEN_AI:
        # OpenAI 官方对话模型 API
        from bot.openai.open_ai_bot import OpenAIBot
        return OpenAIBot()

    elif bot_type == const.CHATGPTONAZURE:
        # Azure chatgpt service https://azure.microsoft.com/en-in/products/cognitive-services/openai-service/
        from bot.chatgpt.chat_gpt_bot import AzureChatGPTBot
        return AzureChatGPTBot()

    elif bot_type == const.XUNFEI:
        from bot.xunfei.xunfei_spark_bot import XunFeiBot
        return XunFeiBot()

    elif bot_type == const.LINKAI:
        from bot.linkai.link_ai_bot import LinkAIBot
        return LinkAIBot()

    elif bot_type == const.CLAUDEAI:
        from bot.claude.claude_ai_bot import ClaudeAIBot
        return ClaudeAIBot()
    elif bot_type == const.CLAUDEAPI:
        from bot.claudeapi.claude_api_bot import ClaudeAPIBot
        return ClaudeAPIBot()
    elif bot_type == const.QWEN:
        from bot.ali.ali_qwen_bot import AliQwenBot
        return AliQwenBot()
    elif bot_type == const.QWEN_DASHSCOPE:
        from bot.dashscope.dashscope_bot import DashscopeBot
        return DashscopeBot()
    elif bot_type == const.GEMINI:
        from bot.gemini.google_gemini_bot import GoogleGeminiBot
        return GoogleGeminiBot()

    elif bot_type == const.DIFY:
        from bot.dify.dify_bot import DifyBot
        return DifyBot()

    elif bot_type == const.ZHIPU_AI:
        from bot.zhipuai.zhipuai_bot import ZHIPUAIBot
        return ZHIPUAIBot()

    elif bot_type == const.COZE:
        from bot.bytedance.bytedance_coze_bot import ByteDanceCozeBot
        return ByteDanceCozeBot()

    elif bot_type == const.MOONSHOT:
        from bot.moonshot.moonshot_bot import MoonshotBot
        return MoonshotBot()
    
    elif bot_type == const.MiniMax:
        from bot.minimax.minimax_bot import MinimaxBot
        return MinimaxBot()
        
    elif bot_type == const.DEEPSEEK:
        from bot.deepseek.deepseek_bot import DeepseekBot
        return DeepseekBot()

    elif bot_type == const.MODELSCOPE:
        from bot.modelscope.modelscope_bot import ModelScopeBot
        return ModelScopeBot()

    elif bot_type == const.ALI_BAILEY:
        from bot.ali_bailey.ali_bailey_bot import AliBaileyBot
        return AliBaileyBot()

    raise RuntimeError
