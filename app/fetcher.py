import aiohttp, asyncio
from .config import get_settings

SETTINGS = get_settings()

async def fetch_html(url: str) -> tuple[str, dict[str, str]]:
    proxy_list = (SETTINGS.proxies.split(",") if SETTINGS.proxies else None)
    proxy = None if not proxy_list else proxy_list[0].strip()
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, proxy=proxy, headers={"User-Agent": "TechLookupBot/0.1"}) as resp:
            html = await resp.text("utf-8", errors="ignore")
            return html, dict(resp.headers)