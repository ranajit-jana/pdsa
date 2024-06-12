
### Prerequisite
1. Python version 3.12.3 or above
2. check if the following libraries are installed

```
sudo apt update
sudo apt install python3-dev libpq-dev
```


### Setup Virtual Environment

1.  Make sure you have virtual environment in your system
    else
    run `pip install virtualenv`

    ```
    sudo apt install python3.10-venv

    ```

2.  Navigate to `backend` folder
    run `virtualenv venv`


3.  activate virtual environment

    For Windows

    ```
    python3 -m venv venv
    venv\Scripts\activate
    ```

    for Linux

    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  To install all the dependencies

    [all dependencies in requirements.txt](requirements.txt)

    run

    ```
    pip install -r requirements.txt
    ```
5. To install the nexessary libraries
    run `pip install fastapi uvicorn sqlalchemy psycopg2`

6.  verify installation

    ```
    pip list
    ```

7. run the following to set `.env` file

    ```
    ./setenv.sh
    ```


    It will set the `.env` file

    ```
    Enter Database User: postgres
    Enter Database Password:
    Enter Database Host: localhost
    Enter Database Name: pdsa
    .env file updated successfully.
    ```
    If this step is not run the DB env will not be set

8. To run the command

   ```
    uvicorn app.main:app --reload

   ```

### Deactivate virtual environment

1.  If you want to deactivate the virtual environment

    run

    ```
    deactivate
    rm -rf venv
    ```
