# Chatbot Setup


1) In the chatbot dir, make python 3.7 virtual environment
  sudo apt update
  sudo apt install python3-dev python3-pip
  python3 -m venv ./venv
   
2) Activate environment using command "source ./venv/bin/activate"
3) Run "pip3 install -r requirements.txt"
4) Run the command "./train.sh" in terminal to train NLU model
5) Open a terminal in the same dir, and run "./action.sh"
5) Open a terminal in the same dir, and run "./rserver.sh"
