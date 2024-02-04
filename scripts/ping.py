import aiospamc
import stamina
from syncer import sync


@stamina.retry(
    on=Exception,
    attempts=10,
    wait_initial=5.0,
    timeout=60.0,
)
@sync
async def is_spam_assassin_responsive():
    await aiospamc.ping()


if __name__ == "__main__":
    is_spam_assassin_responsive()  # type: ignore
