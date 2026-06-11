# 汇率换算与定时推送 API 服务

```bash
cp .env.example .env
docker compose up --build
```

提供实时汇率、历史曲线、货币换算、订阅通知、API Key 鉴权和调用统计的纯后端 API 服务。

## 项目主要功能

- 查询指定货币对实时汇率，支持批量查询
- 查询日期范围内历史汇率曲线
- 输入金额进行货币换算，支持 USD 中转链式换算
- 返回 30 种主要货币代码、名称和符号
- 订阅目标汇率，触发后模拟 Webhook/邮件通知
- APScheduler 每小时同步外部汇率 API
- 用户注册生成 API Key，Header 鉴权并记录调用量
- 查询时间段内调用次数和接口分布

## 本地开发方式

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API 文档地址：http://localhost:19410/docs

## 技术栈

| 分类 | 技术 |
| --- | --- |
| 后端框架 | Python + FastAPI |
| ORM | SQLAlchemy |
| 数据库 | PostgreSQL |
| 认证 | API Key |
| 定时任务 | APScheduler |
| HTTP 客户端 | httpx |
| 部署 | Docker Compose |

## 项目目录结构

```text
backend/
├── app/
│   ├── routers/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   ├── tasks/
│   ├── constants/
│   ├── utils/
│   ├── middleware/
│   ├── config.py
│   └── main.py
├── Dockerfile
└── requirements.txt
database/
└── init.sql
```

## 主要 API 列表

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/health` | 健康检查 |
| POST | `/api/v1/apikey/register` | 注册并生成 API Key |
| GET | `/api/v1/exchange/latest` | 查询实时汇率 |
| GET | `/api/v1/exchange/history` | 查询历史汇率 |
| GET | `/api/v1/exchange/currencies` | 查询支持货币 |
| POST | `/api/v1/convert` | 货币换算 |
| POST | `/api/v1/subscribe` | 创建汇率订阅 |
| GET | `/api/v1/subscribe` | 查询订阅列表 |
| GET | `/api/v1/apikey/stats` | 查询调用统计 |

## 环境变量说明

| 变量 | 说明 |
| --- | --- |
| COMPOSE_PROJECT_NAME | Compose 项目名 |
| POSTGRES_DB | 数据库名 |
| POSTGRES_USER | 数据库用户 |
| POSTGRES_PASSWORD | 数据库密码 |
| DATABASE_URL | SQLAlchemy 数据库连接串 |
| EXCHANGE_API_URL | 外部汇率 API 地址 |
| DEFAULT_API_KEY | 演示 API Key |

## License

MIT
