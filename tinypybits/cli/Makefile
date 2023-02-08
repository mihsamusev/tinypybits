
run-dev:
	uvicorn server:app --port 8888 --reload

create-dotenv:
	echo "JWT_SECRET_KEY=$$(openssl rand -hex 32)" > .env && \
	echo "JWT_ALGORITHM=HS256" >> .env && \
	echo "JWT_TOKEN_EXPIRE_MINUTES=15" >> .env

test:
	python -m pytest


