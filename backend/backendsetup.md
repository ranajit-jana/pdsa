### Setup Virtual Environment
1.  To install the nexessary libraries
    run `pip install fastapi uvicorn sqlalchemy psycopg2`

3.  Make sure you have virtual environment in your system
    else
    run `pip install virtualenv`

4.  Navigate to `backend` folder
    run `virtualenv venv`

5.  activate virtual environment

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

6.  To install all the dependencies

    [all dependencies in requirements.txt](requirements.txt)

    run

    ```
    pip install -r requirements.txt
    ```

7.  verify installation

    ```
    pip list
    ```

8.  If you want to deactivate the virutal environment
    run
    ```
    deactivate
    ```
