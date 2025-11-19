from bot.distpatchers import dp
from bot.handlers.start import router

dp.include_routers(*[
    router,

])
