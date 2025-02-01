import asyncio
import websockets
import json
import uuid
from typing import Dict

global client


class OneBotClient:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self.connection = None
        self.pending_requests: Dict[str, asyncio.Future] = {}

    async def connect(self):
        while True:
            try:
                print(f"尝试连接至 {self.ws_url}...")
                self.connection = await websockets.connect(
                    self.ws_url,
                    ping_interval=20,
                    ping_timeout=30
                )
                print("连接成功！")
                await asyncio.create_task(self.receiver())
                await self._keep_alive()  # 重置重连间隔
            except (ConnectionRefusedError, websockets.ConnectionClosed):
                print("连接失败，30秒后重试...")
                await asyncio.sleep(30)

    async def receiver(self):
        try:
            async for message in self.connection:
                data = json.loads(message)

                if "echo" in data:
                    future = self.pending_requests.pop(data["echo"], None)
                    if future and not future.done():
                        future.set_result(data)

                else:
                    print("\n[事件推送]", data)
        except websockets.ConnectionClosed:
            print("连接已断开")

    async def post_action(self, action: str, params: dict) -> dict:
        """
        发送OneBot API请求
        :param action: API动作名称，如'send_private_msg'
        :param params: API参数
        :return: 服务端响应
        """
        if not self.connection or self.connection.closed:
            return {"status": "error", "msg": "未建立连接"}

        echo = str(uuid.uuid4())
        payload = {
            "action": action,
            "params": params,
            "echo": echo
        }

        future = asyncio.get_event_loop().create_future()
        self.pending_requests[echo] = future

        try:
            await self.connection.send(json.dumps(payload))
            return await asyncio.wait_for(future, timeout=10)
        except asyncio.TimeoutError:
            await self.pending_requests.pop(echo, None)
            return {"status": "timeout", "echo": echo}
        except Exception as e:
            return {"status": "error", "msg": str(e)}

    async def _keep_alive(self):
        while self.connection.open:
            await self.post_action("get_status", {})
            await asyncio.sleep(15)


async def main():
    client = OneBotClient("ws://127.0.0.1:22801")
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())
