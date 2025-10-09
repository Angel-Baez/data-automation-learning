# 🔌 APIs Recomendadas para Práctica

## 🟢 **APIs sin autenticación (para empezar)**

### **JSONPlaceholder**

- **URL:** `https://jsonplaceholder.typicode.com/`
- **Datos:** Posts, usuarios, comentarios, álbumes fake
- **Uso:** Primeras prácticas con requests
- **Ejemplo:** `GET /posts` → Lista de posts

```python
import requests
response = requests.get('https://jsonplaceholder.typicode.com/posts')
posts = response.json()
```

### **CoinGecko API**

- **URL:** `https://api.coingecko.com/api/v3/`
- **Datos:** Precios y datos de criptomonedas
- **Uso:** Datos financieros reales
- **Ejemplo:** `GET /simple/price?ids=bitcoin&vs_currencies=usd`

### **REST Countries**

- **URL:** `https://restcountries.com/v3.1/`
- **Datos:** Información de países
- **Uso:** Datos geográficos y demográficos
- **Ejemplo:** `GET /all` → Todos los países

## 🟡 **APIs con registro gratuito**

### **OpenWeatherMap** ⭐ Recomendada

- **URL:** `https://openweathermap.org/api`
- **Registro:** api.openweathermap.org → Sign up
- **Límite:** 1000 calls/día gratis
- **Uso:** Datos meteorológicos para ETL

```python
api_key = "tu_api_key"
url = f"http://api.openweathermap.org/data/2.5/weather?q=Madrid&appid={api_key}"
```

### **News API**

- **URL:** `https://newsapi.org/`
- **Límite:** 100 requests/día gratis
- **Uso:** Noticias para análisis de texto

### **Alpha Vantage** (Finanzas)

- **URL:** `https://www.alphavantage.co/`
- **Límite:** 5 calls/minuto gratis
- **Uso:** Datos bursátiles para análisis financiero

## 🔵 **APIs para proyectos avanzados**

### **Reddit API**

- **Autenticación:** OAuth2
- **Uso:** Posts y comentarios para análisis de sentimientos
- **Setup:** Crear app en reddit.com/prefs/apps

### **Twitter API v2**

- **Límite:** 500K tweets/mes (gratis)
- **Uso:** Social media analytics
- **Requiere:** Approval process

### **GitHub API**

- **Autenticación:** Personal Access Token
- **Uso:** Datos de repositorios, commits, issues

```python
headers = {'Authorization': 'token tu_token'}
response = requests.get('https://api.github.com/user/repos', headers=headers)
```

## 📋 **Cronograma de uso sugerido**

| Semana | API Recomendada | Proyecto                      |
| ------ | --------------- | ----------------------------- |
| 6      | JSONPlaceholder | Primer script con requests    |
| 7      | OpenWeatherMap  | Reporte automático del clima  |
| 10     | CoinGecko       | ETL de precios crypto         |
| 13     | GitHub API      | Análisis de repos personales  |
| 16     | Reddit API      | Pipeline de análisis de posts |

## 🔧 **Tips de implementación**

### **Manejo de API Keys:**

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
```

### **Manejo de errores:**

```python
import requests
import time

def api_call_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
    return None
```

### **Rate limiting:**

```python
import time
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls_per_minute=60):
        self.calls_per_minute = calls_per_minute
        self.calls = []

    def wait_if_needed(self):
        now = datetime.now()
        # Remove calls older than 1 minute
        self.calls = [call_time for call_time in self.calls
                      if now - call_time < timedelta(minutes=1)]

        if len(self.calls) >= self.calls_per_minute:
            sleep_time = 60 - (now - self.calls[0]).seconds
            time.sleep(sleep_time)

        self.calls.append(now)
```
