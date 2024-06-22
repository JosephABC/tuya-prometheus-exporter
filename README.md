# tuya-prometheus-exporter

## Set up
```
python -m venv .venv

pip install -r requirements.txt
```

## Build
```
docker buildx build -f Dockerfile . -t tuya-prometheus-exporter
```


## Run
```
docker run -p 9090:9090 -v ./config.yaml:/config.yaml tuya-prometheus-exporter
```
