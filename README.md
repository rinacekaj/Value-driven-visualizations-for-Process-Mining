# Value-driven-visualizations-for-Process-Mining

The dataset has to b  manually generated CSV-file with the information taken by another plug-in, namely: the activities that exist in the event log, the synchronous moves or the deviations such as moves in the model or in the log.

The dataset contains of 8 attributes:
d - a unique id for each activity,
act - the activity name,
syn - how many moves were executed correctly (synchronous moves),
mm - the moves that were done only in the model,
log - the number of moves that occurred only in the log,
nr - shows how many followers has the activity,
prior - indicates the id of the previous activity for each activity and
post - shows the id of the following activity for each activity

The code firstly finds the first activities in the model, which are the activities that do not have any prior activity. The next step is to find the following activities by using the ids stored at the column post.

In this way, the activities are saved in the order they are executed. The order is turned to positions, so each activity is mapped to one position. This is done by using the dictionary in Python. The key of the dictionary indicates the position while the values of the dictionary contain the ids of the activities that will be executed in that position.

Next, the code follows several steps. After the creation of the dictionary, it places the activities in the correct order in the graphical window and saves the coordinates of the rectangle for each activity. These coordinates will help the code to find where the places should be drawn. In the end, the places will be connected with the arcs.
