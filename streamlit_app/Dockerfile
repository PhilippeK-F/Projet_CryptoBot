FROM python:3.12-slim

RUN pip install pandas streamlit pillow numpy matplotlib pymongo sqlalchemy psycopg2-binary plotly

ADD . /app/

WORKDIR /app
EXPOSE 8501
CMD streamlit run app.py

# docker build -f dockerfile_streamlit .
# docker run -p 8501:8501 --network <network> <image>
# docker run -p 8501:8501 --network postgresql_default <image>
