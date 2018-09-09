FROM jupyter/datascience-notebook

USER root
# Dependencies specific to barcode reading
RUN apt-get update && apt-get install -y --no-install-recommends \
		libzbar-dev \
		libzbar0

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ADD AWS_Vin_ver2_commented.py ./

CMD [ "python", "./AWS_Vin_ver2_commented.py" ]

