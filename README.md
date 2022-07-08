# COMP90054 AI Planning for Autonomy - Assignment 1 - Search 

You must read fully and carefully the assignment specification and instructions detailed in this file. You are NOT to modify this file in any way.

* **Course:** [COMP90054 AI Planning for Autonomy](https://handbook.unimelb.edu.au/subjects/comp90054) @ Semester 1, 2022
* **Instructor:** Dr. Nir Lipovetzky and Prof. Tim Miller
* **Deadline:** Friday 25th March, 2022 @ 11:59pm (end of Week 4)
* **Course Weight:** 10%
* **Assignment type:**: Individual
* **ILOs covered:** 1, 2, and 3
* **Submission method:** via git tagging (see Submission Instructions below for instructions)

The **aim of this assignment** is to get you acquainted with AI search techniques and how to derive heuristics in Pacman, as well as to understand the Python-based Pacman infrastructure.

 <p align="center"> 
    <img src="logo-p1.jpg" alt="logo project 1">
 </p>

## Your task

You **must build and submit your solution** using the sample code we provide you in this repository, which is different from the original [UC Berlkley code base](https://inst.eecs.berkeley.edu/~cs188/fa18/project1.html). If you want to provide a report with your submission (e.g., reflections, acknowledgments, etc.), please do so in file [REPORT.md](REPORT.md).

* Please remember to complete the [STUDENT.md](STUDENT.md) file with your individual submission details (so we can identify you when it comes time to submit). 

* You should **only work and modify** files [search.py](search.py) and [searchAgents.py](searchAgents.py) in doing your solution. Do not change the other Python files in this distribution.

* Your code **must run _error-free_ on Python 3.6**. Staff will not debug/fix any code. Using a different version will risk your program not running with the Pacman infrastructure or autograder and may risk losing (all) marks. 
   * You can install Python 3.6 from the [official site](https://www.python.org/dev/peps/pep-0494/), or set up a [Conda environment](https://www.freecodecamp.org/news/why-you-need-python-environments-and-how-to-manage-them-with-conda-85f155f4353c/) or an environment with [PIP+virtualenv](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/). 

* Your code **must not have any personal information**, like your student number or your name. That info should go in the [STUDENT.md](STUDENT.md) file, as per instructions above. If you use an IDE that inserts your name, student number, or username, you should disable that.

* **Assignment 1 FAQ** is available to answer common questions you might have about the Assignment 1 on ED at https://edstem.org/au/courses/8178/discussion/716336

* **Getting started on GitHub** - the video below explains how to **clone**, **git add**, **commit** and **push** while developing your solution for this assignment:

[![How to work with github teams](img/loom_video.png)](https://www.loom.com/share/ae7e93ab8bec40be96b638c49081e3d9)



### Practice Task (0 marks)

To familiarize yourself with basic search algorithms and the Pacman environment, it is a good start to implement the tasks at https://inst.eecs.berkeley.edu/~cs188/fa18/project1.html, especially the first four tasks; however, there is no requirement to do so.

You should code your implementations *only* at the locations in the template code indicated by ```***YOUR CODE HERE***``` in files [search.py](search.py) and [searchAgents.py](searchAgents.py), please do not change code at any other locations or in any other files.

### Part 1 (3 marks)

Implement the **Enforced Hill Climbing algorithm** discussed in lectures, using Manhattan Distance as the heuristic, by inserting your code into the template indicated by comment ```***YOUR CODE HERE FOR TASK 1***```, you can view the location at this link: [search.py#L166](search.py#L166).

Note that you don't have to implement Manhattan Distance, as this has already been implemented for you in the template code, although you will need to call the heuristic from inside your search. You should be able to test the algorithm using the following command:

```
python pacman.py -l mediumMaze -p SearchAgent -a fn=ehc,heuristic=manhattanHeuristic
```

Other layouts are available in the layouts directory, and you can easily create you own. The `autograder` will try to validate your solution by looking for the exact output match.

### Part 2 (3 marks)

In this part we will prove that you have all the ingredients to pick up many new search algorithms, tapping to knowledge you acquired in the lectures and tutorials.

**Iterative Deepening A\* (IDA\*)** is a search algorithm that has not been introduced in the lectures but it relies on ingredients which you already know: 
*  **Iterative Deepening**, and 
* the evaluation function <img src="https://latex.codecogs.com/svg.image?f(n)&space;=&space;g(n)&space;&plus;&space;h(n)"/> used by **A\***. 

**IDA\*** is similar to Iterative Deepening, it does a limited depth first search but:
1. instead of initializing the limit <img src="https://latex.codecogs.com/svg.image?l_0=0"/>, it initialises the limit <img src="https://latex.codecogs.com/svg.image?l_0=f(s_0)"/> using the evaluation function of the initial state <img src="https://latex.codecogs.com/svg.image?s_0"/>, and
2. instead of updating the next limit <img src="https://latex.codecogs.com/svg.image?l_{i&plus;1}&space;=&space;l_{i}&space;&plus;&space;1"/> by one, it updates the next limit <img src="https://latex.codecogs.com/svg.image?l_{i&plus;1}"/> by looking at the minimum <img src="https://latex.codecogs.com/svg.image?f"/> value of a node that was pruned by the current limit <img src="https://latex.codecogs.com/svg.image?l_i"/>. Formally, lets define <img src="https://latex.codecogs.com/svg.image?P_i&space;=&space;\{&space;n&space;\&space;|&space;f(n)&space;>&space;l_i&space;\}"/> as the set of nodes pruned by limit <img src="https://latex.codecogs.com/svg.image?l_i"/>, then the update <img src="https://latex.codecogs.com/svg.image?l_{i&plus;1}&space;=&space;\min\limits_{n&space;\in&space;P_i}&space;f(n)"/>, where <img src="https://latex.codecogs.com/svg.image?f(n)&space;=&space;g(n)&space;&plus;&space;h(n)"/> is the same evaluation function as described in **A\***.

This allows IDA* to use the accumulated cost + heuristic  function in order to minimise the number of iterations running the limited depth first search. **IDA\*** is often used to find optimal solutions for memory-constrained problems.

Implement the **Iterative Deepening A\* algorithm** discussed above, using Manhattan Distance as the heuristic, by inserting your code into the template indicated by comment ```***YOUR CODE HERE FOR TASK 2***```, you can view the location at this link: [search.py#L179](search.py#L179). You should be able to test the algorithm using the following command:
```
python pacman.py -l mediumMaze2 -p SearchAgent -a fn=ida,heuristic=manhattanHeuristic
```
For this exercise, you can assume you must **not** check for cycles in the problem. Other layouts are available in the layouts directory, and you can easily create your own. The `autograder` will seek for exact match of the solution and the number node expansions. The successors list are expected to be visited in the original order given by the API. If you implement **IDA\*** using a recursive method, please **reverse** it. An example is given as follows:
```
succs = problem.getSuccessors(state)
succs.reverse()
```

### Part 3 (0 marks)

*This part worths 0 marks. It is now an example how we could generate the heuristics*

This part involves solving a more complicated problem. You will be able to model the problem, using the search algorithm (both Astar, which is provided and Iterative Deepening A* algorithm implemented by yourself in part 2) and design a heuristic function that can guide the search algorithm. 

Just like in Q7 of the Berkerley Pacman framework, you will be required to create an agent that will eat all of the food (dots) in a maze. However, to make it more interesting, the Capsule can provide energy to the Pacman. That is, when the Pacman enters a cell that contains a capsule, it will consume the capsule and gain energy, **causing this move to have 0 cost**. The capsule will disappear after being consumed by a Pacman.

In order to implement this, you should create a new problem called `CapsuleSearchProblem`. Some of the variables are listed in the comments and the initialization. You will need to design a way to represent the states of the problem. You will need to return the initial state through `getStartState` function. You will also need to have `isGoalState` to return true if the given state belongs to one of the goal states. In addition, you will need to implement your Applicability and transition function in `getSuccessors` function, which means to return a list of tuples that contains (`next state`, `action`, `cost`).

You will also need to implement a suitable `capsuleProblemHeuristic`. Your heuristic function needs to be **admissible**. You may choose to implement other helper classes/functions. You should insert your code into the template indicated by the comments ```***YOUR CODE HERE FOR TASK 3***```, you can view the locations at these links: [search.py#L117](search.py#L117) and 4 positions in [searchAgents.py](searchAgents.py).

You should be able to test your program by running the following commands (in one line):

```
python pacman.py -l capsuleSearch -p CapsuleSearchAgent
   -a fn=astar,prob=CapsuleSearchProblem,heuristic=capsuleProblemHeuristic
```

```
python pacman.py -l capsuleSearch -p CapsuleSearchAgent
   -a fn=ida,prob=CapsuleSearchProblem,heuristic=capsuleProblemHeuristic
```

The `autograder` seeks an optimal solution and the number of nodes expended (Please make sure you **do not** remove the code we use to count nodes expansion  in the `getSussessors` function). In addition, please make sure your heuristic is **admissible**, otherwise you might get 0 marks for this part due to either failed to find the optimal plan, or expanding more nodes than our baselines (zero heuristic).

#### Indicative marks IDA*

They are shown below for node expansions with **IDA\*** on the testing files [capsuleIDA1.test](test_cases_assignment1/part3-2/capsuleIDA1.test) and [capsuleIDA2.test](test_cases_assignment1/part3-2/capsuleIDA2.test) which are used by the autograder for checking your submission. Note that we will test your submission on different layouts, however this will give you a good guide for comparing the expected performance of your solution:

| capsuleIDA1 (node expansions)     | Potential Marks | running time | capsuleIDA2 (node expansions) | Potential Marks | running time |
| ----------- | ----------- | ----------- | ----------- |  ----------- |  ----------- |
| <= 515    | 1.00 | 17s  | <= 8458   | 1.00 | 317.9s |
| > 515     | 0.75 | 0.2s | > 8458    | 0.75 | 6s |
| > 1150    | 0.50 | 0.2s | > 30820   | 0.50 | 6.4s |
| > 3754    | 0.25 | 2.5s | > 132449  | 0.25 | 120s |
| >= 55938  | 0.00 |  -   | >= 2429729 | 0.00 |  - |

The runtimes give you a rough idea about how long did it take for the program to run with different sample heuristics we implemented. 

The **timeout** for this part will be **three times** the runtime of the **slowest** heuristic above. Due to the nature of **IDA\***, the program takes significantly longer when the solution length is increased. In addition, the program runtime changes if other layouts are used (different branching) and tie-breaking rules. 


####  Indicative marks A*

They are shown below for node expansions with **A\*** on the testing files [capsuleA1.test](test_cases_assignment1/part3-1/capsuleA1.test) and [capsuleA2.test](test_cases_assignment1/part3-2/capsuleA2.test) which are used by the autograder for checking your submission. Note that we will test your submission on different layouts, however this will give you a good guide for comparing the expected performance of your solution:

| capsuleA1 (node expansions)     | Potential Marks | running time | capsuleA2 (node expansions) | Potential Marks | running time |
| ----------- | ----------- | ----------- | ----------- |  ----------- |  ----------- |
| <= 704    | 1.00 | 146s | <= 648   | 1.00 | 111.5s |
| > 704     | 0.75 | 0.3s | > 648    | 0.75 | 0.5s |
| > 908     | 0.50 | 0.4s | > 1444   | 0.50 | 0.7s |
| > 2980    | 0.25 | 0.6s | > 4194   | 0.25 | 1.0s |
| >= 4688   | 0.00 |  -   | >= 6527   | 0.00 |  - |

The runtime gives you a rough idea about how long did it take for the program to run with the our heuristics. The **timeout** for this part will be **three times**  the runtime of the slowest heuristic above.

You will see in first person the balance between 1) how informed you make your heuristic (it should expand less nodes in general), and 2) the overall runtime. As you can see, sometimes it may be preferable to have a cheaper less informed heuristic, even if you end up expanding more nodes.

### Part 4 (4 marks)

This part involves solving a more complicated problem. You will be able to model the problem, using the search algorithm (both Astar, which is provided and Iterative Deepening A* algorithm implemented by yourself in part 2) and design a heuristic function that can guide the search algorithm. 

Just like in Q7 of the Berkerley Pacman framework, you will be required to create an agent that will eat all of the food (dots) in a maze. However, to make it more interesting, the Capsule is harder to be consumed. That is, when the Pacman enters a cell that contains a capsule, it will consume the capsule with costing more energy, **causing this move to have a cost of 2**. The capsule will disappear after being consumed by a Pacman.

In order to implement this, you should create a new problem called `CapsuleAvoidSearchProblem`. Some of the variables are listed in the comments and the initialization. You will need to design a way to represent the states of the problem. You will need to return the initial state through `getStartState` function. You will also need to have `isGoalState` to return true if the given state belongs to one of the goal states. In addition, you will need to implement your Applicability and transition function in `getSuccessors` function, which means to return a list of tuples that contains (`next state`, `action`, `cost`).

You will also need to implement a suitable `capsuleAvoidProblemHeuristic`. Your heuristic function needs to be **admissible**. You may choose to implement other helper classes/functions. You should insert your code into the template indicated by the comments ```***YOUR CODE HERE FOR TASK 3***```, you can view the locations at these links: [search.py#L117](search.py#L117) and 4 positions in [searchAgents.py](searchAgents.py).

You should be able to test your program by running the following commands (in one line):

```
python pacman.py -l capsuleAvoidA1 -p CapsuleAvoidSearchAgent
   -a fn=astar,prob=CapsuleAvoidSearchProblem,heuristic=capsuleAvoidProblemHeuristic
```

```
python pacman.py -l capsuleAvoidA1 -p CapsuleAvoidSearchAgent
   -a fn=ida,prob=CapsuleAvoidSearchProblem,heuristic=capsuleAvoidProblemHeuristic
```

The `autograder` seeks an optimal solution and the number of nodes expended (Please make sure you **do not** remove the code we use to count nodes expansion  in the `getSussessors` function). In addition, please make sure your heuristic is **admissible**, otherwise you might get 0 marks for this part due to either failed to find the optimal plan, or expanding more nodes than our baselines (zero heuristic).

#### Indicative marks IDA*

They are shown below for node expansions with **IDA\*** on the testing files [capsuleAvoidIDA1.test](test_cases_assignment1/part4-2/capsuleAvoidIDA1.test) and [capsuleAvoidIDA2.test](test_cases_assignment1/part4-2/capsuleAvoidIDA2.test) which are used by the autograder for checking your submission. Note that we will test your submission on different layouts, however this will give you a good guide for comparing the expected performance of your solution:

| capsuleIDA1 (node expansions)     | Potential Marks | running time | capsuleIDA2 (node expansions) | Potential Marks | running time |
| ----------- | ----------- | ----------- | ----------- |  ----------- |  ----------- |
| <= 414     | 1.00 | 6.6s  | <= 8818    | 1.00 | 101s |
| > 414      | 0.75 | 0.7s  | > 8818     | 0.75 | 1.8s |
| > 7300     | 0.50 | 8.6s  | > 21314    | 0.50 | 34.7s |
| > 120317   | 0.25 | 29.8s | > 400872   | 0.25 | 56.7s |
| >= 673473  | 0.00 |  -    | >= 1116517 | 0.00 |  - |

The runtimes give you a rough idea about how long did it take for the program to run with different sample heuristics we implemented. 

The **timeout** for this part will be **three times** the runtime of the **slowest** heuristic above. Due to the nature of **IDA\***, the program takes significantly longer when the solution length is increased. In addition, the program runtime changes if other layouts are used (different branching) and tie-breaking rules. 


####  Indicative marks A*

They are shown below for node expansions with **A\*** on the testing files [capsuleAvoidA1.test](test_cases_assignment1/part4-1/capsuleAvoidA1.test) and [capsuleAvoidA2.test](test_cases_assignment1/part4-2/capsuleAvoidA2.test) which are used by the autograder for checking your submission. Note that we will test your submission on different layouts, however this will give you a good guide for comparing the expected performance of your solution:

| capsuleA1 (node expansions)     | Potential Marks | running time | capsuleA2 (node expansions) | Potential Marks | running time |
| ----------- | ----------- | ----------- | ----------- |  ----------- |  ----------- |
| <= 45    | 1.00 | 1s   | <= 188   | 1.00 | 8s |
| > 45     | 0.75 | 0.1s | > 188    | 0.75 | 0.1s |
| > 68     | 0.50 | 0.1s | > 243    | 0.50 | 0.2s |
| > 349    | 0.25 | 0.2s | > 1034   | 0.25 | 0.5s |
| >= 1890  | 0.00 |  -   | >= 3051  | 0.00 |  - |

The runtime gives you a rough idea about how long did it take for the program to run with the our heuristics. The **timeout** for this part will be **three times**  the runtime of the slowest heuristic above.

You will see in first person the balance between 1) how informed you make your heuristic (it should expand less nodes in general), and 2) the overall runtime. As you can see, sometimes it may be preferable to have a cheaper less informed heuristic, even if you end up expanding more nodes.




## Marking criteria

Marks are allocated according to the task breakdown listed above, based on how many of our tests the algorithms pass. No marks will be given for code formatting, etc. Observe that while the autograder is a useful indication of your performance, it may not represent the ultimate mark. We reserve the right to run more tests, inspect your code and repo manually, and arrange for a face-to-face meeting for a discussion and demo of your solution if needed.  You must **follow good SE practices**, including good use of git during your development such as:

* _Commit early, commit often:_ single or few commits with all the solution or big chucks of it, is not good practice.
* _Use meaningful commit messages:_ as a comment in your code, the message should clearly summarize what the commit is about. Messages like "fix", "work", "commit", "changes" are poor and do not help us understand what was done.
* _Use atomic commits:_ avoid commits doing many things; let alone one commit solving many questions of the project. Each commit should be about one (little but interesting) thing. 

## Checking your submission

Run the following command to run sanity checks using our test files:

```
python ./autograder.py --test-directory=test_cases_assignment1
```

It is important that you are able to run the autograder and have these tests pass, otherwise, our marking scripts will NOT work on your submission.

**NOTE**: You should not change any files other than [search.py](search.py) and [searchAgents.py](searchAgents.py). You should not import any additional libraries into your code. This risks being incompatible with our marking scripts.



## Submission Instructions

This repository serves as a start code for you to carry out your solution for [Project 1 - Search](http://ai.berkeley.edu/search.html) from the set of [UC Pacman Projects](http://ai.berkeley.edu/project_overview.html) and the marked questions. 

**To submit your assignment** you must complete the following **four** steps:

1. Complete the [STUDENT.md](STUDENT.md) file with your details of the submission.
2. Check that your solution runs on Python 3.6 and that your source code does not include personal information, like your student number or name. 
3. Tag the commit version you want to be graded with tag `submission`. 
    * The commit and tagging should be dated before the deadline.
    * Note that a tag is NOT a branch, so do not just create a branch called "submission" as that will not amount to tagging.
4. Fill the [Assignment 1 Certification Form](https://forms.gle/49ir7wwrbb4hCMrN8).
    * Non-certified submissions will **not** be marked and will attract **zero** marks.
    


From this repository, we will copy *only* the files: [search.py](search.py) and [searchAgents.py](searchAgents.py). Please do not change any other file as part of your solution, or it will not run. Breaking these instructions breaks our marking scripts, delays marks being returned, and more importantly, gives us a headache. Submissions not compatible with the instructions in this document will attract zero marks and do not warrant a re-submission. Staff will not debug or fix your submission.

Please view the following to learn how to *Tag* your commit version you want to be graded:

**How to create a Tag using the Command Line**:


[![How to create a Tag the Command Line](img/loom_video.png)](https://www.loom.com/share/17ec72b954454bc89bbe1dbb0bd2874f)

**Another way to create a Tag using the User Interface**:

[![How to create a Tag the User Interface](img/loom_video.png)](https://www.loom.com/share/3cd39e97919e4b688d9841613aba6973)

## Important information

**Corrections:** From time to time, students or staff find errors (e.g., typos, unclear instructions, etc.) in the assignment specification. In that case, corrected version of this file will be produced, announced, and distributed for you to commit and push into your repository.  Because of that, you are NOT to modify this file in any way to avoid conflicts.

**Late submissions & extensions:** A penalty of 10% of the maximum mark per day will apply to late assignments up to a maximum of five days, and 100% penalty thereafter. Extensions will only be permitted in _exceptional_ circumstances; refer to [this question](https://docs.google.com/document/d/17YdTmDC54WHq0uZ-2UX3U8ESwULyBDJSD4SjKCrPXlA/edit?usp=sharing) in the course FAQs. 

**About this repo:** You must ALWAYS keep your fork **private** and **never share it** with anybody in or outside the course, except your teammates, _even after the course is completed_. You are not allowed to make another repository copy outside the provided GitHub Classroom without the written permission of the teaching staff. Please respect the [authors request](http://ai.berkeley.edu/project_instructions.html): 

> **_Please do not distribute or post solutions to any of the projects._**

**Academic Dishonesty:** This is an advanced course, so we expect full professionalism and ethical conduct.  Plagiarism is a serious issue. Please **don't let us down and risk our trust**. The staff take academic misconduct very seriously. Sophisticated _plagiarism detection_ software (e.g., [Codequiry](https://codequiry.com/), [Turinitin](https://www.turnitin.com/), etc.) will be used to check your code against other submissions in the class as well as resources available on the web for logical redundancy. These systems are really smart, so just do not risk it and keep professional. We trust you all to submit your own work only; please don't let us down. If you do, we will pursue the strongest consequences available to us according to the **University Academic Integrity policy**. For more information on this see file [Academic Integrity](ACADEMIC_INTEGRITY.md).

**We are here to help!:** We are here to help you! But we don't know you need help unless you tell us. We expect reasonable effort from you side, but if you get stuck or have doubts, please seek help. We will ran labs to support these projects, so use them! While you have to be careful to not post spoilers in the forum, you can always ask general questions about the techniques that are required to solve the projects. If in doubt whether a questions is appropriate, post a Private post to the instructors.

**Silence Policy:** A silence policy will take effect **48 hours** before this assignment is due. This means that no question about this assignment will be answered, whether it is asked on the newsgroup, by email, or in person. Use the last 48 hours to wrap up and finish your project quietly as well as possible if you have not done so already. Remember it is not mandatory to do all perfect, try to cover as much as possible. By having some silence we reduce anxiety, last minute mistakes, and unreasonable expectations on others. 

Please remember to follow all the submission steps as per assignment specification.

## COMP90054 Code of Honour

We expect every UoM student taking this course to adhere to it **Code of Honour** under which every learner-student should:

* Submit their own original work.
* Do not share answers with others.
* Report suspected violations.
* Engage in any other activities that will dishonestly improve their results or dishonestly improve or damage the results of others.

Unethical behaviour is extremely serious and consequences are painful for everyone. We expect enrolled students/learners to take full **ownership** of your work and **respect** the work of teachers and other students.


**I hope you enjoy the assignment and learn from it**, and if you still **have doubts about the assignment and/or this specification** do not hesitate asking in the [ED discussion Forum](https://edstem.org/au/courses/8178/discussion/) and we will try to address it as quickly as we can!

**GOOD LUCK and HAPPY PACMAN!**

## Acknowledgements

This is [Project 1 - Search](http://ai.berkeley.edu/search.html) from the set of [UC Pacman Projects](http://ai.berkeley.edu/project_overview.html).  We are very grateful to UC Berkeley CS188 for developing and sharing their system with us for teaching and learning purposes.
