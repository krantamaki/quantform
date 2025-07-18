# QuantForm instructions

## Installation

The QuantForm platform is meant to be ran on a Linux distribution (or WSL on Windows) and the instructions assume such. Much of the instructions could be applied to other platforms with proper domain knowledge.

The QuantForm platform is designed to be used with Python 3.12 and C++17. The setup scripts assume that GNU compiler is available for C++. 

Before the setup some steps need to be taken. The commands in the instructions should be ran in the root quantform directory where these instructions are located as well. The steps are

0. Install Python 3.12 and C++17 compiler. With Ubuntu or WSL this can be done by running the following commands in the terminal

    ```
    sudo add-apt-repository ppa:deadsnakes/ppa
    ```
    ```
    sudo apt update
    ```
    ```
    sudo apt install python3.12-full -y
    ```
    ```
    sudo apt-get update
    ```
    ```
    sudo apt-get install g++
    ```

1. Create a virtual environment by running the following commands in the terminal

    ```
    python3.12 -m venv .venv
    ```
    ```
    source .venv/bin/activate
    ```

2. Install the required Python dependencies

    ```
    python3.12 -m pip install --upgrade pip
    ```
    ```
    python3.12 -m pip install -r requirements.txt
    ```


## Setup

These steps need to be taken each time modifications are made to the source code. Once again these instructions are assumed to be ran from the root quantform directory. 

0. Fill the config file _src/config.yaml_. Note that the file can be copied and the sensitive information stored elsewhere (in fact this is recommended so that it doesn't accidentally end up being added to GitHub).

1. Install the _quantform_ library using pip. By using the _--editable_ flag changes in the Python code are will be reflected in the installed package without a need for a reinstall. However, for the changes in the C++ code to take effect the install needs to be redone. 

    ```
    python3 -m pip install --editable src
    ```

2. Run the tests to validate that nothing has been broken

    ```
    python3 src/tests.py
    ```

3. Run the _main.py_ file. Note that the main file needs to be filled before running it or it will raise a _NotImplementedError_. Here _\<path to config file\>_ is used to refer to the location where the config file filled in step 0 is stored.

    ```
    python3 src/main.py -c <path to config file>
    ```
