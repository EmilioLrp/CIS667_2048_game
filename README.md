# CIS 667 Term Project: 2048 Game

The project implemented an advanced version of classical game 2048 with tree search and machine learning algorithm.
Specifically, it has the following modifications:
* **Game Mode**: Game players are allowed to swipe horizontally, vertically, and diagonally.
* **Board Size**: The game board is 4x4 by default, and can be enlarged up to 50×50. The larger the game board is, the larger the game goal is. `game goal = 2 ^ (game size + 7)`


## Contributors

* [Ruipeng LIU](https://github.com/EmilioLrp) (rliu02@syr.edu)
* [Duhao Guo](https://github.com/frankgx97) (dguo13@syr.edu)
* [Qi Fang](https://github.com/mllejuly) (qfang04@syr.edu)



## System Requirements

In order to run this project, please make sure that the hosting machine having a python3 installed and be able to build a virtual environment from it. An OS of mac or linux is preferred. Yet it still can be able to run on windows only no guarantee whether the start.sh file works.
alre


## Environment Installation

It is highly recommend running this code under a virtual environment so that this project's dependencies may not contaminating other system dependencies.

If the host machine supports bash, after downloading and unzipping the source code, run the following command:

```
sh start.sh
```

This command is going to automatically create a virtualenv and install all the dependencies needed for this project for you under the same directory where the script locates. If there is already a virtual environment named `/venv`  exists, then the script will update the dependencies and execute the code.

If that does not work for you, a sample manual setup can be seen as follows:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Note that these operations is executed under the same directory as all the source codes are.

There might be a situation that the dependencies failed to install due to the variance of name and version for the same package on different OS. In that case make sure all the following packages are properly installed before running the project:

* numpy
* enum



## Getting Started
```
python game.py
```
