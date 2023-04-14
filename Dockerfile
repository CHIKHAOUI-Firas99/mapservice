# 
FROM python:3.10.2

# 
RUN apt-get update && apt-get install -y build-essential libpq-dev libffi-dev libssl-dev git

# 
COPY ./requirements.txt /requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

RUN pip install python-jose

RUN pip install python-dotenv
# 
COPY ./ /

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
