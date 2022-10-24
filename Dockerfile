FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY handlers /
COPY keyboards /
COPY lang /
COPY .env /
COPY bot_configure.py /
COPY main.py /
COPY support_files/order.db /


CMD [ "python3", "./main.py" ]