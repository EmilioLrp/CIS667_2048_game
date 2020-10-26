# CIS 667 term proj 2048 game

This project aims to implement a variant of 2048 game and later on being played using both a tree search algorithm and a machine learning algorithm.

## Authors

1. Ruipeng LIU (rliu02@syr.edu)
2. Duhao Guo (dguo13@syr.edu)
3. Qi Fang (qfang04@syr.edu)

## System requirements

In order to run this project, please make sure that the hosting machine having a python3 installed and be able to build a virtual environment from it. An OS of mac or linux is preferred yet still be able to run on windows only no guarantee whether the start.sh file works.

## How to run

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
python game.py
```

Note that these operations is executed under the same directory as all the source codes are.

There might be a situation that the dependencies failed to install due to the variance of name and version for the same package on different OS. In that case make sure all the following packages are properly installed before running the project:

1. numpy
2. enum