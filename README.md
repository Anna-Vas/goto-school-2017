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

## Bots

There are some specific programs in this directory that were created for a bot fight at GoTo school. They were used inside a particular infrastructure and that's why all programs in this directory contain functions only.

At every step program gets three parameters: `x` and `y` are current coords and `field` is a list of all rows and columns with information about bots at every spot and their health points. If there is no bot at some spot, it's `field[x][y]` will be `0`. Othrewise, it'll be equal to health points amount of this bot.

There are 8 possible actions at each step: `go_up`, `go_down`, `go right`, `go_left` (bot moves one spot in given direction), `fire_up`, `fire_down`, `fire_right` and `fire_left` (bot starts shooting in given directions; if there's another bot in this direction, he starts losing one health point per step). If bot tries to move or shoot to the wall (for example, it's in the up left corner and tries to move or shoot up or right), nothing happens.

If bot loses all health points, it dies (loses ability to move and shoot). In case of some error in program, bot crashes which is basically similar to death. Bots get score for damaging and killing other bots and lose some score (but not all) in case of death or crash.

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
