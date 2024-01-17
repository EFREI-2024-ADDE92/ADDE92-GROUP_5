FROM python:3.11.0

# set the working directory in the container
WORKDIR /app

# ADD all files 
COPY . /app

# install required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000
# command to run on container start
CMD ["python", "app.py"]