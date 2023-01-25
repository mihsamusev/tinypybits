
run-dev:
	uvicorn server:app --port 8888 --reload

create-dotenv:
	echo "SECRET_KEY=$$(openssl rand -hex 32)" > .env && \
	echo "ALGORITHM=HS256" >> .env && \
	echo "ACCESS_JWT_EXPIRE_MINUTES=15" >> .env

test:
	python -m pytest


