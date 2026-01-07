import urllib.request
import urllib.error
import json

# 测试API地址
api_url = 'http://127.0.0.1:8000/api/appointment/1/approve/'

# 测试数据
payload = {
    "approvalInfo": {
        "appointmentNumber": "AP1234567890",
        "receptionLocation": "探访室A",
        "receptionist": "值班人员",
        "receptionistPhone": "010-12345678"
    }
}

# 转换为JSON字符串
json_data = json.dumps(payload).encode('utf-8')

# 创建请求
req = urllib.request.Request(
    api_url,
    data=json_data,
    headers={'Content-Type': 'application/json'},
    method='PUT'
)

try:
    # 发送请求
    with urllib.request.urlopen(req) as response:
        # 读取响应
        response_data = response.read().decode('utf-8')
        result = json.loads(response_data)
        print("API响应:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    print(f"HTTP错误: {e.code} - {e.read().decode('utf-8')}")
except urllib.error.URLError as e:
    print(f"URL错误: {e.reason}")
except Exception as e:
    print(f"其他错误: {str(e)}")
