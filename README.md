# Bot for tracking quotes on crypto exchanges.

### Message example: 
```
📉  ALGO-USDC:
min:   0.217700$ - KUCOIN
max:   0.228100$ - HUOBI
diff: 4.55%
common networks: ALGO
Volume of trading on KUCOIN:
 🔴 5m:   138534.31 (0.0%)
 ⚪ 30m: 138540.55 (0.0%)
 ⚪ 1h:     138540.55 (0.0%)
 ⚪ 4h:     138540.55 (0.0%)
 ⚪ day:   138540.55 (0.0%)
```


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
