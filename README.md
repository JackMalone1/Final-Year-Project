# **4th year Project Documents**
*This is a github Repo to store the different documents that I have for my final year project.*
---
## **Project Outline**
My project is based on the *Monte-Carlo Tree Search* which was used as part of Alpha-Go to be able to play the game of go.

## Gym Go SetUp Outline ##
- run an anaconda command prompt and dc into the GymGo folder
- Run the commands: 
	conda create -n tensorflow python=3.7
	conda activate tensorflow
	conda install python=3.6.5
	pip install tensorflow==2.2.0
	pip install gym
	pip install matplotlib
	pip install sklearn
	pip install -e .
- Run any other pip isntall commands for any other libraries that you need to run the code
- If you want to see the deep q learning model learn run the command:
	python training.py
- If you want to see the deep q learning model play run the command:
	python model_playing.py
- If you want to test out the proximal policy optimisation code run the command:
	python proximal_policy_optimisation.py
  This will allow the model to learn as well as play against a player