# Test task for ProstoPay

### set env vars and all perms

```shell
cp .env.sample .env
chmod 777 dc.sh 
chmod 777 coverage.sh
chmod 777 coverage-test.sh
chmod 777 coverage-report.sh
chmod 777 coverage-export.sh
chmod 777 migrate-db.sh
chmod 777 downgrade-db.sh
```

#### run tests

###### run server and test

```shell
./dc.sh up -d server
./coverage-test.sh
```

###### report terminal

```shell
./coverage-report.sh
```

###### report html

```shell
./coverage-export.sh
```

###### stop server after tests

```shell
./dc.sh down
```

### migrate

```shell
./migrate-db.sh
```

### run server

```shell
./dc.sh up -d
```

### stop server

```shell
./dc.sh down
```
