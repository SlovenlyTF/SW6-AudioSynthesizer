# SonicEye Webserver

This webserver provides an API for interacting with our AI driven audio synthesis.

## Prepare & run server

**Make sure you have python installed**\
The code has only been tested on version 3.11, but should run fine on 3.8 and above.

> To check which version of python you are running, check the output of `python --version`.

**Install dependencies**

Python dependencies are stored in the requirements.txt file.

To install with pip run the command `pip install -r requirements.txt`

Additionally, for any MIDI related endpoints to work, you need to install [fluidsynth](https://www.fluidsynth.org/).

> On Arch, fluidsynth can be installed through the `fluidsynth` package.

**Run the server**\
Finally, run the server using waitress by executing run.sh, or directly with `waitress-serve --host 0.0.0.0 --port=5000 --call app_server:create_app`.

You can check if the server is running by sending a get request to the URI specified in the last line of this output. E.g. by running `curl 127.0.0.1:5000` or opening the URI in a web browser.

You should receive a status message.

## Attributions

Many thanks to the talented people behind the sound fonts that we use.

**Violin**
https://musical-artifacts.com/artifacts/3149

**Tuba**
https://musical-artifacts.com/artifacts/419

**Hurdy Gurdy**
https://musical-artifacts.com/artifacts/2897

**Female vocalizer**
https://musical-artifacts.com/artifacts/3004

**Zombie**
https://musical-artifacts.com/artifacts/2363

**Windows vista**
https://musical-artifacts.com/artifacts/2594
