FROM python:3.11.4-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev unixodbc-dev

COPY controle_codage_pmsi_ui/requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./consore-services/ /app/consore-services/

RUN cd /app/consore-services && pre-commit install

RUN cd /app/consore-services \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

COPY controle_codage_pmsi_ui/app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
