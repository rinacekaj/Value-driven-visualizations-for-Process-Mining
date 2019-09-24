import pandas as pd 
#Import Graphis.py for the visualization
from graphics import *
win = GraphWin('Conformance Checking', 1000, 400) #title and dimensions
win.setBackground("white")

#load data
data = pd.read_csv("C:/Users/Admin/Desktop/real code/BPIChallenge12.csv",sep = ",",quotechar="'")
data['post'] = [1],[2,3],[5,6],[4],[5,6],[''],['']
data['prior'] = '',0,1,1,3,[2,4],[2,4]
data['total'] = 935,4085,0,239,239,655,0




#calculate the maximum of the total activities
actvityWithTotal = data[['act','total']]
maxTotalActivity = actvityWithTotal['total'].max()
print(maxTotalActivity)




#color function for the transitions and places
def color(transition,cc,colorIntesityPercentage):
    if colorIntesityPercentage > 0 and colorIntesityPercentage <=0.1:
        transition.setFill(color_rgb(192,243,255))
        transition.setOutline(color_rgb(192,243,255))
        cc.setFill(color_rgb(255,255,204))
        cc.setOutline(color_rgb(255,255,204))
    elif colorIntesityPercentage >0.1 and colorIntesityPercentage<=0.4:
        transition.setFill(color_rgb(166,238,255))
        transition.setOutline(color_rgb(166,238,255))
        cc.setFill(color_rgb(255,255,153))
        cc.setOutline(color_rgb(255,255,153))
    elif colorIntesityPercentage > 0.4 and colorIntesityPercentage <= 0.7:
        transition.setFill(color_rgb(7,206,255))
        transition.setOutline(color_rgb(7,206,255))
        cc.setFill(color_rgb(255,255,102))
        cc.setOutline(color_rgb(255,255,102))
    elif colorIntesityPercentage > 0.7 and colorIntesityPercentage <= 1: 
        transition.setFill(color_rgb(5,183,228))
        transition.setOutline(color_rgb(5,183,228))
        cc.setFill(color_rgb(255,255,0))
        cc.setOutline(color_rgb(255,255,0))

#define the width of the arrows      
def arrow(arr,colorIntesityPercentage):
    if colorIntesityPercentage >= 0.01 and colorIntesityPercentage <=0.1:
        arr.setWidth(0.3) 
    elif colorIntesityPercentage >0.1 and colorIntesityPercentage<=0.4:
        arr.setWidth(1.2) 
    elif colorIntesityPercentage > 0.4 and colorIntesityPercentage <= 0.7:
        arr.setWidth(2)
    elif colorIntesityPercentage > 0.7 and colorIntesityPercentage <= 1: 
        arr.setWidth(3)
                    
                    
                    
##################### Find the FIRST ACTIVITY #####################
#dictionary
global d
d ={}
#key of the dictionary
global k
k = 0

first = pd.DataFrame()

for row in range(0,len(data)-1):
    #find the activity that has no prior
    if data['prior'][row] == '':
        first = first.append(data[data['id'][:] == row])
        first = first.reset_index(drop=True) 
        
        #save the id of this activity in the position 0 in the dictionary
        if len(first) == 1:
              v = first['id'][0]
        elif len(first) > 1: 
            v = []
            for e in range(0, len(first)):
                v.append(first['id'][e])
        d.update({k: v})
        
##################### DICTIONARY which maps each activity a position #####################
def findlevels(first):
    global d
    v=[]
    global post
    global k
    post = pd.DataFrame()
    
    for row in range(0,len(first)):
        
        #find the follower of the first activity 
        #when the first activity has only one follower
        if first['nr'][row] == 1:
            post = post.append(data[data['id'][:] == first['post'][row][0]])
            post = post.reset_index(drop=True)
       
        #when first activity has more than one follower
        elif first['nr'][row] > 1:
            #go through the list of the follower
            for a in range(0, first['nr'][row]):
                sup = data[data['id'][:]==first['post'].str[a][row]]
                post =  post.append(sup)
                post = post.reset_index(drop=True)
                
    if len(post) != 0:
        #if there is only one follower
        if len(post) == 1:
            #get the id of the follower
            v = post['id'][0]
            
        #more then one follower
        elif len(post) > 1: 
            v = []
            for e in range(0, len(post)):
                v.append(post['id'][e])
                
        #define the key of the dictionary
        k = k+1
        #add the positions including key and the values(activities) to the dictionary 
        d.update({k: v})
    
    #the fuction will be called for the followers saved in the dataframe post
    if len(post) != 0:
        findlevels(post)
        
        
