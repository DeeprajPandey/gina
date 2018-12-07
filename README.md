# Gina
#### *isi ka naam hai*

Gina is a bot in the most rudimentary form who is trying to use her knowledge in English to learn a new language that *you* know that *you* are going to teach her.
How? Fret not. She is going to guide you throughout.

There are two parts to the program. In the first part, she gives you a series of simple sentences in English which you have to translate into a language of your choice. She assumes you are correct and based on your inputs, she will display a bunch of syntax rules of the language you used. She knows that languages are vast and complicated and they often do not follow rigid rules which is why you might notice some discrepancies here and there but that is still rare.

The second part of the program is more specific. Using the base register of English as a point of reference, she learns verbs, nouns, adjectives, and adpositions. She begins with an initial state of the Hindi lexicon in each of these syntactic categories, and given an English word and its translation, she learns the unfamiliar words and keeps building her lexicon.

Gina uses the Cloud Natural Language API by Google for syntax analysis of the English sentences she encounters.

## Setup

### Authentication
Gina is still under development. You would need to setup credentials from an NLP API enabled account on GCP to get Gina up and running on your device.

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
For generating syntax rules for any language, Gina will give you a paragraph to translate. Do this very literally, without taking any meaning away from the sentences and she will show the syntax rules for the language you are translating into.
```sh
  $ python interface.py
```

### To Do (Early 2019)
- [ ] Build a web interface for Gina
- [ ] Move to a database

### License
CC BY-NC 4.0 International
