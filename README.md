# Evolutionary-Computation-Algorithms


## Project Overview

This project is a collection of Evolutionary Computation Algorithms, including:

* ### Genetic Algorithm:
    * Simulates a genetic algorithm with all its core concepts.
    * Applies it to a **Tetris** GUI game built with **Pygame**, allowing for simultaneous multi-agent training.
    * Generates a log file with resulting generations and trained weights.
    * Uses **Seaborn** to visualize the performance of the top 2 chromosomes during training.
    * Includes a **report** explaining the algorithm and results.
    * Provides a **presentation** for further explanation.
* ### Swarm Algorithm:
    * Simulates Ant Colony Optimization (ACO) with all its key concepts.
    * Applies it to solve the **Travelling Salesman Problem**.
    * Creates videos using **Manim** to visualize ant movement, travel cycles, and pheromone values.
    * Includes a **report** explaining the algorithm and results.
    * Provides a **presentation** for further explanation.

## Installation
1- Open your terminal or command prompt.

2- Navigate to the directory where you want to create the virtual environment. You can use the cd command to change directories.

3- Enter the following command to create a virtual environment named projectenv.
You can name it anything you like, but projectenv is used as an example here.
```sh
python -m venv projectenv && cd projectenv
```

This will create a new directory named **projectenv** in your current directory, which will contain the virtual environment.

4- Activate the virtual environment through: ```Scripts\activate```  
> Note: If it didn't work enter this instead: ```source Scripts\activate```

You should now see (**projectenv**) at the beginning of your command prompt, indicating that the virtual environment is active.

> To deactivate the virtual environment, simply enter the command `deactivate` in the terminal.

5- After activating the virtual environment, you can install the required packages using the following command:
```sh
pip install -r requirements.txt

```
6- After installing the required packages, you can run the project using the following command:
```sh
python -u main.py
```
## **Optional** installation to run manim
1- You can follow the Manim installation from the [documentation](https://docs.manim.community/en/stable/installation.html) but we will walk through it together.
2- Install FFMPEG, in windows u can do that using:
```
winget install ffmpeg
```
3- Install [MiKTeX](https://miktex.org/download) or in console using the command: 
```
winget install MiKTeX.MiKTeX
```
4- Now go to the Ant_Colony directory and run the following command:
```
manim visualizer.py AntColonyVisualizer -pqm
```
> Warning: The video will take time to render depending on the number of Cities, Iterations, and Ants

## Usage

This project is designed to be a user-friendly resource for learning Evolutionary Computation Algorithms (ECA). It provides:

* **Executable Code:** Run the included projects to see ECA algorithms in action.
* **Clear Documentation:** Understand the concepts behind each algorithm through the provided reports.
* **Interactive Environment:** Experiment with the code for hands-on learning.

Feel free to explore and modify the code examples to deepen your understanding of ECAs.


## License

This project is licensed under the terms of the Apache License 2.0. For more details, see the [LICENSE](./LICENSE) file in the root directory of this project.
