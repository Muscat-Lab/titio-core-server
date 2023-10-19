# TITO Backend 입니다

![python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&label=v3.11)
![fastapi](https://img.shields.io/badge/Fastapi-009688?logo=fastapi&logoColor=white&label=v0.103.1)
![poetry](https://img.shields.io/badge/Poetry-60A5FA?logo=poetry&logoColor=white&label=v1.6.1)
![mysql](https://img.shields.io/badge/mysql-4479A1?logo=mysql&logoColor=white&label=v8.0.31)


## 프로젝트 시작하기

```bash
git clone https://github.com/Muscat-Lab/titio-core-server.git
cd TITO_CORE_API
```

## 로컬에서 서버를 실행하는 방법

### Requirements

- ![docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
- ![docker-compose](https://img.shields.io/badge/Docker_Compose-000000?logo=docsdotrs&logoColor=white)


### Step 1. 서버 실행

```bash
docker-compose up -d
```

![화면-기록-2023-10-06-오후-7 31 51](https://github.com/Muscat-Lab/TITO_Backend/assets/61671343/99842f78-cc02-4971-bfa3-81edd23ca2f5)



### Step 2. DB 테이블 생성

```bash
make migration_init
```


## 테스트

### 테스트용 DB 구성하기

1. 아래 경로의 `.env.test` 파일에 들어갑니다
```
TITO-Backend
├── .env.test
├── ...
```

2. 여기 써있는 db명과 같은 데이터베이스를 만들어야 합니다.
```.env
...
APP_DATABASE_NAME=dev-test
...
```

3. 기본적으로 APP_DATABASE_NAME 는 dev-test이기 때문에 아래 명령어로 테스트용 db를 생성할 수 있습니다
```bash
docker-compose exec mysql mysql -uroot -proot1234 -e "CREATE DATABASE \`dev-test\`;"
```

### 도커 쉘 들어가기

```bash
docker-compose exec -it fastapi /bin/bash
poetry shell
```

### 테스트 실행하기

```bash
pytest .
```
