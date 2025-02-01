import time
import os
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

            success_rate = (success / times) * 100 if times > 0 else 0
            succprob = f"{success_rate:.2f}%"

            nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            log_line = f"{nowtime} {checkresult.get('code', 'N/A')} {checkresult.get('info', '')} {succprob}"
            f.write(log_line + '\n')
            f.flush()

            print(f"Times: {times}, Success Rate: {succprob}")
            time.sleep(5)

        except ZeroDivisionError:
            print("Error: Division by zero occurred")
        except KeyError as e:
            print(f"Missing key in checkresult: {e}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            break
