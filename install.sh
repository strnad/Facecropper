#!/bin/bash
echo "Creating virtual environment..."
python -m venv venv
echo "Activating virtual environment..."
source venv/Scripts/activate
echo ""
echo "Installing requirements..."
pip install -r requirements.txt
mkdir _INPUT
mkdir _OUTPUT
echo "Installation complete. Use run.sh to run the script."
read -p "Press enter to exit."