#the function start with the first activity
# and it goes till the end of the dataset
findlevels(first)


#The dictionary d contains the positions and each activity mapped to the corresponding position 
#It is possible that an activity comes more than once in a position thats they have to be removed 
#the activity will be left at the highest position. So if it is repeated before it will be deleted
for i in range(len(d)-1,-1,-1):
    if type(d[i])!= list:
        d[i] = [d[i]]

for i in range(len(d)-1,-1,-1):
    d[i]=list(set(d[i]))
    for e in range(0,len(d[i])):
        if i != 0:
            for k in range(0, len(d[i-1])):
                if d[i][e] == d[i-1][k]:
                    d[i-1][k]=''











#####################  DRAWING EACH ACTIVITY IN THE CORRESPONDING POSITION #####################

#create columns for the the coordinates of the rectangle                    
data['x1'] = 0
data['x2'] = 0
data['y1'] = 0
data['y2'] = 0


#the loop goes through each position to find which activity is within
for position in range(0,len(d)):

    if len(d[position]) == 1: 
        #the y value when the rectangle starts
        a=182
        #the y value when the rectangle ends
        b=232
        
        #y1 = a1 + (n-1)d 
        #180 (d)defines the difference between the activities of a position to the next posititon
        #100 is the starting point of the rectangle
        #position is the following place
        x1 = 100 + position*180
        #160 the end point of rectangle (x value)
        x2 = 160 + position*180
           
        #takes the id of the activity in that position 
        id = d[position][0]
        #Save the coordinates in the dataset
        data['x1'][id] = x1
        data['x2'][id] = x2
        data['y1'][id] = a
        data['y2'][id] = b

         
        #loads the information that needs to be shown in the visualization
        #activity name
        actName = data['act'][id]
        #synchronous moves
        syn = data['syn'][id]
        #model moves
        mm = data['mm'][id]
        #total moves
        total = data['total'][id]
        
        #calculates the percentage that is needed for the color and arrow function
        colorIntesityPercentage = total/maxTotalActivity
        
        
        
        #draws the activity
        transition = Rectangle(Point(x1, a), Point(x2, b))
        transition.draw(win)
        
        #in case of a silent transition(tau) the fill will be black
        if actName == 'TAU' and syn == 0 and mm == 0:
            transition.setFill('black')
            transition.setOutline('black')

        ######Calculates the coordinates for the rectangle that shows the deviations (conformance checking)
        #the height of this rectangle is calculated the normal height of the rectangle blue 
        #multiplied with the percentage of the moves in the model divided by the total number of that activity 
        percentage = mm/total
        height = b-a
        fute = height * percentage
        
        #draws the rectangle that shows the deviations
        cc = Rectangle(Point(x1, a), Point(x2, a+fute))
        #this rectangle exists only if the moves in the model are greater than 0
        if mm != 0:
            cc.draw(win)
        color(transition,cc,colorIntesityPercentage)

        #Defines the size and the position where the activity name and moves will be shown.
        act_name  = Text(Point(x1+27, a+6), actName )
        act_name.setSize(5)
        act_name.draw(win)
        
        if mm == 0:
           syn_moves_nr = Text(Point(x1+45, a+ 16), syn)
           syn_moves_nr.setSize(6)
           syn_moves_nr.draw(win)
        elif syn == 0: 
           model_moves_nr = Text(Point(x1+45, a+ 16), mm)
           model_moves_nr.setSize(6)
           model_moves_nr.draw(win)
        else:
           model_moves_nr = Text(Point(x1+45, a+ fute - 5), mm)
           model_moves_nr.setSize(6)
           model_moves_nr.draw(win)
           syn_moves_nr = Text(Point(x1+45, a+fute+6), syn)
           syn_moves_nr.setSize(6)
           syn_moves_nr.draw(win)

    #if there are more than one activity in a position        
    else:
        for e in range(0, len(d[position])):
            #takes the id of each activity
            id = d[position][e]
            
            #if the id has modulus equal to 0 will have a position over the previous rectangle 
            if e % 2 == 0 and d[position][0] != '':
                
                a=120
                b=170
                
                x1 = 100 + position*180
                y1 = a - e*65
                x2 = 160 + position*180
                y2 = b - e*65
                
                #save the coordinates in the dataset
                data['x1'][id] = x1
                data['y1'][id] = y1
                data['x2'][id] = x2
                data['y2'][id] = y2

                #load activity name, synchronous moves and model moves
                actName = data['act'][id]
                syn = data['syn'][id]
                mm = data['mm'][id]
                total = data['total'][id]
                
                #it is used for the color function and arrow function
                #the value says in which intevall it belongs
                #it is the total moves of an activiy divided by the maximum number of the total activity in the whole dataset
                colorIntesityPercentage = total/maxTotalActivity


                transition = Rectangle(Point(x1, y1), Point(x2, y2))
                transition.draw(win)

                
                if syn ==0 and mm == 0:
                    transition.setFill(color_rgb(192,243,255))
                    transition.setOutline(color_rgb(192,243,255))
                    
                if actName == 'TAU' and syn == 0 and mm == 0:
                    transition.setFill('black')
                    transition.setOutline('black')

                percentage = mm/total
                height = y2-y1
                fute = height*percentage
                
                cc = Rectangle(Point(x1, y1), Point(x2, y1+fute))

                if mm != 0:
                    cc.draw(win)
                    
                color(transition,cc,colorIntesityPercentage)

                act_name  = Text(Point(x1+25, y1+6), actName )
                act_name.setSize(5)
                act_name.draw(win)
                
                if mm == 0:
                   syn_moves_nr = Text(Point(x1+45, y1+ 16), syn)
                   syn_moves_nr.setSize(6)
                   syn_moves_nr.draw(win)
                elif syn == 0: 
                   model_moves_nr = Text(Point(x1+45, y1+ 16), mm)
                   model_moves_nr.setSize(6)
                   model_moves_nr.draw(win)
                else:
                   model_moves_nr = Text(Point(x1+45, y1+ fute - 5), mm)
                   model_moves_nr.setSize(6)
                   model_moves_nr.draw(win)
                   syn_moves_nr = Text(Point(x1+45, y1+fute+6), syn)
                   syn_moves_nr.setSize(6)
                   syn_moves_nr.draw(win)
                   
            #if modulus is not equal to zero will be positioned in the next position with the coordinates below the previus position
            else:
                a = 180
                b = 230

                x1 = 100 + position*180
                y1 = a + e*65
                x2 = 160 + position*180
                y2 = b + e*65
                
                id = d[position][e]
                
                if d[position][e] == '':
                    print(e)

                else:
                    #save the coordinates
                    data['x1'][id] = x1
                    data['x2'][id] = x2
                    data['y1'][id] = y1
                    data['y2'][id] = y2
    
                    #load the data information for the rectangle
                    actName = data['act'][id]
                    syn = data['syn'][id]
                    mm = data['mm'][id]
                    total = data['total'][id]
                    colorIntesityPercentage = total/maxTotalActivity
                    
                    #draw the activity
                    transition = Rectangle(Point(x1, y1), Point(x2, y2))
                    transition.draw(win)

                    if syn ==0 and mm == 0:
                        transition.setFill(color_rgb(192,243,255))
                        transition.setOutline(color_rgb(192,243,255))
                    #silent transition  
                    if actName == 'TAU' and syn == 0 and mm == 0:
                        transition.setFill('black')
                        transition.setOutline('black')
                    
                    #draw deviations
                    percentage = mm/total
                    height = y2-y1
                    fute = height*percentage
                    
                    cc = Rectangle(Point(x1, y1), Point(x2, y1+fute))
                    
                    if mm != 0:
                        cc.draw(win)
                        
                    color(transition,cc,colorIntesityPercentage)
                    
                    #show the information about the activity names and moves   in the rectangle
                    act_name  = Text(Point(x1+25, y1+6), actName )
                    act_name.setSize(5)
                    act_name.draw(win)
                    
                    if mm == 0:
                       syn_moves_nr = Text(Point(x1+45, y1+ 16), syn)
                       syn_moves_nr.setSize(6)
                       syn_moves_nr.draw(win)
                    elif syn == 0: 
                       model_moves_nr = Text(Point(x1+45, y1+ 16), mm)
                       model_moves_nr.setSize(6)
                       model_moves_nr.draw(win)
                    else:
                       model_moves_nr = Text(Point(x1+45, y1+ fute - 5), mm)
                       model_moves_nr.setSize(6)
                       model_moves_nr.draw(win)
                       syn_moves_nr = Text(Point(x1+45, y1+fute+6), syn)
                       syn_moves_nr.setSize(6)
                       syn_moves_nr.draw(win)

                    







