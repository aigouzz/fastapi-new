# fastapi后端项目

```
包含mysql redis jwt等通用接口框架

```


```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```
