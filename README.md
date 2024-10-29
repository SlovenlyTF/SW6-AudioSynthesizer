# Sonic Eye 🧿
*Exploring Timbre Transfer in Portable Creativity Support Tools for Musicians*\
*Authors: Tobias Friese, Jack Skaarup Munn, Mads Hjerrild Hansen & August Louis Kuhn Jeppesen*

This README contains a very short introduction to the background for and components of the project.

## Introduction
This repository contains the implementation for our Software BSc project at Aalborg University CPH.\
We set out to answer the following problem statement:

> How can a portable creativity support tool for musicians
be designed and implemented to support the exploration and storage
of auditory ideas, utilizing timbre transfer to enhance creativity?

For more information about the project you can reach out and read the research paper written about it.

The implementation consists of three parts; the app (frontend), the webserver (backend), and the AI model(s).

## AI
In order to perform timbre transfer, we sought to implement a machine learning model.
We tried an array of different approaches and models and lastly implemented a CycleGAN model.
Sadly this model never received a proper amount of training due to lack of time and hardware.

You can listen to the outputs of our models on the project's [GitHub pages](https://slovenlytf.github.io/SW6-AudioSynthesizer/).

## App
The timbre transfer of Sonic Eye is accessible through a frontend in the form of an app.
The app is written in Dart using Flutter, as to ensure compatibility across mobile devices.

<div align="center">
<img
alt="Sonic Eye home page"
src="https://github.com/SlovenlyTF/SW6-AudioSynthesizer/blob/main/docs/images/app_screenshot_home_page.jpg?raw=true"
height=512
/>
<img
alt="Sonic Eye archive page"
src="https://github.com/SlovenlyTF/SW6-AudioSynthesizer/blob/main/docs/images/app_screenshot_archive.jpg?raw=true"
height=512
/>
</div>

## Webserver
To provide an API for accessing audio operations, we've implemented a webserver in Python using Flask.
The reasons behind this architectural choice include faster compute times and slower battery depletion.
As we didn't get to incorporate the AI models into our platform, the backend also includes a POC timbre transfer implementation using fourier transforms.

You can read more about how to setup and run the server in the [*web_server* directory](/web_server).
