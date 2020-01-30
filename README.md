# GoTo School 2017

These files were created by me while I was taking courses at GoTo School.

## Images

There are two programs for image processing in this folder. One of them adds red filter to the image, another one makes image black and white. The folder also contains an example file called `ironman.jpg`.

### Requirements

- PIL

## Faces

It's another program for image processing with more functions than the previous one. It lets user choose one of five filters and can also replace all faces on a picture with matching emojis. It uses [Microsoft Azure](https://azure.microsoft.com/ru-ru/services/cognitive-services/face/) service for emotions recognition.

### Requirements

- PIL
- requests

## Music

There are two sound processing programs in this directory. One of them (`sound_music.py`) recieves a sound file and outputs its high-pitched and reversed version. Another one (`sound_voice.py`) records user's voice, increases its speed by 25% and adds background music.

### Requirements

- wave

## Events

It was supposed to be a site with some upcoming events (as an example I used three films that were about to have a premiere in Russia at the moment I was creating this site) where people would be able to sign up for these events. It was my first site that used a database ([MongoDB](https://www.mongodb.com/)). Web application is based on [Tornado](https://www.tornadoweb.org/en/stable/). Later I created dockerfile for this site.

### Requirements

- pymongo
- tornado

## Telegram bot

This is a simple telegram bot that can replace faces on image with emojis (using program from `faces`), execute Python code, send spam messages if user asks to do it and until they send stop command.

### Requirements
- telebot
- requests
- PIL
