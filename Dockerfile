FROM python:3.9.7

WORKDIR /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev unixodbc-dev

COPY controle_codage_pmsi_ui/requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY consore-services/ .

WORKDIR /app/consore-services/

RUN pre-commit install

RUN poetry install --no-root

WORKDIR /app

COPY controle_codage_pmsi_ui/app.py .
COPY controle_codage_pmsi_ui/mock.py .

ENV PYTHONPATH "$PYTHONPATH:/app/consore-services"

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