#####################  DRAWING THE PLACES FROM THE LAST ACTIVITY TO THE BEGIN #####################
#create the columns for the place coordinates
data['circleX'] = 0
data['circleY'] = 0

#it starts from the end till the first activity
for position in range(len(d)-1,-1,-1):
    
    positions = pd.DataFrame()
    #position has one activity only
    if len(d[position])==1: 
        positions = positions.append(data[data['id'][:]==d[position][0]])
        positions = positions.reset_index(drop=True)
        
        #takes the cordinates of the rectangle 
        #the place center should be 45 pixel before it 
        circleX = positions['x1'][0]-30-15
        circleY = positions['y1'][0] + (positions['y2'][0]-positions['y1'][0])/2
        
        #takes the id of the activity
        id  = positions['id'][0]
        
        #saves the coordinates in the dataset
        data['circleX'][id] = circleX
        data['circleY'][id] = circleY
        
        #draw the place
        place = Circle(Point(circleX,circleY), 15) 
        place.draw(win)

        
    #if there are more than one activity   
    else:
        for e in range(0, len(d[position])):
            if d[position][e] != '':
                #load the data row of this activity
                positions = positions.append(data[data['id'][:]==d[position][e]])
                positions = positions.reset_index(drop=True)
        if len(positions)==1: 
        
            circleX = positions['x1'][0]-30-15
            circleY = positions['y1'][0] + (positions['y2'][0]-positions['y1'][0])/2
            
            id  = positions['id'][0]
            
            data['circleX'][id] = circleX
            data['circleY'][id] = circleY
            
            place = Circle(Point(circleX,circleY), 15) 
            place.draw(win)
        
        else:
            for f in range(0, len(positions)-1):
                #if there are more activities with the same prior 
                #the place should be drawn(y coordinate) in the middle of the them 
                if positions['prior'][f] == positions['prior'][f+1]:
                    priorsLength = positions['prior'][f]
                    circleX = positions['x1'][f]-30-15
                    circleY = positions['y1'][f] + (positions['y2'][f+1]-positions['y1'][f])/2
                    #save the place coordinates for each activity 
                    for f in range(0, len(positions)):
                        id  = positions['id'][f]
                        data['circleX'][id] = circleX
                        data['circleY'][id] = circleY
                    
                    place = Circle(Point(circleX,circleY), 15) 
                    place.draw(win)
                    
                else: 
                    #if they do not have the same priors 
                    #draw them normaly
                    circleX = positions['x1'][f]-30-15
                    circleY = positions['y1'][f] + (positions['y2'][f]-positions['y1'][f])/2
                    
                    id  = positions['id'][f]
                    
                    data['circleX'][id] = circleX
                    data['circleY'][id] = circleY
                    
                    place = Circle(Point(circleX,circleY), 15) 
                    place.draw(win)








