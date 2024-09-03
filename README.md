# ChatBot-Genai: Chat with Your Documents

# LOCAL

## Installation

### Prerequisites

- Python 3.10 or higher
- A virtual environment (recommended)

### Clone the Repository

Clone the ChatBot-Genai repository from GitHub:

```bash
git clone https://github.com/ulumsai/engine-ai-pdf.git
```

### Using `venv`

1. Create a virtual environment:

```bash
python3 -m venv aipdf-venv
```

2. Activate the virtual environment:

```bash
source aipdf-venv/bin/activate
```

3. Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

1. **Set API Keys:**
```
cp .env.example .env
```
fill the key

2. **Export app**

```bash
export PYTHONPATH=/path/to/aipdf-flask
export FLASK_APP=app.py
export FLASK_ENV=development 
```

3. **Upload your all document into folder docs**

4. **Run the Application:**

```bash
flask run
```

# USE DOCKER

## Installation

1. instal docker 
2. run script 
    ```bash
    sh start.sh
    ```