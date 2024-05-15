# Logitycoon Automation

> automate repetitive tasks in the game of [logitycoon](http://logitycoon.com/)

[![Release][release-url]][release-url]

![Static Badge](https://img.shields.io/badge/state-under_construction-orange)  
Please note that the tool is still in active development and some features may be yet undocummented.

## About

This tool aims to automate as much manual work as possible in the game "Logitycoon".

- Select the best routes, assign trucks, trailers and employees.
- Take care of employee needs (sleep, sickness etc.).
- Manage company finances (keep as much money on the savings account at any time).
- Send you daily overview report.

## Installation

Windows - python - run from source:

```sh
git clone "https://github.com/JakubDotPy/logitycoon_automation"
cd logitycoon_automation
python -m venv venv
venv/Scripts/activate
python main.py
```

## Usage example

- Clone the tool from this repo.
- Log in the game in a browser.
- Copy the cookie string into a file named `.env_secret` in a format `LT_COOKIE=jointhedarksidewehavecookies`.
- Run the tool using docker or python.

## Release History

* 0.0.1 - _NO RELEASE_
  * Work in progress

## Meta

Jakub Červinka – [@JakubDotPy](https://twitter.com/jakubdotpy) – cervinka.jakub.1989@gmail.com

## Contributing

1. Fork it (<https://github.com/JakubDotPy/logitycoon_automation>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->

[release-url]: https://img.shields.io/github/v/release/jakubdotpy/logitycoon-automation?style=flat-square
