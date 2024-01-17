FROM python:3.12.1

WORKDIR /divifilter

COPY . /divifilter

WORKDIR /divifilter

RUN pip install -r /divifilter/requirements.txt

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost/_stcore/health

ENV STREAMLIT_SERVER_PORT=80
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

ENTRYPOINT ["streamlit", "run", "dividend_stocks_filterer/ui.py"]
