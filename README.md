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
- Accuracy: %% (tests table here)
