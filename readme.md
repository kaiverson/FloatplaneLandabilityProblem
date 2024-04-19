# How to Run main.py

This document provides a detailed guide on how to install and run `main.py` using a Python virtual environment. This process involves setting up a virtual environment, installing dependencies, and running the Python script.

## Prerequisites

Before you begin, ensure you have Python installed on your system. You can download Python from [the official Python website](https://www.python.org/downloads/).

## Step 1: Setup a Virtual Environment

First, you need to create a virtual environment to manage your project's dependencies separately from your global Python installation. Open your terminal and run the following commands:

```bash
# Navigate to your project directory
cd path/to/your/project

# Create a virtual environment named 'venv'
python3 -m venv venv
```

## Step 2: Activate the Virtual Environment

Once the virtual environment is created, you need to activate it. Activation will ensure that the Python and pip you use will be from within this environment, isolated from the global installation.

```bash
# Activate the virtual environment
source venv/bin/activate
```

For Windows users, activate the virtual environment with:

```bash
.\venv\Scripts\activate
```

## Step 3: Install Dependencies

Run the following commands to install the requirements for the project.

```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt
```


## Step 4: Run the Python Script

With the environment set up and dependencies installed, you are now ready to run `main.py`.

```bash
# Run main.py
python main.py
```

## Step 5: Deactivate the Virtual Environment

After running your script, you can deactivate the virtual environment to return to your global Python setup:

```bash
# Deactivate the virtual environment
deactivate
```

After running this, there should be a "map.html" file and "detected_lakes.csv" file that you can view some of the results in.