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
docker run -tdi --restart unless-stopped -v D:/apps/twitter_logger:/usr/src/app --name twitter_logger twitter_logger
```


