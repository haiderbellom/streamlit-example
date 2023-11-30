pip install -r requirements.txt

python ETL\extract.py

python ETL\transform.py

python ETL\load.py

streamlit ETL\run app.py

python -m streamlit run ETL\app.py
