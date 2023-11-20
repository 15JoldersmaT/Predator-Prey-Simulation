# Predator-Prey-Simulation
Python script I wrote to showcase reinforcement learning/Genetic algorithms.

The way version 8 works:
There are two predators (cat) and one prey (mouse).

They are initialized with 'brains' that are random values represented in a Numpy array. 

These values (weights) interact with the input values to the brains (their location on the screen, the location of the others, etc.)

The values (weights) of the brain are mutated under these conditions:

If either a cat or mouse is touching the edge of the screen, their brains mutate.
If a cat does not catch a mouse, its brain mutates.
If a mouse is caught by a cat, its brain mutates.

1 - 0 to adjust simulation speed.

![](demo.gif)

(3 mice, to cats in demo, wall mutation on, leaky relu used for activation function, version 8)

Arder Cat version:
expanded number of neurons with hidden layers. Fixed number of cats and mice in this version currently. 

Simulations with more than two cats seem to behave strangely, still debugging. 





