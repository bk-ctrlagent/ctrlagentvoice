import os
import asyncio
import aiohttp

CTRL_BASE     = os.getenv("CTRL_BASE",      "http://44.204.7.58")
CTRL_EMAIL    = os.getenv("CTRL_EMAIL",     "b@g.com")
CTRL_PASSWORD = os.getenv("CTRL_PASSWORD",  "Test@123")
ACCOUNT_ID    = os.getenv("ACCOUNT_ID",     "a33bdd97-8181-4e7c-a583-ac3b4cf90b9b")
AGENT_ID      = os.getenv("AGENT_ID",       "892fba16-17ab-41ad-bc14-e8fabf34cc1a")

async def login_ctrlagent(email: str, password: str) -> str:
    async with aiohttp.ClientSession() as sess:
        r = await sess.post(
            f"{CTRL_BASE}/ctrlagent/auth/login",
            json={"email": email, "password": password},
            ssl=False,
        )
        r.raise_for_status()
        return (await r.json())["access_token"]

async def new_conversation(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession(headers=headers) as sess:
        r = await sess.post(
            f"{CTRL_BASE}/api/v1/conversation/new",
            json={"account_id": ACCOUNT_ID, "agent_id": AGENT_ID, "initial_variables": {}},
            ssl=False,
        )
        r.raise_for_status()
        d = await r.json()
        return d.get("conversation_id") or d.get("conversationId") or d.get("id")

async def query_ws(token: str, conv_id: str) -> tuple[str, str]:
    ws_url = (
        f"ws://44.204.7.58/api/v1/ws/conversation/"
        f"{conv_id}?token={token}&channel=voice"
    )
    return ws_url


async def main():
    token = await login_ctrlagent(CTRL_EMAIL, CTRL_PASSWORD)
    conv_id = await new_conversation(token)
    ws = await query_ws(token, conv_id)
    print(ws)

if __name__ == "__main__":
    asyncio.run(main())
