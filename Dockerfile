FROM python:3.7

# Install Dependencies
RUN apt update && \
    apt install \
    sqlite3 \
    -y

WORKDIR /astro-tablets

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./src ./src

VOLUME /astro-tablets/generated
VOLUME /astro-tablets/skyfield-data

ENTRYPOINT ["python", "./src/main.py"]
