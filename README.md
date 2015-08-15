# rhythmbox-plugins
my plugins for rhythmbox

# Only Toolbar

![only-toolbar action](https://github.com/fraoustin/rhythmbox-plugins/blob/master/only-toolbar/images/onlytoolbar.png)



# Remember The Rhythm

A plugin for rhythbox to remember last playing song and playback time.
The remember-the-rhythm plugin is a copy of https://github.com/owais/remember-the-rhythm/
with a python3 loader



# Installation

```

    git clone https://github.com/fraoustin/rhythmbox-plugins.git
    cd rhythmbox-plugin
    python install.py only-toolbar
    python install.py remember-the-rhythm
```

# Error

If you have error "no import gi":

* apt-get install python3-gi
* check python3 (/usr/bin/python3) by command "import gi"
