# Trading API

### Usage

#### Docker

```powershell
ren .env.example .env
```
> Input your api keys
```powershell
docker-compose up --build
```

#### Local

```powershell
python -m venv venv
```
```powershell
venv/Scripts/activate
```
```powershell
pip install -r requirements.txt
```
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
