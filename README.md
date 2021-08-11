# Customer Relationship Management System
## SETUP
#### Creating and activating virtual environment

```python
  virtualenv venv
  source venv/bin/activate
```
#### Install the project's dependencies
```python
  pip install -r requirements.txt
```
#### env variables
<p>Create a new file named <code>.env</code> inside the <code>djcrm</code> folder.</p>
<p>Copy all of the variables inside <code>djcrm/.template.env</code> and assign your own values to them</p>
<p>Run export <code>READ_DOT_ENV_FILE=True</code> inside your terminal so that your environment variables file will be read.</p>

#### open localhost

```python
  python manage.py migrate
  python manage.py runserver

```
## Acknowledgements
Created By-Shreya Singh,3rd year student at Jaypee Institute of Information Technology Noida
