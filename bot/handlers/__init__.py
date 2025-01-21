from bot.distpatchers import dp
from bot.handlers.main import router1, router2

dp.include_routers(*[
    router1,
    router2,
])
