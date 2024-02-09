---
title: Larvae Counter
emoji: 📚
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# Larvae Counter

Welcome to the Larvae Counter repo! This web-app utilizes several computer vision techniques to
automate mosquito larvae and pupae counting tasks in a lab setting. To get started visit
the web-app [here](https://lilferrit.github.io/larvaecount/).

## About

The Larvae Counter web-app is implemented purely in python. Most image processing is done using
the [OpenCV](https://opencv.org/) library and the web-ui is written using Plotly's
[Dash](https://dash.plotly.com/) library. The web-app is currently hosted on Huggingface
[here](https://huggingface.co/spaces/lilferrit/larvae-counter).

## Running Locally

To run the larvae counter app locally first clone the repo. Next, navigate to the repo folder using:

```
cd larvaecount
```

or your system's equivalent. Next, install the project dependencies (you may choose
to so in a virtual environment):

```
pip install -r requirements.txt
```

Then install the larvaecount package itself:

```
pip install .
```

to run the web app run

```
python3 -m larvaecount.app --debug=<True/False> --port="<port>" --host="<host-addr>"
```

Note: The debug, port, and host arguments are optional and default to `False`, `8080` and
`127.0.0.1` respectively.

## Using the CLI

All of the counting methods are also available via the command line. To run the CLI run the
command:

```
python3 -m larvaecount.cli <counting_method> <args>
```

The command line arguments are passed directly to the functions in 
[larvaecount/cli.py](larvaecount/cli.py) using the 
[python-fire](https://github.com/google/python-fire) library. See 
[larvaecount/cli.py](larvaecount/cli.py) for usage instructions.

## License

This project uses the MIT license, see [license.txt](license.txt)