# SQLite 迁移计划

本项目当前使用 `databases` 库和 SQLAlchemy ORM 与 MySQL 数据库进行交互。为了将项目迁移到支持 SQLite，需要进行以下主要更改：

**计划：**

1.  **修改数据库连接配置：**
    *   更新 `app/config/config.py` 中的数据库 URL，使其指向一个本地 SQLite 文件。
    *   可能需要添加一个新的配置项来指定 SQLite 数据库文件的路径。

2.  **更新数据库连接代码：**
    *   修改 `app/database/connection.py` 中的 `DATABASE_URL` 变量，使用新的 SQLite URL。
    *   检查 `create_engine` 和 `Database` 的参数，确保它们与 SQLite 兼容。`pool_pre_ping` 对于 SQLite 可能不需要或需要不同的配置。

3.  **检查和调整数据库模型：**
    *   查看 `app/database/models.py` 中的模型定义。
    *   特别关注数据类型，例如 `JSON` 类型在不同数据库中的实现可能略有差异。虽然 SQLAlchemy 会尽力抽象，但仍需注意潜在的不兼容性。

4.  **检查和调整数据库服务：**
    *   审查 `app/database/services.py` 中的所有数据库操作。
    *   确保使用的 SQLAlchemy 表达式和 `databases` 库的方法在 SQLite 中正常工作。
    *   注意任何可能依赖 MySQL 特定函数或语法的查询。

5.  **更新数据库初始化逻辑：**
    *   修改 `app/database/initialization.py` 中的代码，使其能够创建 SQLite 数据库文件和表。
    *   使用 SQLAlchemy 的 `metadata.create_all(engine)` 方法来创建表。

6.  **更新依赖：**
    *   在 `requirements.txt` 中添加 SQLite 相关的数据库驱动，例如 `aiosqlite` (用于 `databases` 库的异步支持) 和 `pysqlite3` (Python 标准库通常自带，但有时需要确保)。

7.  **测试：**
    *   在更改完成后，需要进行全面的测试，确保所有的数据库操作（读取、写入、更新、删除）都能在 SQLite 上正常工作。

以下是计划的 Mermaid 图示：

```mermaid
graph TD
    A[开始] --> B(分析现有数据库代码);
    B --> C{确定需要修改的文件};
    C --> D(修改数据库连接配置);
    D --> E(更新数据库连接代码);
    E --> F(检查和调整数据库模型);
    F --> G(检查和调整数据库服务);
    G --> H(更新数据库初始化逻辑);
    H --> I(更新依赖);
    I --> J(进行全面测试);
    J --> K[完成];