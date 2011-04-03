# Plex metadata agent for Bierdopje.com

This is a metadata agent for [Plex](http://plexapp.com) fetches Dutch subtitles for TV shows from [Bierdopje.com](http://www.bierdopje.com/).

## Installation

Download the latest package from the downlaods screen: [Bierdopje-0.0.1.plexapp](https://github.com/downloads/jeroenj/bierdopje-plex-agent/Bierdopje-0.0.1.plexapp)

If that doesn't work for some reason or you want to install it manually, you can clone this repository and copy the Bierdopje.bundle to your `~/Library/Application Support/Plex Media Server/Plug-ins` folder.

## Todo
* Figure out a way to download alternative subtitles if an exact filename match is not found:
  * Download the most popular one
  * Download all of them (which would mean that you have multiple Dutch subtitles in Plex)
  * Preferably the user should choose one
* Avoid putting the API key in plex config for subtitles location

## Bugs

Please report them on the [Github issue tracker](https://github.com/jeroenj/bierdopje-plex-agent/issues)
for this project.

If you have a bug to report, please include the following information:

* **Version information for bierdopje, Rails and Ruby.**
* Stack trace and error message.

Logs can be found in the `~/Library/Logs/PMS Plugin Logs/com.plexapp.agents.bierdopje.log` files.

You may also fork this project on Github and create a pull request.

Copyright (c) 2011, released under the MIT license.
