# Post Manager
![ICO](pm_ico.png)

This is a app to save posts and can do login/register users. this app is written in `python` and its configable.
## Features
- simple
- easy to use
- open source
- free
- no need database
- configable
- fixed xss

## How to use
- just run `python3 server.py` in terminal and you can see the server is running.
to go to the website, just open your browser and type `http://localhost:{post that you selected in cofig.json}/`

## Installation
- clone the project in your computer
- go to the project folder
- run `python3 server.py` in terminal
- you can see the server is running
## Config
there is a file named `config.json` in the project folder. you can change the config in this file.
The default config (If you want to change the config back to normal):
```json
{
    "port": "8080",
    "debug": true
}
```
so, the `port` is for port of the project, the default is `8080`, you can change it to any port you want. second, we got the debug, because this is a test server, do not edit this part but if you want to use this project in public server, use `serv` insted of `app.run` because if you use it, it makes the app not in debug mode. the app will be more configable so that you can change the frameworks of the app and the url for pages.
## License
License for this project is [`Appache-2.0`](license) license.

## Contributing
- if you want to contribute, you can fork this project and make a pull request.
- there is just 2 rules:
- - don't use any third-party library
- - don't copy and paste the code

## Contact
- if you have any question, you can contact me at [@ghalbeyou](https://github.com/Ghalbeyou/) ! I hope this project will be useful for you.