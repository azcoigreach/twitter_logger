# Twitter Logger

Dockerized Twitter Logger stroing to a MOngo DB.

Modify config.py with Twitter Keys and DB minformation.

x86 build

* BUILD

```
 docker build -t twitter_logger https://github.com/azcoigreach/twitter_logger.git
 ```

* RUN

```
docker run -tdi --restart unless-stopped -v D:/apps/twitter_logger:/usr/src/app/twitter_logger/app --log-driver json-file --log-opt max-size=20m --name twitter_logger twitter_logger
```

* TODO

    - /app directory not copying to shared volumes on Windows.  Permissions issues. Need to correct.  Manual copy required to windows share for config.py and twitter_logger.py
