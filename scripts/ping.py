import asyncio

import stamina

from backend.dependencies import get_spam_assassin


@stamina.retry(
    on=Exception,
    attempts=10,
    wait_initial=5.0,
    timeout=60.0,
)
def is_spam_assassin_responsive():
    async def ping():
        sa = get_spam_assassin()
        await sa.ping()

    asyncio.run(ping())


if __name__ == "__main__":
    is_spam_assassin_responsive()
