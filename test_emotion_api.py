import requests
import json

# 测试情绪分析接口
print("="*60)
print("测试1: 分析文本情绪")
print("="*60)
response = requests.post(
    "http://localhost:8000/api/v1/emotion/analyze",
    json={
        "text": "我今天心情非常好，遇到了很多开心的事情！",
        "user_id": 1
    }
)
print(f"状态码: {response.status_code}")
result = response.json()
print(f"情绪类型: {result['emotion_type']}")
print(f"情绪分数: {result['emotion_score']}")
print(f"分析结果: {result['analysis_result']}")
print(f"建议: {result['suggestions']}")
print()

# 测试查询历史记录
print("="*60)
print("测试2: 查询历史记录（最新1条）")
print("="*60)
response = requests.get(
    "http://localhost:8000/api/v1/emotion/history/1?limit=1"
)
print(f"状态码: {response.status_code}")
history = response.json()
if history:
    record = history[0]
    print(f"记录ID: {record['id']}")
    print(f"输入文本: {record['input_text']}")
    print(f"情绪类型: {record['emotion_type']}")
    print(f"情绪分数: {record['emotion_score']}")
    print(f"分析结果: {record['analysis_result']}")
    print(f"建议: {record['suggestions']}")
    print(f"创建时间: {record['created_at']}")
print()

print("="*60)
print("测试完成！")
print("="*60)