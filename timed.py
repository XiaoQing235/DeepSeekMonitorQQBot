import time
import os

import requests

from check import check

os.system("cls")
print("StatusCheck is Running")

success = 0
times = 0

with open('logs.txt', "a+") as f:
    while True:
        try:
            times += 1
            print(f"Checking... {times}")

            checkresult = check()
            print(checkresult)

            if checkresult.get('info') == "Success":
                success += 1

            success_rate = (success / times) if times > 0 else 0
            succprob = f"{success_rate * 100:.2f}%"

            nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            log_line = f"{nowtime} {checkresult.get('code', 'N/A')} {checkresult.get('info', '')} {succprob}"
            f.write(log_line + '\n')
            f.flush()

            print(f"Times: {times}, Success Rate: {succprob}")
            requests.post("http://127.0.0.1/post",data={
                    "status_type": checkresult["available"],
                    "status_code": checkresult["code"],
                    "duration": checkresult["duration"],
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                    "availability":success_rate
            })
            time.sleep(300)

        except ZeroDivisionError:
            print("Error: Division by zero occurred")
        except KeyError as e:
            print(f"Missing key in checkresult: {e}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

