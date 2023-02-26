# Bot for tracking quotes on crypto exchanges.

## Local deployment

Copy via terminal repository:
```bash
git clone https://github.com/FeltsAzn/Ctypto_info_bot
```

#### If you are working with code editors `vim`, `nano`, `notepad` and others:
Installing a virtual environment if you don't have one locally.
```bash
python3 -m pip install --user virtualenv
```

Create a virtual environment in the copied repository:
```bash
python3 -m venv env
```

Activate the virtual environment:
```bash
source env/bin/activate
```

Install the dependency file in the virtual environment:
```bash
(venv):~<project path>$ pip install -r requirements.txt
```

Create a `.env` file in the project folder
```bash
touch.env
```

For correct work, you need to create a **logs** folder in the project repository:
```bash
mkdir logs
```


#### If you are using the IDE:
Install the dependency file in the virtual environment:
```bash
(venv):~<project path>$ pip install -r requirements.txt
```

Create a ***.env*** file in your project folder

Contents of the `.env` file:
```sh
MULTIPROCESSORING=ON
COMPOSE_PROJECT_NAME=<for docker images>
# WEBHOOK
DOMAIN_NAME=<webhook server domain>
WEBAPP_HOST=0.0.0.0
BOT_PORT=5555
WEBHOOK_PATH=/bot/

# TELEGRAM
ADMIN_NAME=<tg-url admin>
SUPER_ADMIN_ID=<tg id admin for logs>
BOT_TOKEN=<tg bot token>

# DATABASE
DATABASE_URL_ASYNC=sqlite+aiosqlite:///src/db/info.db
DATABASE_URL=sqlite:///src/db/info.db

#EXCHANGE DATA
EXCHANGES_DATA_COLLECTOR=http://exchanges_data:8888
# EXCHANGES_DATA_COLLECTOR=http://0.0.0.0:8888 for local run
# EXCHANGES_DATA_COLLECTOR=http://exchanges_data:8888 for docker run

# CREATE SENDING TEXT
TEXT_GENERATOR=http://text_creator:9999
# TEXT_GENERATOR=http://0.0.0.0:9999
# TEXT_GENERATOR=http://text_creator:9999

# CACHE
REDIS_URL=redis_server
REDIS_PORT=6379
REDIS_PASS=redis_password
# REDIS_URL=0.0.0.0 for local start
# REDIS_URL=redis_server for docker run

```


For correct work, you need to create a **logs** folder in the project repository:
```bash
mkdir logs
```


!!! IMPORTANT
1. Before starting, you need to create a database, for this you need to run **db/**`create_database.py`.
2. The bot will only work with its [backend](https://github.com/FeltsAzn/FastAPI-service-for-bot) part,
so before you start, download the 2nd part of the application.

Run from terminal -> `python3 app.py`


#### Docker container

You can deploy the application on a server or locally in a container using ***dockerfile***:
```bash
docker build . -t <image name>
```

And run the built image in a container:
```bash
docker run -d <image name>
```


It is possible to raise a cluster for the bot and its [backend](https://github.com/FeltsAzn/FastAPI-service-for-bot) parts in docker-compose:
```bash
"Changing the path to the API for the bot"

services:
   fastapi:
     image:fastapi
     container_name: fastapi_app
     ports:
     - "8000:8000"
     build:
       context: <absolute path in the system to the dockerfile_bot for the fastapi service>
       dockerfile_bot: dockerfile_bot
.....
```

We register in the IDE terminal or the terminal of the operating system:
```bash
docker compose -f docker-compose.dev.yaml up -d --build
```


_______________________________________________________________

The application is written in the `aiogramm` library. There are two types of operation: single-threaded mode and multiprocessor.



Run from terminal -> `python3 app.py`

The application is written in the `aiogramm` library. There are two types of operation: single-threaded mode and multiprocessor.
Changing the bot's mode of operation is possible through the "*.env*" file.

To start multiprocessor mode `MULTIPROCESSORING=ON`
To start single-threaded mode `MULTIPROCESSORING={Any characters}`

The bot consists of 3 parts:

- The implementation of user notifications is located in the *alerts_worker* folder.

- The bot user database and CRUD methods are in the *db* folder.

- Bot keyboard handlers are in the *handlers* folder


### Administrator
The administrative interface consists of a list of users and administrator settings (still in progress)

#### A list of users:
Viewing a list of users via inline-keyboard.
Available information:
- Telegram id
- Username
- Activity notifications

It is possible to delete a user at the request of the administrator
(disabled the ability to delete yourself through the administrative panel).

### User
The user interface consists of a list of monitored exchanges and settings

#### Settings
- Disable / enable notifications from the bot.
- Deleting an account from the bot database to stop receiving messages
(the bot writes the user to the database and will send notifications,
even after deleting the dialogue with the bot)

**The bot user receives notifications about currency quotes only available for sale/purchase.**


The bot is configured to work permanently on the server, so only in case of a critical error
the application will exit (server shutdown, manual stop, telegram error).

Requests to exchanges are made through an internal service written in `FastAPI`.

Filtering information by currencies is done through the `config.py` file in the *alerts_worker* folder.
Where constants are exposed:
- High percentage (highlighted in notifications)
- Starting percentage at which otp starts

send notifications to users
- The minimum step up when the quotes gap increases
- The minimum step down when the quotes gap increases

The cycle time for information processing from stock exchanges is ~3 seconds.