##################### ARROWS FINDING THE FOLLOWING ACTIVITIES  #####################
for position in range(0,len(d)):
    if len(d[position]) == 1: 
        print('POSITION',position)
        id = d[position][0]
        connection = data[data['id'][:]==d[position][0]]

        #checks if it is the first activity
        if connection['prior'][id] == '':
            print(connection['x1'][id])
            #the percentage needed to define the intervall for the function arrow
            colorIntesityPercentage = connection['total'][id]/maxTotalActivity
            #draws the arrow  
            arc1 = Line(Point(connection['circleX'][id]+15, connection['circleY'][id]), Point(connection['x1'][id], connection['y1'][id]+(connection['y2'][id]-connection['y1'][id])/2)) # set endpoints
            arc1.draw(win)
            arc1.setArrow("last")
            #calls arrow activity
            arrow(arc1,colorIntesityPercentage)
        
        #takes the coordinates where the place of the following activity is 
        find = connection['post'][id][0]
        findthePlace = data[data['id'][:]==find]
        
        #the cordinates where the arc should start from the activity itself
        x1 = connection['x1'][id]
        y1 = connection['y1'][id]
        x2 = connection['x2'][id]
        y2 = connection['y2'][id]
        
        #the coordinates where the arc should end
        circleX = findthePlace['circleX'][find]
        circleY = findthePlace['circleY'][find]

        x1A1 = x2
        y1A1 = y1 + (y2-y1)/2
        x2A1 = circleX-15
        y2A1 = circleY
        
        
        x1A2 = circleX + 15
        y1A2 = circleY 
        
        colorIntesityPercentage = connection['total'][id]/maxTotalActivity

        arc1 = Line(Point(x1A1, y1A1), Point(x2A1, y2A1)) # set endpoints
        arc1.draw(win)
        arc1.setArrow("last")
        arrow(arc1,colorIntesityPercentage)

        #takes the coordinates where the next activity is 
        #draws the arc from the place to the following activity
        follower  = connection['post'][id]    
        print(follower)
        for f in range (0, len(follower)):
            if follower[f] in d[position+1]:
                x2A2 = data['x1'][follower[f]]
                y2A2 = data['y1'][follower[f]] + (data['y2'][follower[f]]-data['y1'][follower[f]])/2

                colorIntesityPercentage = data['total'][follower[f]]/maxTotalActivity
                
                arc2 = Line(Point(x1A2, y1A2), Point(x2A2, y2A2)) # set endpoints
                arc2.draw(win)
                arc2.setArrow("last")
                arrow(arc2,colorIntesityPercentage)
                
                
    else: 
        #when there are more than one activity in the position
        for e in range(0, len(d[position])):
            print('POSITION',position)
            if d[position][e] != '':
                id = d[position][e]
                print(id)
                connection = data[data['id'][:]==id]                
                if connection['post'][id][0] != '':
                    find = connection['post'][id][0]
                    print('FIND',find)
                    
                    findthePlace = data[data['id'][:]==find]
                    #the cordinates where the arc should start from the activity itself
                    x1 = connection['x1'][id]
                    y1 = connection['y1'][id]
                    x2 = connection['x2'][id]
                    y2 = connection['y2'][id]
                
                
                    #the coordinates where the arc should end
                    circleX = findthePlace['circleX'][find]
                    circleY = findthePlace['circleY'][find]

                    
                    x1A1 = x2
                    y1A1 = y1 + (y2-y1)/2
                    x2A1 = circleX-15
                    y2A1 = circleY
                    
                    
                    x1A2 = circleX + 15
                    y1A2 = circleY 

                    
                    colorIntesityPercentage = connection['total'][id]/maxTotalActivity

                    arc1 = Line(Point(x1A1, y1A1), Point(x2A1, y2A1)) # set endpoints
                    arc1.draw(win)
                    arc1.setArrow("last")
                    arrow(arc1,colorIntesityPercentage)
                    
                    #takes the coordinates where the next activity is 
                    #draws the arc from the place to the following activity
                    follower = connection['post'][id]
                    for f in range (0, len(follower)):
                        for i in range(1, len(d)):
                            if follower[f] in d[i]:
                                x2A2 = data['x1'][follower[f]]
                                y2A2 = data['y1'][follower[f]] + (data['y2'][follower[f]]-data['y1'][follower[f]])/2

                                colorIntesityPercentage = data['total'][follower[f]]/maxTotalActivity

                                arc2 = Line(Point(x1A2, y1A2), Point(x2A2, y2A2)) # set endpoints
                                arc2.draw(win)
                                arc2.setArrow("last")
                                arrow(arc2,colorIntesityPercentage)
                           



                else:
                    #takes the coordinates of the last activity and draws the last place 
                    x1 = connection['x1'][id]
                    y1 = connection['y1'][id]
                    x2 = connection['x2'][id]
                    y2 = connection['y2'][id]

                    place = Circle(Point(x2+45,207), 15) 
                    place.draw(win)
                   

                    colorIntesityPercentage = connection['total'][id]/maxTotalActivity
                    #draws the arc 
                    arc2 = Line(Point(x2, y1+(y2-y1)/2), Point(x2+30, 207))
                    arc2.draw(win)
                    arc2.setArrow("last")
                    arrow(arc2,colorIntesityPercentage)
                    
