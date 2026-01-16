# Bot Feriados Argentina 🇦🇷

Bot de Twitter que publica automáticamente el tiempo restante para el próximo feriado en Argentina.

## Funcionalidades

- Publica 3 veces al día (9:00, 15:00 y 21:00 hora Argentina)
- Obtiene los feriados desde la [API de Argentina Datos](https://argentinadatos.com/)
- Cachea los feriados localmente para minimizar consultas a la API
- Mensajes personalizados según la proximidad del feriado

## Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/botFeriadosNacionales.git
cd botFeriadosNacionales
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar credenciales de Twitter

Crear un archivo `.env` en la raíz del proyecto:

```env
TWITTER_API_KEY=tu_api_key
TWITTER_KEY_SECRET=tu_api_key_secret
TWITTER_ACCESS_TOKEN=tu_access_token
TWITTER_ACCESS_TOKEN_SECRET=tu_access_token_secret
```

> Las credenciales se obtienen desde el [Portal de Desarrolladores de Twitter](https://developer.twitter.com/). La app debe tener permisos de **Read and Write**.

### 4. Ejecutar localmente

```bash
python main.py
```

## Despliegue en GitHub Actions

El bot está configurado para ejecutarse automáticamente usando GitHub Actions.

### Configurar Secrets

En tu repositorio de GitHub, ir a **Settings → Secrets and variables → Actions** y agregar:

- `TWITTER_API_KEY`
- `TWITTER_KEY_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`

### Ejecución manual

También podés ejecutar el workflow manualmente desde la pestaña **Actions** → **Publicar feriado** → **Run workflow**.

## Estructura del proyecto

```
botFeriadosNacionales/
├── main.py              # Lógica principal del bot
├── twitter.py           # Funciones para publicar en Twitter
├── feriados.json        # Caché de feriados (se genera automáticamente)
├── requirements.txt     # Dependencias de Python
├── .env                 # Credenciales (no incluido en el repo)
└── .github/
    └── workflows/
        └── twittear.yml # Workflow de GitHub Actions
```

## API utilizada

Los feriados se obtienen de [Argentina Datos](https://argentinadatos.com/):

```
GET https://api.argentinadatos.com/v1/feriados/{año}
```

## Licencia

MIT
