# auth strign

```bash
curl http:localhost:8888/token -d "username=alice&password=secret"
curl http:localhost:8888/token -F username=alice -F password=secret

# then use the bearer for the requests (Otherwise will 401)
curl http://localhost:8888/good_stuff -H 'Authorization: Bearer alice'
```