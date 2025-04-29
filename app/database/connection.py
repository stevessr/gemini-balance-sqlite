"""
数据库连接池模块
"""
from databases import Database
from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import sessionmaker # 不再需要
from sqlalchemy.ext.declarative import declarative_base

from app.config.config import settings
from app.log.logger import get_database_logger

logger = get_database_logger()

# 数据库URL
DATABASE_URL = f"sqlite:///{settings.SQLITE_DATABASE_PATH}"

# 创建数据库引擎
# SQLite 是文件数据库，不需要连接池参数，也不需要 pool_pre_ping
# connect_args={"check_same_thread": False} 对于 SQLite 是必需的，因为默认情况下 SQLite 不允许跨线程共享连接
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建元数据对象
metadata = MetaData()

# 创建基类
Base = declarative_base(metadata=metadata)

# 创建数据库连接池，并配置连接池参数
# 对于 SQLite，databases 库的连接池参数通常不需要像关系型数据库那样精细配置
# 对于 SQLite，不需要传递连接池参数给底层的 sqlite3.connect
database = Database(DATABASE_URL)

# 移除了 SessionLocal 和 get_db 函数

# --- Async connection functions for lifespan/async routes ---
async def connect_to_db():
    """
    连接到数据库
    """
    try:
        await database.connect()
        logger.info("Connected to database")
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise


async def disconnect_from_db():
    """
    断开数据库连接
    """
    try:
        await database.disconnect()
        logger.info("Disconnected from database")
    except Exception as e:
        logger.error(f"Failed to disconnect from database: {str(e)}")
