# 微信通知接口使用文档

本文档介绍如何使用微信通知接口，让外部应用能够通过我们的服务向微信用户发送消息通知。

## 功能概述

通知接口允许外部应用通过 API 调用向特定微信用户发送文本消息。此功能适用于以下场景：

- 系统任务完成通知
- 异常事件告警
- 定时提醒
- 工作流状态更新
- 其他需要实时通知用户的场景

## 接口说明

### 通知消息接口

**接口地址**：`/api/notify`

**请求方式**：POST

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|-------|-----|-----|------|
| wxid | string | 是 | 接收者的微信 ID |
| content | string | 是 | 要发送的消息内容 |

**请求示例**：

```json
{
  "wxid": "wxid_xxxxxxxx",
  "content": "您的任务已完成！"
}
```

**响应参数**：

| 参数名 | 类型 | 说明 |
|-------|-----|------|
| success | boolean | 操作是否成功 |
| message | string | 操作结果说明 |
| data | object | 成功时返回的数据 |

**响应示例（成功）**：

```json
{
  "success": true,
  "message": "消息发送成功",
  "data": {
    "newMsgId": "7265188027048533884",
    "msgId": 1883401595
  }
}
```

**响应示例（失败）**：

```json
{
  "success": false,
  "message": "发送消息失败：用户未登录"
}
```

### 健康检查接口

**接口地址**：`/health`

**请求方式**：GET

**响应示例（成功）**：

```json
{
  "status": "ok",
  "message": "服务正常运行中"
}
```

**响应示例（失败）**：

```json
{
  "status": "error",
  "message": "用户未登录"
}
```

## 使用步骤

### 1. 启动通知 API 服务

```bash
# 启动通知API服务（默认监听8080端口）
python api_server.py

# 指定其他端口
PORT=9000 python api_server.py
```

### 2. 验证服务是否正常

```bash
# 检查服务健康状态
curl http://localhost:8080/health
```

### 3. 发送测试消息

您可以使用提供的模拟工具进行测试：

```bash
# 使用模拟任务模式测试
python mock_external_app.py --wxid wxid_xxxxxxxx --task "数据分析"

# 直接发送指定消息
python mock_external_app.py --wxid wxid_xxxxxxxx --message "这是一条测试消息"

# 指定接口URL（如果不是默认值）
python mock_external_app.py --url http://localhost:9000/api/notify --wxid wxid_xxxxxxxx
```

### 4. 实际应用集成

在您的应用中添加 API 调用代码。以下是使用 Python 的示例：

```python
import requests
import json

def send_notification(wxid, content):
    api_url = "http://localhost:8080/api/notify"
    headers = {"Content-Type": "application/json"}
    payload = {
        "wxid": wxid,
        "content": content
    }
    
    response = requests.post(
        api_url,
        data=json.dumps(payload),
        headers=headers
    )
    
    return response.json()

# 使用示例
result = send_notification("wxid_xxxxxxxx", "任务已完成！")
print(result)
```

## 注意事项

1. **安全性**：在生产环境中，建议添加 API 身份验证机制，以防止未授权调用。
2. **稳定性**：确保 gewechat 服务正常登录和运行，否则消息无法发送。
3. **内容规范**：消息内容须符合微信的规范，避免发送敏感信息或营销广告内容。
4. **高可用性**：考虑使用负载均衡和错误重试机制，以提高服务可靠性。
5. **频率限制**：避免短时间内发送大量消息，以防被微信限制。

## 常见问题

### Q: 发送消息失败，提示"用户未登录"怎么办？
A: 请确保 gewechat 服务已正常登录，可以通过 web_ui.py 查看登录状态。

### Q: 如何获取接收者的 wxid？
A: wxid 可以在添加好友后通过 gewechat API 获取，或在 web 界面中查看联系人列表。

### Q: 发送消息有数量限制吗？
A: 建议控制单个用户每分钟的消息数量，避免频繁发送导致微信限制。 