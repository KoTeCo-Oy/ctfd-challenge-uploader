# CTFd challenge uploader

## Setup

Clone the repo 

    git clone git@github.com:KoTeCo-Oy/ctfd-challenge-uploader.git

Install packages

    pip install -r requirements.txt

Create file `.env.local` and add following two variables

    CTFD_ACCESS_TOKEN=TOKEN
    CTFD_URL=https://your.ctfd.address


## Challenge file format

Syntax is following

```
* Flag rewarded for opening PDF
  * Challenge name: Hello world challenge
  * Description: Can you find your first flag?
  * Category: Category
  * Flag: CTF{H3llO_wOrlD}
```

This will be parsed to following entry

```
{
    "name": "Hello world challenge",
    "description": "Can you find your first flag?",
    "flag": "CTF{H3llO_wOrlD}"
    "category": "Category"
}
```

You can have other "fields" described too, they will be ignored (for now). So if you want to write solving steps for the flag you can write it as following 

```
* Flag rewarded for opening PDF
  * Challenge name: Hello world challenge
  * Description: Can you find your first flag?
  * Category: Category
  * Flag: CTF{H3llO_wOrlD}
  * How to solve:
    * Open PDF
    * Go to page 47
```

## Send to CTFd

Once you are ready to sync flags to CTFd, just run the following command.

**NOTE**: The script will remove existing flags if the name doesn't match!

     python challenges ../ctf_challenge.md

## TODO

- [ ] Some specs would be nice
- [ ] Publish as package to avoid git cloning
- [ ] Set points win the md (now uses 1 as default)