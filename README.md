# Portfolio

### Education
- Bachelor of Science, Statistics | Minnesota State University, Mankato (_May 2024_)
  
### Projects
#### Connect 4 Game
[Play Connect 4 Game](https://jakeh766.github.io/portfolio/assets/Connect4/build/web/index.html)

Developed a Connect 4 game using Python and implemented the minimax algorithm with alpha-beta pruning to maximize efficiency. The game has three different levels: Beginner, Intermediate, and Expert. The difference between levels is the depth of moves that the computer looks ahead. For example, a depth of two means that the computer searches and evaluates each possible board state two moves ahead. Below is a table showing the search depth of each level:

| Level | Depth |
| --- | --- |
| Beginner | 2 |
| Intermediate | 4 |
| Expert | 6 |

There are four directions that a player can win in Connect 4: vertical, horizontal, positive-sloped diagonal, and negative-sloped diagonal. If a player gets at least 4 pieces in a row in any of these directions, they win the game. To evaluate a board position, the program segments the board into windows of length 4 (Each window contains 4 holes) in each direction. Then the Connect 4 AI follows a heuristic (rule of thumb) scoring approach on each window that has been fine-tuned by trial and error. In addition to scoring each window, the number of pieces in the center column is also scored. The center column is the most key column on the board because in the center you have the most options to branch out and get 4 in a row. The table below outlines the heuristic scoring approach:

| Condition | Score |
| --- | --- |
| Four in a row | + &infin; |
| Three in a row with one empty spot | + 5 |
| Two in a row with two empty spots | + 2 |
| Opponent has three in a row with one empty spot | - 4 |
| Opponent has two in a row with two empty spots | - 1 |
| Opponent has four in a row | - &infin; |
| Piece in center column | + 3 |
| Opponent piece in center column | - 2 |

The following GIF illustrates how the AI would evaluate this specific position for yellow.

![Scoring](/assets/Connect4/Connect4Scoring.gif)

The following GIF shows how the AI (yellow piece) would pick the optimal move after red starts the game by placing a piece in the center. The circled boards are ones are pruned, meaning that there is no point in evaluating them.



![Minimax](/assets/Connect4/Connect4GIF.gif)




#### MUDAC

#### Capstone Project

#### Data Derby

#### Handwritten Data Processing Application
Created an application for processing and creating reports from handwritten data.

The code and more information can be found here:

[Github repo](https://github.com/Jakeh766/pigmaker-program)

### Work Experience
Tutor | MNSU TRIO Student Support Services | Mankato, MN Oct 2023 – Apr 2024
- Conducted one-on-one tutoring sessions in mathematics and statistics for 10-15 students weekly, primarily
assisting first-generation, disabled, and low-income college students
- Applied diverse teaching methods and visual aids to engage students and enhance learning outcomes
- Developed practice exercises to improve understanding and retention, resulting in positive student feedback

### Volunteering and Leadership
[BEST BOARD Blog Post](https://blog.mnsu.edu/csu/best-board-s24-jake-hauser-leads-march-book-drive-as-a-new-maverick-tradition/)
