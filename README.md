# myapp setup

## Use these commands on your terminal

```bash
git clone https://github.com/gi0rkyr/OEP_thesis.git
cd OEP_thesis/ 

chmod u+x setup.sh
sh -x setup.sh

python3 -m venv .my_venv
source .my_venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py createsuperuser
python3 manage.py runserver
```