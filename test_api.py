import requests
import json

# API端点
url = 'http://127.0.0.1:8000/api/appointment/1/approve/'

# 请求头
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token admin_mock_token'
}

# 请求数据
data = {
    'approval_info': {
        'appointmentNumber': 'AP123456',
        'receptionLocation': '探访室A',
        'receptionist': '值班人员',
        'receptionistPhone': '010-12345678'
    }
}

# 发送请求
response = requests.put(url, headers=headers, data=json.dumps(data))

# 输出结果
print(f'响应状态码: {response.status_code}')
print(f'响应内容: {response.text}')
