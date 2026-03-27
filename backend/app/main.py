from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import settings
from database import init_db
from routes import staff_router, service_router, client_router, appointment_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url='/api/docs',
    redoc_url='/api/redoc'
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем папку со статикой (для фото мастеров/услуг)
app.mount('/static', StaticFiles(directory=settings.static_dir), name='static')

# Подключаем роутеры нашего проекта
app.include_router(staff_router.router)
app.include_router(service_router.router)
app.include_router(client_router.router)
app.include_router(appointment_router.router)


@app.on_event('startup')
def on_startup():
    # Создаем таблицы в БД при запуске
    init_db()

@app.get('/')
def root():
    return {
        'message': f'Welcome to {settings.app_name} API',
        "docs": "/api/docs",
    }

@app.get('/health')
def health_check():
    return {'status': 'healthy'}
