import stamina
from syncer import sync

from backend.dependencies import get_spam_assassin


@stamina.retry(
    on=Exception,
    attempts=10,
    wait_initial=5.0,
    timeout=60.0,
)
@sync
async def is_spam_assassin_responsive():
    sa = get_spam_assassin()
    await sa.ping()


if __name__ == "__main__":
    is_spam_assassin_responsive()  # type: ignore
