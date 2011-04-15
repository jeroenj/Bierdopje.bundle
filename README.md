# Plex metadata agent for Bierdopje.com

This is a metadata agent for [Plex](http://plexapp.com) fetches Dutch subtitles for TV shows from [Bierdopje.com](http://www.bierdopje.com/).

## Features

* It is capable of downloading Dutch, English or both subtitles
* It has smart recognition built it: it wil match all available results on bierdopje if no exact match is found. From those mathes it will fetch the closest match. This is based on various criteria like "HDTV", "DVDRiP", "720p", etc.
* It gives you the option to download the most popular (most downloaded) subtitle if no other matches are found. This might be handy if files are renamed and do not include any release details.
* It allows you to set your own [Bierdopje.com](http://www.bierdopje.com/) API key. This might come in handy if there are any problems with the default API key.

## Installation

Download the latest package from the downlaods screen: [Bierdopje-0.0.4.plexapp](https://github.com/downloads/jeroenj/bierdopje-plex-agent/Bierdopje-0.0.4.plexapp)

If that doesn't work for some reason or you want to install it manually, you can clone this repository and copy the Bierdopje.bundle to your `~/Library/Application Support/Plex Media Server/Plug-ins` folder.

## Todo

This can be found on the [Github issue tracker](https://github.com/jeroenj/bierdopje-plex-agent/issues).

## Troubleshooting

If you are encoutering problems, the first location to see what's wrong are the logs. You can finde them (on a Mac) in the Console.app. They are listed in the PMS Plugin Logs section.

It might be possible that the default API key is not working anymore. If you want to set up your own, you can register one on [Bierdopje.com](http://www.bierdopje.com/) and enter it in the plugin's preferences.

## Bugs

Please report them on the [Github issue tracker](https://github.com/jeroenj/bierdopje-plex-agent/issues)
for this project.

If you have a bug to report, please include the following information:

* **Version information for bierdopje, Rails and Ruby.**
* Stack trace and error message.

Logs can be found in the `~/Library/Logs/PMS Plugin Logs/com.plexapp.agents.bierdopje.log` files.

You may also fork this project on Github and create a pull request.

Copyright (c) 2011, released under the MIT license.
