FROM python:3.12

ENV PYTHONUNBUFFERED=1

# İş qovluğunu təyin edirik
WORKDIR /code

# Asılılıqları kopyalayırıq
COPY requirements.txt /code/

# Asılılıqları quraşdırırıq
RUN apt-get update && apt-get install -y \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Layihə fayllarını kopyalayırıq
COPY ./epin_website .  

# Django serverini işə salırıq
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]