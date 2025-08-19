# This line says "start with a Python 3.11 container that already exists"
# Think of it like: "Give me a computer that already has Python installed"
FROM python:3.11-slim

# This sets the working directory inside the container
# Like doing "cd /app" when you enter the container
WORKDIR /app

# Copy your requirements.txt file from your computer INTO the container
# This is like copy-pasting the file
COPY requirements.txt .

# Install the Python packages listed in requirements.txt
# Same as running "pip install -r requirements.txt" on your computer
RUN pip install -r requirements.txt

# Copy ALL your Python code from your computer INTO the container
# The "." means "copy everything from current directory"
COPY . .

# Tell Docker that your app will use port 8000
# This doesn't actually open the port, just documents it
EXPOSE 8000

# This is the command that runs when the container starts
# Like double-clicking your app to start it
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
