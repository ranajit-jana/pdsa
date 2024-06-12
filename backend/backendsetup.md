### Setup Virtual Environment

1.  Make sure you have virtual environment in your system
    else
    run `pip install virtualenv`

2.  Navigate to `backend` folder
    run `virtualenv venv`

3.  activate virtual environment

    For Windows

        ```bash
        python3 -m venv venv
        venv\Scripts\activate
        ```

    for Linux
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

4.  To install all the dependencies

    run

    ```
    pip install -r requirements.txt
    ```

5.  verify installation

    ```
    pip list
    ```

6.  If you want to deactivate the virutal environment
    run
    ```
    deactivate
    ```
