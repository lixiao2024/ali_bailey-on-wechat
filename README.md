<div align="center">
<h1>Dify on WeChat</h1>

<div align="center">
<h1>阿里百炼 on WeChat</h1>
本项目 ali_bailey-on-wechat 为 chatgpt-on-wechat 下游分支
额外对接了阿里百炼智能体平台 Ali Bailey，支持阿里百炼智能体，并保留了原 dify-on-wechat 对 Dify 的支持。
如果我的项目对您有帮助请点一个 star 吧~
</div>
<div align="center">
<img width="700" src="./docs/images/image1.jpg">
</div>
<div align="center">
<img width="700" src="./docs/images/image2.jpg">
</div>
本项目在 dify-on-wechat 的基础上新增了对阿里百炼智能体的支持，使您可以轻松将已构建的阿里百炼智能体接入微信生态。
做本项目的初衷是想补充上游 ChatGPT on WeChat 项目未提供接入阿里百炼智能体功能，同时我也在维护的过程中学习到了很多有用的技术。
大家在使用本项目的时候一定要遵守相关法律法规，希望大家利用此项目能够增加生活的趣味性与便捷性、提高工作效率，或者提供更有价值的东西。
<details><summary><strong>免责声明【必读】</strong></summary>
本项目仅供学习和技术研究使用，不得用于任何商业或非法行为，否则后果自负。
本项目的作者不对本工具的安全性、完整性、可靠性、有效性、正确性或适用性做任何明示或暗示的保证，也不对本工具的使用或滥用造成的任何直接或间接的损失、责任、索赔、要求或诉讼承担任何责任。
本项目的作者保留随时修改、更新、删除或终止本工具的权利，无需事先通知或承担任何义务。
本项目的使用者应遵守相关法律法规，尊重微信的版权和隐私，不得侵犯微信或其他第三方的合法权益，不得从事任何违法或不道德的行为。
本项目的使用者在下载、安装、运行或使用本工具时，即表示已阅读并同意本免责声明。如有异议，请立即停止使用本工具，并删除所有相关文件。
本项目提供的微信接入方式均来自其他开源项目，仅供学习和技术研究使用。
</details>
目前已测试过的通道如下：
[x] 个人微信
[x] 企业微信应用
[x] 企业服务公众号
[x] 企业微信个人号 (仅 windows 系统)
[ ] 个人订阅公众号 待测试
[ ] 企业微信客服 待测试
[ ] 钉钉 待测试
[ ] 飞书 待测试




</div>

# 最新功能

## 1.支持阿里百炼智能体
新增对阿里百炼智能体平台的支持，可以轻松将阿里百炼智能体接入微信生态。阿里百炼智能体配置如下：
```bash
{
    "channel_type": "ali_bailey",  # 通道类型设置为ali_bailey
    "ali_bailey_app_id": "",       # 首次登录可留空,自动获取
    "ali_bailey_app_key": "",      # 首次登录可留空,自动获取
    "ali_bailey_base_url": "https://api.ali-bailey.com/",  # 阿里百炼服务API地址
}
```
原项目所有功能仍然保留，包括 gewechat 登录、用户信息对接、企业微信个人号支持、JinaSum 插件、Dify 工作流等。
快速开始
准备
1. 账号注册
进入阿里百炼官网注册账号，创建一个智能体并发布，然后获取 API 密钥和应用 ID。
2.运行环境
支持 Linux、MacOS、Windows 系统（可在 Linux 服务器上长期运行)，同时需安装 Python。
python 推荐 3.8 以上版本，已在 ubuntu 测试过 3.11.6 版本可以成功运行。
3. 安装依赖
```bash
pip install -r requirements.txt
```
致谢
本项目基于 dify-on-wechat 和 chatgpt-on-wechat 开发，特此感谢。


## 2. 支持 gewechat 登录微信

