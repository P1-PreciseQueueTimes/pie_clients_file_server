python -m venv .venv
source ~/.venv/bin/activate
rm -rf pie_clients_file_server
git clone https://github.com/P1-PreciseQueueTimes/pie_clients_file_server
cd pie_clients_file_server
pip install requirements.txt

python pie_clients/receiver.py
