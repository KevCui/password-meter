# Passmeter

> A password meter evaluates the strength of passwords.

## Table of Contents

- [Features](#features)
- [Dependency](#dependency)
- [Usage](#usage)
  - [Example](#example)
- [Credits](#credits)

## Features

- Offline, no worry about your password collected by certain evil web service
- Simple and colorful output for better result analysis
- Flexible to adjust password rules/requirements in script
- Easy to be integrated into any CI processes because of CLI script

## Dependency

- [Rich](https://github.com/willmcgugan/rich)

```bash
~$ pip install rich
```

## Usage

```
usage: passmeter.py [-h] [-p PASSWORD] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -p PASSWORD, --password PASSWORD
                        Password
  -s, --score-only      Only show score number as output
```

### Example

```bash
~$ ./passmeter.py -p password
Very Weak
Score: 8%
Complexity: Very Weak
+--------------------------------------------------------------+
|                               | Rate         | Count | Bonus |
|-------------------------------+--------------+-------+-------|
| Number of Characters          | +(n*4)       |     8 |   +32 |
| Uppercase Letters             | +((len-n)*2) |     0 |     0 |
| Lowercase Letters             | +((len-n)*2) |     8 |     0 |
| Numbers                       | +(n*4)       |     0 |     0 |
| Symbols                       | +(n*6)       |     0 |     0 |
| Middle Numbers of Symbols     | +(n*2)       |     0 |     0 |
| Requirements                  | +(n*2)       |     2 |     0 |
| Letters Only                  | -n           |     8 |    -8 |
| Numbers Only                  | -n           |     0 |     0 |
| Repeat Characters             | -?           |     2 |    -2 |
| Consecutive Uppercase Letters | -(n*2)       |     0 |     0 |
| Consecutive Lowercase Letters | -(n*2)       |     7 |   -14 |
| Consecutive Numbers           | -(n*2)       |     0 |     0 |
| Sequential Letters (3+)       | -(n*3)       |     0 |     0 |
| Sequential Numbers (3+)       | -(n*3)       |     0 |     0 |
| Sequential Symbols (3+)       | -(n*3)       |     0 |     0 |
+--------------------------------------------------------------+
```

Although `-p` exists as an option, it's recommended to avoid using it with your real password. The reason is that Shell commands including all paraders are logged in Shell command execution history, which might cause the trouble to expose your real password. Instead, run `./passmeter.py` and enter password in prompt:

```bash
~$ ./passmeter.py
Password:
```

## Credits

The original code of this project is ported from web app [Password Meter](http://www.passwordmeter.com/)
