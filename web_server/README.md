# EchoPond Webserver

This webserver provides an API for interacting with our AI driven audio synthesis.

## Prepare & run server

**Make sure you have python installed**\
The code has only been tested on version 3.11, but should run fine on 3.8 and above.

> To check which version of python you are running, check the output of `python --version`.

**Install dependencies**

- Flask

To install with pip run the command `pip install flask`

**Run the server**\
Finally, run the server using the command `python -m flask --app app_server run`.

*Expected output:*
```
 * Serving Flask app 'app_server'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

You can check if the server is running by sending a get request to the URI specified in the last line of this output. E.g. by running `curl 127.0.0.1:5000` or opening the URI in a web browser.

You should receive a status message.
