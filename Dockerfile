FROM python:3.9.7

WORKDIR /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev unixodbc-dev

COPY controle_codage_pmsi_ui/requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./consore-services/ /app/consore-services/

RUN cd /app/consore-services && pre-commit install

RUN cd /app/consore-services && poetry export -o /app/poetry_requirements.txt
RUN pip install --no-cache-dir -r poetry_requirements.txt

COPY controle_codage_pmsi_ui/app.py .

ENV PYTHONPATH "$PYTHONPATH:/app/consore-services"

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
