import requests
import json
import time

head = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sk-c78fff1e8f4548c5ac6141cc28d5d65b'
}


def check():
    global result
    global duration
    try:
        startTime = time.time()
        result = requests.post("https://api.deepseek.com/chat/completions", headers=head, json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "This is a test. JUST AND ONLY say \"IM HERE.\"."},
                {"role": "user", "content": "Are you here?"}
            ],
            "stream": False,
            "temperature": 0.1
        })
        duration = time.time() - startTime
        # print(result.text)


        output = json.loads(result.text).get("choices")[0].get("message").get("content")
        print(output)

        if (result.status_code == 200) and (output == "IM HERE."):
            return {'available': 1, 'info': 'Success', 'code': result.status_code, 'time': duration}
        elif result.status_code == 200:
            return {'available': 2, 'info': '200 OK, Incorrect Answer', 'code': result.status_code, 'time': duration}

    except requests.ConnectTimeout:
        return {'available': 0, 'info': 'Connect Timeout', 'code': result.status_code, 'time': duration}
    except requests.ConnectionError:
        return {'available': 0, 'info': 'Connect Failed', 'code': result.status_code, 'time': duration}
    except Exception as e:
        return {'available': 0, 'info': e, 'code': result.status_code, 'time': duration}


if __name__ == '__main__':
    print(check())
