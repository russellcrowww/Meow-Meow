import httpx

async def send_tg_notification(message: str):
    token = "8658995129:AAHBvN04JbFsY8WAvyF6NyCps2P9wi_-Q3g"
    chat_id = "@IamPusselcrow"
    url = f"https://api.telegram.org{token}/sendMessage"
    
    async with httpx.AsyncClient() as client:
        await client.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        })