基于[Gewechat](https://github.com/Devo919/Gewechat)项目实现的微信个人号通道，使用 ipad 协议登录，相比 itchat 协议更稳定。

> 1. gewechat 要求必须搭建服务到**同省服务器**或者电脑里方可正常使用
> 2. 此项目仅用于个人娱乐场景，请勿用于任何商业场景
>
> ⚠️注意目前 channel_type: "wx" 对应的 itchat 无法使用，请更换为 gewechat

dify-on-wechat、dify、gewechat 服务的调用关系

<div align="center">
<img width="700" src="./docs/gewechat/gewechat_service_design.png">
</div>

### 快速启动 gewechat 机器人

#### 部署 gewechat 服务

```bash
# 从阿里云镜像仓库拉取(国内)
docker pull registry.cn-chengdu.aliyuncs.com/tu1h/wechotd:alpine
docker tag registry.cn-chengdu.aliyuncs.com/tu1h/wechotd:alpine gewe

# 创建数据目录并启动服务
mkdir -p gewechat/data  
docker run -itd -v ./gewechat/data:/root/temp -p 2531:2531 -p 2532:2532 --restart=always --name=gewe gewe
```

#### 配置 dify-on-wechat

gewechat 相关配置如下，注意**channel_type 设置为 gewechat**

```bash 
{
    "channel_type": "gewechat",  # 通道类型设置为gewechat    
    "gewechat_token": "",        # 首次登录可留空,自动获取
    "gewechat_app_id": "",       # 首次登录可留空,自动获取
    "gewechat_base_url": "http://本机ip:2531/v2/api",  # gewechat服务API地址
    "gewechat_callback_url": "http://本机ip:9919/v2/api/callback/collect", # 回调地址
    "gewechat_download_url": "http://本机ip:2532/download" # 文件下载地址
}
```

> 本机 ip 是指**局域网 ip**或**公网 ip**，可通过`ipconfig`或`ifconfig`命令查看
> 
> 对与 gewechat_callback_url，ip 不能填`127.0.0.1`或`localhost`，否则会报错
> 
> `9919`端口是 dify-on-wechat 服务监听的端口，如果是用 docker 启动的 dify-on-wechat 服务，请把`9919`端口映射到宿主机

**请务必查看详细配置**： [gewechat 接入文档](./docs/gewechat/README.md)

#### 启动机器人

```bash
python app.py
```
启动成功后，可以看到如下日志信息，注意 token 和 appid 会**自动保存**到 config.json，无需手动保存

<div align="center">
<img width="700" src="./docs/gewechat/gewechat_login.jpg">
</div>
⚠️如果遇到 gewechat 创建设备失败，unexpected EOF 错误，请排查网络是否是以下情况：

1️⃣代理：请关闭代理后尝试；

2️⃣国外服务器；

3️⃣回调地址为外网；

4️⃣异地服务器

## 2. 用户信息对接 dify

新增用户信息对接 dify 的能力，会把用户 id、用户名称、群聊 id、群聊名称信息传递给 dify，搭配 gewechat_channel 提供的 wxid 与 chatroomid，
可以在 dify 中识别出每个用户，实现个性化服务。详细教程请查看：[用户信息对接 dify](./docs/user-info/README.md)

<div align="center">
<img width="700" src="./docs/user-info/user-info-room.jpg">
</div>

## 3. 支持企业微信个人号（仅支持 windows 系统）
<div align="center">
<img width="700" src="./docs/images/wework.jpg">
</div>

> 1. 有**封号风险**，请使用企业微信**小号**测试
> 2. 在登录旧版本的企业微信时可能会出现企业微信版本过低，无法登录情况，参考[issue1525](https://github.com/zhayujie/chatgpt-on-wechat/issues/1525)，请尝试更换其他企业微信号重试

### 快速启动企业微信个人号机器人

#### 安装指定版本企业微信

[WeCom_4.0.8.6027.exe 官方下载链接](https://dldir1.qq.com/wework/work_weixin/WeCom_4.0.8.6027.exe)

[WeCom_4.0.8.6027.exe 阿里云盘备份](https://www.alipan.com/s/UxQHrZ5WoxS)

[WeCom_4.0.8.6027.exe 夸克网盘备份](https://pan.quark.cn/s/1d06b91b40af)

#### 下载项目安装依赖

参考[**手摸手教你把 Dify 接入微信生态**](https://docs.dify.ai/v/zh-hans/learn-more/use-cases/dify-on-wechat)，下载本项目，安装 python 依赖

#### 安装 ntwork 依赖

由于 ntwork 的安装源不是很稳定，可以下载对应的 whl 文件，使用 whl 文件离线安装 ntwork

首先需要查看你的 python 版本，在命令行中输入 python 查看版本信息，然后在[ntwork-whl](https://github.com/hanfangyuan4396/ntwork-bin-backup/tree/main/ntwork-whl)目录下找到对应的 whl 文件，运行`pip install xx.whl`安装 ntwork 依赖，注意"xx.whl"更换为 whl 文件的**实际路径**。

例如我的 python 版本信息为

"Python 3.8.5 (default, Sep  3 2020, 21:29:08) [MSC v.1916 64 bit (AMD64)]"

可以看到 python 版本是**3.8.5**，并且是**AMD64**，所以对应的 whl 文件为**ntwork-0.1.3-cp38-cp38-win_amd64.whl**，需要执行如下命令安装
```sh
pip install your-path/ntwork-0.1.3-cp38-cp38-win_amd64.whl
```

#### 填写配置文件

我们在项目根目录创建名为 config.json 的文件，文件内容如下，请根据教程参考[**手摸手教你把 Dify 接入微信生态**](https://docs.dify.ai/v/zh-hans/learn-more/use-cases/dify-on-wechat)获取 dify_api_base、dify_api_key、dify_app_type 信息，注意 channel_type 填写为 **wework**

```json
{ 
  "dify_api_base": "https://api.dify.ai/v1",
  "dify_api_key": "app-xxx",
  "dify_app_type": "chatbot",
  "channel_type": "wework",
  "model": "dify",
  "single_chat_prefix": [""],
  "single_chat_reply_prefix": "",
  "group_chat_prefix": ["@bot"],
  "group_name_white_list": ["ALL_GROUP"]
}
```

#### 登录企业微信

务必提前在电脑扫码登录企业微信

#### 启动机器人

运行如下命令启动机器人
```sh
python app.py
```
我们可以看到终端输出如下信息，等待 wework 程序初始化完成，最后启动成功~
```
[INFO][2024-04-30 21:16:04][wework_channel.py:185] - 等待登录······
[INFO][2024-04-30 21:16:05][wework_channel.py:190] - 登录信息:>>>user_id:xxx>>>>>>>>name:
[INFO][2024-04-30 21:16:05][wework_channel.py:191] - 静默延迟60s，等待客户端刷新数据，请勿进行任何操作······
[INFO][2024-04-30 21:17:05][wework_channel.py:224] - wework程序初始化完成········
```

## 4. 集成[JinaSum](https://github.com/hanfangyuan4396/jina_sum)插件
使用 Jina Reader 和 ChatGPT 支持总结公众号、小红书、知乎等分享卡片链接，配置详情请查看[JinaSum](https://github.com/hanfangyuan4396/jina_sum)

<div align="center">
<img width="700" src="./plugins/jina_sum/docs/images/wechat_mp.jpg">
</div>

<div align="center">
<img width="700" src="./plugins/jina_sum/docs/images/red.jpg">
</div>

## 5. 新增[CustomDifyApp](https://github.com/hanfangyuan4396/dify-on-wechat/tree/master/plugins/custom_dify_app)插件
支持根据群聊名称关键词自动切换不同的 Dify 应用，也支持为单聊配置专门的 Dify 应用。

例如，在与 AI 助手进行私聊时，自动调用企业内部员工助手 Dify 应用；在 xx 平台技术支持群中@AI 助手时，则自动切换至该平台的技术支持 Dify 应用。

配置详情请查看 [CustomDifyApp](https://github.com/hanfangyuan4396/dify-on-wechat/tree/master/plugins/custom_dify_app)

## 6. 支持 Dify Chatflow & Workflow
dify 官网已正式上线工作流模式，可以导入本项目下的[dsl 文件](./dsl/chat-workflow.yml)快速创建工作流进行测试。工作流输入变量名称十分灵活，对于**工作流类型**的应用，本项目**约定工作流的输入变量命名为`query`**，**输出变量命名为`text`**。

(ps: 感觉工作流类型应用不太适合作为聊天机器人，现在它还没有会话的概念，需要自己管理上下文。但是它可以调用各种工具，通过 http 请求和外界交互，适合执行业务逻辑复杂的任务；它可以导入导出工作流 dsl 文件，方便分享移植。也许以后 dsl 文件 + 配置文件就可以作为本项目的一个插件。)
## 7. 支持 COZE API

<div align="center">
<img width="700" src="./docs/images/image5.jpg">
</div>

<div align="center">
<img width="700" src="./docs/images/image6.jpg">
</div>

### 如何快速启动 coze 微信机器人

- 请参照**快速开始**步骤克隆源码并安装依赖

- 按照下方 coze api config.json 示例文件进行配置
以下是对默认配置的说明，可根据需要进行自定义修改（**如果复制下方的示例内容，请去掉注释**）
```bash
# coze config.json文件内容示例
{
  "coze_api_base": "https://api.coze.cn",     # coze base url
  "coze_api_key": "xxx",                      # coze api key
  "coze_bot_id": "xxx",                       # 根据url获取coze_bot_id https://www.coze.cn/space/{space_id}/bot/{bot_id}
  "channel_type": "gewechat",                 # 通道类型，当前为个人微信
  "model": "coze",                            # 模型名称，当前对应coze平台
  "single_chat_prefix": [""],                 # 私聊时文本需要包含该前缀才能触发机器人回复
  "single_chat_reply_prefix": "",             # 私聊时自动回复的前缀，用于区分真人
  "group_chat_prefix": ["@bot"],              # 群聊时包含该前缀则会触发机器人回复
  "group_name_white_list": ["ALL_GROUP"]      # 机器人回复的群名称列表
}
```

上述示例文件是个人微信对接 coze 的极简配置，详细配置说明需要查看 config.py，注意**不要修改 config.py 中的值**，config.py 只是校验是否是有效的 key，最终**生效的配置请在 config.json 修改**。

- 启动程序

```
python3 app.py                                    # windows环境下该命令通常为 python app.py
```



特别感谢 [**@绛烨**](https://github.com/jiangye520) 提供内测 coze api key

## 8. 支持 dify voice

dify 语音相关配置如下，另外需要在 dify 应用中开启语音转文字以及文字转语音功能，注意语音功能需要**安装 ffmpeg 依赖**

```bash
{
  "dify_api_base": "https://api.dify.ai/v1",
  "dify_api_key": "app-xxx",
  "dify_app_type": "chatbot",
  "speech_recognition": true,  # 是否开启语音识别
  "voice_reply_voice": true,   # 是否使用语音回复语音
  "always_reply_voice": false, # 是否一直使用语音回复
  "voice_to_text": "dify",     # 语音识别引擎
  "text_to_voice": "dify"      # 语音合成引擎
}
```

> ⚠️注意：dify 应用中开启语音转文字以及文字转语音功能，不是在工具中添加 Audio（tts/asr），以 0.15.1 版本为例，**具体路径是：你的 dify 应用 - 编排 - 调试与预览 - 开启功能增强 webapp 用户体验（底部）- 开启语音转文字 - 开启文字转语音 - 发布后生效**。老版本 dify 与新版不同，不在调试与预览中，而是左边编排工具下面。详细开启方法可查看 issue [#211](https://github.com/hanfangyuan4396/dify-on-wechat/issues/211)

搭配 gewechat_channel 可以实现发送语音条功能，gewechat 服务只能获取到**20s**以内的语音，所以**你只能给 bot 发送 20s 以内的语音**，但**bot 给你发送语音时无此限制**。[**请查看 gewechat 接入文档**](./docs/gewechat/README.md)

<div align="center">
<img width="700" src="./docs/gewechat/gewechat_voice.jpg">
</div>


## 9. 支持 dify 图片识别

dify 图片识别配置如下，另外需要在 dify 应用中开启图片上传与图片理解功能。使用方法为，**先发送图片**，然后**在 3 分钟内发送关于图片的问题**，注意先后顺序。

```bash
{
  "dify_api_base": "https://api.dify.ai/v1",
  "dify_api_key": "app-xxx",
  "dify_app_type": "chatbot",
  "image_recognition": true
}
```

## 10. 支持 deepseek

deepseek 和 openai 可以共用一套 api lib，，默认 model 是`deepseek-chat`
```json
{
  "model": "deepseek-chat",  // 或其他 Deepseek 模型，如"deepseek-chat-v2"
  "open_ai_api_key": "您的 Deepseek API 密钥",
  "open_ai_api_base": "https://api.deepseek.com/v1"
}
```
## 11. web ui 优化

webui 启动方式
- 源码：python web_ui.py
- docker: 设置环境变量 DIFY_ON_WECHAT_EXEC: 'python web_ui.py'
- 访问 http://服务器ip:7860，输入默认账号密码 dow/dify-on-wechat

可以通过 web ui 登录退出 gewechat 微信，查看状态，重启服务

详情请查看文档 [gradio web ui](./docs/webui/README.md)

![image](https://github.com/user-attachments/assets/6735e4e4-bc6d-4b8a-9854-a3dcf877e3eb)

## 12. 同步上游 wcf 通道

需要 Windows 环境，接入详情请查看 [chatgpt-on-wechat#2562](https://github.com/zhayujie/chatgpt-on-wechat/pull/2562)

# 更新日志
- 2025/04/12 修复 jina_sum 插件无法总结微信链接，感谢 [sofs2005](https://github.com/sofs2005/jina_sum) 的代码；同步上游最新功能，支持 [wcf](https://github.com/lich0821/WeChatFerry) 微信通道
- 2025/01/24 优化 web ui，可以通过 web ui 登录退出 gewechat 微信
- 2025/01/06 修复在微信群中微信账号无法识别命令的 bug，感谢[**sofs2005**](https://github.com/sofs2005)贡献的代码
- 2025/01/04 修复 gewechat 自动回复公众号等官方账号消息的 bug，感谢[**benxiaohai86**](https://github.com/benxiaohai86)提供的过滤思路
- 2024/12/29 支持 gewechat 发送语音条消息
- 2024/12/28 支持 gewechat 总结分享的公众号文章与图片识别
- 2024/12/14 支持用户信息对接 dify
- 2024/12/04 新增 [gewechat](https://github.com/Devo919/Gewechat) 通道，相比 itchat 更稳定。
- 2024/10/01 新增插件 CustomDifyApp 与 GroupAtAutoreply，CustomDifyApp 支持根据群聊名称关键词自动切换不同的 Dify 应用，GroupAtAutoreply 支持群聊艾特自动回复，贡献者[**blankbro**](https://github.com/blankbro)
- 2024/09/18 支持 dify voice
- 2024/08/09 dify chatbot 类型应用支持解析 markdown 格式响应，分别发送文本、图片和文件
- 2024/08/04 支持 dify 图片识别功能
- 2024/08/03 微信支持通过 web ui 扫码登录或异常重启，已适配 docker 容器
- 2024/08/01 同步上游 chatgpt on wechat 最新功能，docker 镜像地址支持阿里云容器仓库 ACR
- 2024/04/30 支持 windows 环境下企业微信个人号
- 2024/04/24 集成 JinaSum 插件，修复总结微信公众号文章，修复 dify usage key error, 修复 dify 私有部署的图片 url 错误
- 2024/04/16 支持基本的企业微信客服通道，感谢[**@lei195827**](https://github.com/lei195827), [**@sisuad**](https://github.com/sisuad) 的贡献
- 2024/04/14 Suno 音乐插件，Dify on WeChat 对接详细教程，config 文件 bug 修复
- 2024/04/08 支持聊天助手类型应用内置的 Chatflow，支持 dify 基础的对话 Workflow
- 2024/04/04 支持 docker 部署
- 2024/03/31 支持 coze api(内测版)
- 2024/03/29 支持 dify 基础的对话工作流，由于 dify 官网还未上线工作流，需要自行部署测试 [0.6.0-preview-workflow.1](https://github.com/langgenius/dify/releases/tag/0.6.0-preview-workflow.1)。

# 快速开始

接入非 Dify 机器人可参考原项目文档 [chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat)、[项目搭建文档](https://docs.link-ai.tech/cow/quick-start)

Dify 接入微信生态的**详细教程**请查看文章 [**手摸手教你把 Dify 接入微信生态**](https://docs.dify.ai/v/zh-hans/learn-more/use-cases/dify-on-wechat)

下文介绍如何快速接入 Dify

## 准备

### 1. 账号注册

进入[Dify App](https://cloud.dify.ai) 官网注册账号，创建一个应用并发布，然后在概览页面创建保存 api 密钥，同时记录 api url，一般为 https://api.dify.ai/v1

### 2.运行环境

支持 Linux、MacOS、Windows 系统（可在 Linux 服务器上长期运行)，同时需安装 `Python`。

python 推荐 3.8 以上版本，已在 ubuntu 测试过 3.11.6 版本可以成功运行。

**(1) 克隆项目代码：**

```bash
git clone https://github.com/hanfangyuan4396/dify-on-wechat
cd dify-on-wechat/
```

**(2) 安装核心依赖 (必选)：**
> 能够使用`itchat`创建机器人，并具有文字交流功能所需的最小依赖集合。
```bash
pip3 install -r requirements.txt  # 国内可以在该命令末尾添加 "-i https://mirrors.aliyun.com/pypi/simple" 参数，使用阿里云镜像源安装依赖
```

**(3) 拓展依赖 (可选，建议安装)：**

```bash
pip3 install -r requirements-optional.txt # 国内可以在该命令末尾添加 "-i https://mirrors.aliyun.com/pypi/simple" 参数，使用阿里云镜像源安装依赖
```
> 如果某项依赖安装失败可注释掉对应的行再继续

## 配置

配置文件的模板在根目录的`config-template.json`中，需复制该模板创建最终生效的 `config.json` 文件：

```bash
  cp config-template.json config.json
```

然后在`config.json`中填入配置，以下是对默认配置的说明，可根据需要进行自定义修改（如果复制下方的示例内容，请**去掉注释**, 务必保证正确配置**dify_app_type**）：

```bash
# dify config.json文件内容示例
{ 
  "dify_api_base": "https://api.dify.ai/v1",    # dify base url
  "dify_api_key": "app-xxx",                    # dify api key
  "dify_app_type": "chatbot",                   # dify应用类型 chatbot(对应聊天助手)/agent(对应Agent)/workflow(对应工作流)，默认为chatbot
  "dify_convsersation_max_messages": 5,         # dify目前不支持设置历史消息长度，暂时使用超过最大消息数清空会话的策略，缺点是没有滑动窗口，会突然丢失历史消息，当设置的值小于等于0，则不限制历史消息长度
  "channel_type": "wx",                         # 通道类型，当前为个人微信
  "model": "dify",                              # 模型名称，当前对应dify平台
  "single_chat_prefix": [""],                   # 私聊时文本需要包含该前缀才能触发机器人回复
  "single_chat_reply_prefix": "",               # 私聊时自动回复的前缀，用于区分真人
  "group_chat_prefix": ["@bot"],                # 群聊时包含该前缀则会触发机器人回复
  "group_name_white_list": ["ALL_GROUP"],       # 机器人回复的群名称列表
  "image_recognition": true,                    # 是否开启图片理解功能，需保证对应的dify应用已开启视觉功能
  "speech_recognition": true,                   # 是否开启语音识别
  "voice_reply_voice": true,                    # 是否使用语音回复语音
  "always_reply_voice": false,                  # 是否一直使用语音回复
  "voice_to_text": "dify",                      # 语音识别引擎
  "text_to_voice": "dify"                       # 语音合成引擎
}
```

上述示例文件是个人微信对接 dify 的极简配置，详细配置说明需要查看 config.py，注意**不要修改 config.py 中的值**，config.py 只是校验是否是有效的 key，最终**生效的配置请在 config.json 修改**。

## 运行

### 1.本地运行

如果是开发机 **本地运行**，直接在项目根目录下执行：

```bash
python3 app.py                                    # windows环境下该命令通常为 python app.py
```

终端输出二维码后，使用微信进行扫码，当输出 "Start auto replying" 时表示自动回复程序已经成功运行了（注意：用于登录的微信需要在支付处已完成实名认证）。扫码登录后你的账号就成为机器人了，可以在微信手机端通过配置的关键词触发自动回复 (任意好友发送消息给你，或是自己发消息给好友)，参考[#142](https://github.com/zhayujie/chatgpt-on-wechat/issues/142)。

### 2.服务器部署

使用 nohup 命令在后台运行程序：

```bash
nohup python3 app.py & tail -f nohup.out          # 在后台运行程序并通过日志输出二维码
```
扫码登录后程序即可运行于服务器后台，此时可通过 `ctrl+c` 关闭日志，不会影响后台程序的运行。使用 `ps -ef | grep app.py | grep -v grep` 命令可查看运行于后台的进程，如果想要重新启动程序可以先 `kill` 掉对应的进程。日志关闭后如果想要再次打开只需输入 `tail -f nohup.out`。此外，`scripts` 目录下有一键运行、关闭程序的脚本供使用。

> **多账号支持：** 将项目复制多份，分别启动程序，用不同账号扫码登录即可实现同时运行。

> **特殊指令：** 用户向机器人发送 **#reset** 即可清空该用户的上下文记忆。

### 3.Docker 部署

⚠️使用`docker`或者`docker-compose`部署时，**必须先拉取最新源码**，否则会报错⚠️

```bash
cd dify-on-wechat/docker       # 进入docker目录
cp ../config-template.json ../config.json
docker compose up -d           # 启动docker容器
docker logs -f dify-on-wechat  # 查看二维码并登录
```

# Contributors
<a href="https://github.com/hanfangyuan4396/dify-on-wechat/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=hanfangyuan4396/dify-on-wechat" />
</a>



也请各位大佬多多提 PR，我社畜打工人，精力实在有限~

# 致谢

感谢所有打赏的朋友。

感谢 **NLP 工程化** 知识星球对本项目的支持

<img width="240" src="./docs/images/NLP 工程化.png">
(提供 Dify 源码剖析及答疑，Dify 对话系统源码等)

