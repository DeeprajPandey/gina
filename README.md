# Gina
#### *isi ka naam hai*
  
Gina is a bot in the most rudimentary form who is trying to use her knowledge in English to learna new language that *you* know that *you* are going to teach her.
How? Fret not. She is going to guide you throughout.

Gina uses Google Natural Language API for syntax analysis. She tries to extrapolate her reasoning from how she learned English to the new language (which could be completely imaginary, as long as you set and follow the basic rules of a language).

## Setup
---

### Authentication
Gina is still under development. You would need to setup credentials from your Google Cloud Platform to run the scripts.

### Install Dependencies
1. Install [pip](https://pip.pypa.io) and [virtualenv](https://virtualenv.pypa.io/)

2. Create a virtualenv and activate it
> ```sh
> $ virtualenv --python python3 env
> $ source env/bin/activate
> ```
If you're on Windows, you may have to specify the full path to your python installation directory
> ```sh
> $ virtualenv --python "c:\python36\python.exe" env
> $ .\env\Scripts\activate
> ```
3. Install the dependencies required by Gina
> ```sh
> $ pip install -r requirements.txt
> ```

### Run
Gina will give you a paragraph to translate. Do this very literally, without taking any meaning away from the sentences and she will show the syntax rules for the language you are translating into.
```sh
  $ python generate_rules.py
```

```sh
  $ python interface.py
```

### License
MIT