#####################  Showing the number of log moves inside the place  #####################               
for position in range(0, len(d)-1):
    positions = pd.DataFrame()
    tjt = pd.DataFrame()
    if len(d[position])==1 and d[position][0]!= '': 
        positions = positions.append(data[data['id'][:]==d[position][0]])
        positions = positions.reset_index(drop=True)
        id  = positions['id'][0]
        post = positions['post'][0]
        if data['log'][id] != 0:
            #gets the cordinates of the place at the following activity and gets the log moves at the activity itself
            log_moves_nr  = Text(Point(data['circleX'][post[0]], data['circleY'][post[0]]), data['log'][id] )
            log_moves_nr.draw(win)
            log_moves_nr.setSize(7)
            
    else: 
        for e in range(0, len(d[position])):
              if d[position][e]  !='':
                print(d[position][e])
                positions = positions.append(data[data['id'][:]==d[position][e]])
                id  = positions['id'][d[position][e]]
                post = positions['post'][id]
                if data['log'][id] != 0:
                    #gets the cordinates of the place at the following activity and gets the log moves at the activity itself
                    log_moves_nr  = Text(Point(data['circleX'][post[0]], data['circleY'][post[0]]), data['log'][id] )
                    log_moves_nr.draw(win)
                    log_moves_nr.setSize(7)
   
            

                                   

            
print(data)


win.getMouse()
win.close()

                
