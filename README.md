### Multiple Traveling Salesman Problem

#### The problem:
The Multiple Traveling Salesman Problem (mTSP) is a generalization of the Traveling Salesman Problem (TSP) in which more than one salesman is allowed. MTSP involves assigning M salesmen to N cities, and each city must be visited by a salesman while requiring a minimum total cost.

#### Solution:
- Step 1: Find centroid city (the city that has the lowest sum of distances to every other city).
- Step 2: Connect every city to centroid.
- Step 3: Starting from the nearest to the farthest city from centroid, connect each city to the 2 nearest ones to it. The connections between cities MUST NOT insersect other connections.
- Step 4: Divide the number of cities (N) by the number of salesmen (M). Each salesman will travel N / M cities.
 
#### Solution's images:
- ##### Step 1:
![image](https://github.com/Marcos-Godinho-Filho/multiple_travelling_salesman_problem/assets/113946578/5a466535-ca9c-424c-9ca9-412feee0ff76)

- ##### Steps 2 and 3:
![image](https://github.com/Marcos-Godinho-Filho/multiple_travelling_salesman_problem/assets/113946578/d89308fc-f16a-40f3-bbc7-75874a6dcc04)

- ##### Step 4:
![image](https://github.com/Marcos-Godinho-Filho/multiple_travelling_salesman_problem/assets/113946578/9aa83763-c35f-4152-aef2-26188757e196)


#### Results:
| Instância         | N | M | K | Solução (em tese) ótima | Solução encontrada |
| :---------------: | - | - | - | :---------------------: | :----------------: |
| 1 | 13 | 1 | 13 | 3071 | 3013 |
| 2 | 17 | 1 | 17 | 3948 | 4146 |
| 3 | 19 | 1 | 19 | 4218 | 4686 |
| 4 | 32 | 3 | 11 | 5841 | 8378 |
| 5 | 48 | 3 | 16 | 6477 | 9931 |
| 6 | 60 | 3 | 20 | 6786 | 11769 |
| 7 | 72 | 5 | 15 | 8618 | 12447 |
| 8 | 86 | 5 | 17 | 9565 | 15770 |
| 9 | 92 | 5 | 19 | 9586 | 16432 |


#### How to run:
- Create virtual environment:
`python3 -m venv .venv`
- Activate it:
  - For MACOS: `.venv/bin/activate`
  - For Windows: `.venv/Scripts/activate`
- Install dependencies:
`pip install -r requirements.txt`
- Run `main.py`
