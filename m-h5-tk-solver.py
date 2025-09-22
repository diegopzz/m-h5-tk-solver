import hashlib
import time
import requests
from urllib.parse import urlparse

class RequestData:
    token = ""
    timestamp = ""
    full_token = ""
    token_enc = ""

def compute_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    hash_bytes = md5_hash.digest()

    hex_string = ''.join(f'{b:02X}' for b in hash_bytes)
    return hex_string.lower()

def do_request():
    try:
        time.sleep(1)

        proxies = {
            'http': '',
            'https': ''
        }

        session = requests.Session()
        session.proxies.update(proxies)

        url = "https://acs-m.miravia.es/h5/mtop.relationrecommend.lazadarecommend.recommend/1.0/"

        headers = {
            'Host': 'acs-m.miravia.es'
        }

        response = session.get(url, headers=headers)

        if response.status_code == 200:
            extract_cookies(session, url)
            print("Cookies extracted successfully")
        else:
            print(f"Failed: {response.status_code}")

    except Exception as ex:
        print(f"Error in do_request: {ex}")

def extract_cookies(session, url):
    try:
        parsed_url = urlparse(url)

        for cookie in session.cookies:
            if cookie.name == "_m_h5_tk":
                RequestData.full_token = cookie.value
                values = cookie.value.split('_')
                if len(values) >= 2:
                    RequestData.token = values[0]
                    RequestData.timestamp = values[1]
            elif cookie.name == "_m_h5_tk_enc":
                RequestData.token_enc = cookie.value

        print(f"Extracted tokens:")
        print(f"  full_token: {RequestData.full_token}")
        print(f"  token: {RequestData.token}")
        print(f"  timestamp: {RequestData.timestamp}")
        print(f"  token_enc: {RequestData.token_enc}")

    except Exception as ex:
        print(f"Error extracting cookies: {ex}")

def generate_signature_data(page_number=1):
    request_data = {
        "Api": "mtop.relationrecommend.LazadaRecommend.recommend",
        "V": "1.0",
        "Ecode": 0,
        "Type": "get",
        "IsSec": 1,
        "AntiCreep": True,
        "Timeout": 10000,
        "NeedLogin": False,
        "AppKey": "24677475",
        "DataType": "json",
        "SessionOption": "AutoLoginOnly",
        "Xi18nLanguage": "es-ES",
        "Xi18nRegionID": "ES",
        "Entrance": "",
        "IsIcmsMtop": True,
        "Data": '{"appId":"32771","params":"{\\"regionId\\":\\"es\\",\\"language\\":\\"es\\",\\"appVersion\\":\\"\\",\\"platform\\":\\"pc\\",\\"_input_charset\\":\\"UTF-8\\",\\"_output_charset\\":\\"UTF-8\\",\\"anonymousId\\":\\"5fUxHLhsdsdasdsdasdxRDcCAWgcxaHtpBF+\\",\\"type\\":\\"campaignModule\\",\\"backupParams\\":\\"regionId,language,type,timeslotId,pageNo,themeId,sellerId,categoryId\\",\\"pageNo\\":' + str(page_number) + '}"}"'
    }

    print(f"Key {RequestData.token}")

    i = int(time.time() * 1000)

    concatenated_string = f"{RequestData.token}&{i}&{request_data['AppKey']}&{request_data['Data']}"

    j = compute_md5(concatenated_string)
    print(f"Sign: {j}")
    print(f"Timestamp: {RequestData.timestamp}")
    print(f"Sign timestamp: {i}")
    print(f"Key: {RequestData.token}")
    print(f"_m_h5_tk: {RequestData.full_token}")
    print(f"_m_h5_enc: {RequestData.token_enc}")

    return {
        'sign': j,
        'timestamp': i,
        'token': RequestData.token,
        'full_token': RequestData.full_token,
        'token_enc': RequestData.token_enc,
        'concatenated_string': concatenated_string
    }

def main():
    print("Starting automatic token extraction...")

    do_request()

    if not RequestData.token or not RequestData.full_token:
        print("Error: Could not extract required tokens from cookies")
        return

    print("\nGenerating signature data...")
    result = generate_signature_data()

    return result

if __name__ == "__main__":
    main()