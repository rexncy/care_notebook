FROM python:3-slim-buster

RUN apt-get update && apt-get install -y wget gnupg2 unzip bash

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
# Install pip packages
RUN pip install -U pip
RUN pip install --no-cache-dir splinter
RUN pip install --no-cache-dir selenium
RUN pip install --no-cache-dir webdriver-manager
RUN pip install --no-cache-dir pandas
RUN pip install --no-cache-dir openpyxl

# for df style
RUN pip install --no-cache-dir jinja2
RUN pip install --no-cache-dir schedule
RUN pip install --no-cache-dir pytz
COPY . /app/
ENV TZ Asia/Hong_Kong
RUN mkdir /app/data

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]