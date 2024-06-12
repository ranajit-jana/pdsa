### Setup Virtual Environment
1.  Make sure you have virtual environment in your system
    else
    run `pip install virtualenv`

2.  Navigate to `backend` folder
    run `virtualenv venv`

2.  activate virtual environment

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

7.  If you want to deactivate the virutal environment
    run
    ```
    deactivate
    ```
