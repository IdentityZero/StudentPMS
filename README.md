# Steps to start working on the project

## 1. Clone the repository
## 2. Create a Virtual Environment inside the same folder where you cloned the repo. Using the terminal type:
  ```python -m venv <virtual_environment_name>```
## 3. Use the virtual environment
Windows using cmd:
  ``` <virtual_environment_name>/Scripts/Activate  ``` <br>
Mac/Linux:
  ``` source <virtual_environment_name>/bin/Activate ```
## 4. Install dependencies
  ``` pip install -r requirements.txt```
## 5. Change directory
  ``` cd SPMS ```
## 6. Migrate Database
  ``` python manage.py migrate```
## 7. Start the server
  ``` python manage.py runserver```
