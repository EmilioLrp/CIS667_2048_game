# CIS 667 Term Project: 2048 Game

The project implemented an advanced version of classical game 2048 with tree search and machine learning algorithm.
Specifically, it has the following modifications:
* **Moves**: Game players are allowed to swipe horizontally, vertically, and diagonally. Using the `3 * 3` number keyboard as follows, to map the moving direction to action input. For example, press 8 to move up.
	
	7, 8, 9\
	4, \_, 6\
	1, 2, 3
	
* **Game Mode**: There are in total 4 modes for user to choose. All auto play modes (or except the only manual mode) requires player to press `Enter` to continue to the next move.
	* **human**: In this mode the player is able to play the game manually. This mode is the only mode that allows the player to play manually. Input a move and press `Enter` to perform the action.
	* **baseline**: In this mode a universal random selection is adopt to perform the auto play.
	* **tree**: A MCTS is adopt to perform the auto play.
	* **tree-nn**: A trained neural network on top of the MCTS is used.

* **Game instances**: 5 predefined game instance is defined for player to choose. 
	* size: `3*3`, goal: `128`
    * size: `3*3`, goal: `256`
    * size: `4*4`, goal: `512`
    * size: `4*4`, goal: `1024`
    * size: `4*4`, goal: `2048`


## Contributors

* [Ruipeng LIU](https://github.com/EmilioLrp) (rliu02@syr.edu)
* [Duhao Guo](https://github.com/frankgx97) (dguo13@syr.edu)
* [Qi Fang](https://github.com/mllejuly) (qfang04@syr.edu)



## System Requirements

In order to run this project, please make sure that the hosting machine having a python3 installed and be able to build a virtual environment from it. An OS of mac or linux is preferred. Yet it still can be able to run on windows only no guarantee whether the start.sh file works.
alre


## Environment Installation & Execution

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
python main.py
```

Note that these operations is executed under the same directory as the starting shell is located.

There might be a situation that the dependencies failed to install due to the variance of name and version for the same package on different OS. In that case make sure all the following packages are properly installed before running the project:

* numpy
* enum
* torch

## NN module
### Training nn model
The data for training the neural network is stored in

`/dir_to_project/data/`

Make sure the data is there before training.

The data provided is used to train the provided 5 game instances, any change on the game instance will result in the requirement of modifying the source code.

Training data can be genenerated by running the `training_data_generator.py`, this script will generate training data from MCTS.

### Loading nn model
There are in total 3 different trained neural network models in this project. Before executing the tree-nn option, make sure that the model is correctly loaded in the following directory:

`/dir_to_project/model/{name of the model that you wish to load}/`

The name of the model will provided with three choices corresponding to 3 contributors of this project:

* rliu02
* dguo13
* qfang04


