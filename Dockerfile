FROM python:3.12-bookworm

# Native libraries required by WeasyPrint's PDF renderer.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 \
    && apt-get clean

# add requirements.txt to the image
COPY requirements.txt /app/requirements.txt
WORKDIR /app/

# install python dependencies
RUN python -m pip install --upgrade pip setuptools \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY ./accessibility/ /app
COPY ./local_dev/run_web.sh /app/run_web.sh
RUN chmod +x /app/run_web.sh
