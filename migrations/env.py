from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
import os
import sys
import time

print("=" * 50)
print("Начало выполнения миграций...")
print(f"Текущая рабочая директория: {os.getcwd()}")
print(f"Файлы в текущей директории: {os.listdir('.')}")
print("=" * 50)

# ----- НАСТРОЙКА ПУТЕЙ ИМПОРТА -----
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../app'))
sys.path.insert(0, app_dir)

print(f"Директория приложения: {app_dir}")
print(f"sys.path: {sys.path}")
print("=" * 50)

# Пытаемся импортировать модули приложения
try:
    if not os.path.exists(app_dir):
        raise Exception(f"Директория приложения не найдена: {app_dir}")

    print(f"Содержимое директории приложения: {os.listdir(app_dir)}")

    from app.core.config import settings
    from app.db.base import Base  # Ключевое изменение!
    import app.db.models

    print("✅ Модули приложения успешно импортированы")
except Exception as e:
    print(f"❌ Ошибка импорта: {e}")
    if os.path.exists(app_dir):
        print("Проверка структуры директории app:")
        for root, dirs, files in os.walk(app_dir):
            print(f"{root}:")
            print(f"  ДИРЕКТОРИИ: {dirs}")
            print(f"  ФАЙЛЫ: {files}")
    raise

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    sync_url = settings.POSTGRES_URL.replace("asyncpg", "psycopg2")
    context.configure(
        url=sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    sync_url = settings.POSTGRES_URL.replace("asyncpg", "psycopg2")

    print("=" * 50)
    print(f"Попытка подключения к базе данных по адресу: {sync_url}")
    print("=" * 50)

    max_attempts = 10
    for attempt in range(1, max_attempts + 1):
        try:
            connectable = create_engine(
                sync_url,
                poolclass=pool.NullPool,
            )

            with connectable.connect() as connection:
                print("✅ Успешное подключение к базе данных")
                context.configure(
                    connection=connection,
                    target_metadata=target_metadata,
                    compare_type=True,
                    compare_server_default=True,
                )
                with context.begin_transaction():
                    context.run_migrations()
            break
        except Exception as e:
            print(f"⚠️ Попытка подключения {attempt}/{max_attempts} не удалась: {str(e)}")
            if attempt == max_attempts:
                print("❌ Все попытки подключения не удались")
                raise
            delay = 2 ** (attempt - 1)
            print(f"⏳ Ожидание {delay} секунд перед следующей попыткой...")
            time.sleep(delay)


if context.is_offline_mode():
    print("Выполнение миграций в OFFLINE режиме")
    run_migrations_offline()
else:
    print("Выполнение миграций в ONLINE режиме")
    run_migrations_online()