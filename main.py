from fastapi import FastAPI
from api.users.routers import user_router
from api.company.routers import company_router
from api.stock.routers import stock_router
from web.routers import web_router

app = FastAPI(
    title="Система управления запасами",
    description="Система управления запасами(материалами) предположим на складе"
                " и автоматическая отправка заявки на email компаний(предварительно нужно добавить эти компании) "
                "у которых есть данный материал. Используется nosql база данных, а конкретно Redis",
    version="0.1.0",
    contact={
        'name': "Victor",
        "email": "krupeichenkovictor@gmail.com"
    }
)
app.include_router(user_router)
app.include_router(company_router)
app.include_router(stock_router)
app.include_router(web_router)
