python3 -m venv .venv
source .venv/bin/activate

# instal package
pip install -r requirements.txt

# torch
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# run backend server
# uvicorn app:app --host 0.0.0.0 --port 8000
python main.py
