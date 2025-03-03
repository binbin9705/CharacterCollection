import base64
import json


def decode_jwt(jwt_token):
    # 分割JWT，获取头部、负载和签名
    header, payload, signature = jwt_token.split('.')

    # Base64URL解码头部和负载
    decoded_header = base64.urlsafe_b64decode(header + '==').decode('utf-8')
    decoded_payload = base64.urlsafe_b64decode(payload + '==').decode('utf-8')

    # 解码后的头部和负载是JSON格式，转换为Python字典
    header_data = json.loads(decoded_header)
    payload_data = json.loads(decoded_payload)

    return header_data, payload_data


# 要解码的JWT字符串
jwt_token = 'eyJhbGciOiJIUzI1NiJ9.eyJyb2xlQ29kZSI6IjE5MmViZWM4NGQ0NmY0MzMxMWY4YzJmYjU5NmVmOTVjIiwibmFtZSI6Imh1YmluYmluIiwiY25hbWUiOiLog6HlvazlvawiLCJ0aW1lIjoiMjAyNC0wNS0yNyAwOTo0Mzo1MyIsInVzZXJJZCI6MzUsInV1aWQiOiJhM2ExZjAzZjE5Yzc0NjdjOGQ0NTNhNWRmNDQwYTY1MyIsImlhdCI6MTcxNjc3NDIzM30.zlJ2PBN0rUWWayZdlcqgpMeAYqT498Nt3RQfjj46r2g'

# 解码JWT
header, payload = decode_jwt(jwt_token)

# 打印解码后的负载信息
print("Decoded payload:", payload)