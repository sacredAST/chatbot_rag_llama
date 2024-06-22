FROM python:3.8.18

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./rag_bot /app/rag_bot

RUN printf '#!/bin/bash \n\
python /app/rag_bot/pull_model.py \n\
streamlit run /app/rag_bot/app.py' >> /app/rag_bot/run.sh

CMD ["bash", "/app/rag_bot/run.sh"]