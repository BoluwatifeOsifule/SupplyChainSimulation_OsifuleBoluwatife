# we are going to create an economy simulation following the supply and demand for commodities
# first import the libraries needed
import mesa #for Agent Based Model
import matplotlib.pyplot as plt # for graphing
import seaborn as sns #Seaborn for improved statistics


# DEFINE CONSUMER AGENT CLASS
class Consumer_Agent(mesa.Agent):
    def __init__(self, unique_id,model): #I call this constructor
        super().__init__(model)
        self.Demand = 5 #number of goods the consumer wants to buy
        self.income = 50 #Initial income
        self.commodities = 0#Goods owned by the consumer

# define the movement and the behavior of the consumer agent
    def move(self):
        possible_step = self.model.grid.get_neighborhood(self.pos, moore = True , include_center= False)
# self.pos = initial position of the agents
# moore = allows diagonal movement of agent
        new_position = self.random.choice(possible_step)
# movement of the agent on the grid
        self.model.grid.move_agent(self, new_position)

# we define the agent task (buying commodities and spending money )
    def buy(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1: # check if there is more than one cellmate
            Random_cellmate = self.random.choice(cellmates) # we are choosing a cellmate at random
            if Random_cellmate != self: # we check if the random agent is not a consumer
                if isinstance(Random_cellmate, Supplier_Agent):
                    if Random_cellmate.produced_goods > 0 and Random_cellmate.Supply > 0:
                        if self.Demand > 0 and self.income > 5:
                            self.Demand -= 1
                            self.income -= 5
                            self.commodities += 1


# we define the consumer's actions per time step:
#move first, then attempt to buy goods.
    def step(self):
        self.move()
        if self.Demand > 0 and self.income > 5:
            self.buy()



#DEFINE SUPPLIER AGENT CLASS
class Supplier_Agent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(model)
        self.revenue = 0 #Money earned by the supplier
        self.Supply = 5 #Nu of goods available
        self.produced_goods = 50 #Total inventory


    #The movement of the supplier

    def move(self):
        possible_step = self.model.grid.get_neighborhood(self.pos, moore = True , include_center= False)
        # self.pos = initial position of the agents
        # moore = diagonals check and left and right
        new_position = self.random.choice(possible_step)
        # we move the agent
        self.model.grid.move_agent(self, new_position)


    # we define the task of the supplier (selling) agent
    def sell(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            Random_cellmate = self.random.choice(cellmates)

    #Ensure the interacting agent is a consumer
            if Random_cellmate != self:
                if isinstance(Random_cellmate, Consumer_Agent):
                    if Random_cellmate.Demand > 0 and Random_cellmate.income > 5:
                        if self.Supply > 0 and self.produced_goods > 0:
                            self.Supply -= 1
                            self.produced_goods -= 1
                            self.revenue += 5

#Step method for suppliers
    def step(self):
        self.move()
        if self.Supply > 0 and self.produced_goods > 0:
            self.sell()


# WE DEFINE ECONOMY MODEL CLASS
class Economy_Model(mesa.Model):
    def __init__(self, C, S, width, height):
        super().__init__()
        self.Num_of_consumers = C
        self.Num_of_suppliers = S

        # create the grid for the agents movement using mesa space
        self.grid = mesa.space.MultiGrid(width, height, torus = True)

        # create the consumer agents
        for i in range(self.Num_of_consumers):
            a = Consumer_Agent(i,self)

        # create the axis for the grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

        # place the agent on the grid
            self.grid.place_agent(a,(x,y))

        # create the consumer agents
        for j in range(self.Num_of_suppliers):
            b = Supplier_Agent(j,self)

        # create the axis
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            self.grid.place_agent(b,(x,y))


    # we shuffle the agents using the step method
    def step(self):
        self.agents.shuffle_do("step")




# MODEL EXECUTION
model = Economy_Model(4000,400,30,30)
# Where C is the Number of consumers,
# While S is the Number of suppliers

#Run the simulation for 1000 steps
for i in range(100):
    print(f"Span {i}")
    model.step()


# DATA VISUALIZATION:for consumer income
incomes = []
for consumer in model.agents:
    if isinstance(consumer, Consumer_Agent):
        incomes.append(consumer.income)

if incomes:
    plt.figure(figsize = (10,10))
    sns.histplot(incomes, bins = range(max(incomes)+1), kde = True, stat = "count" , discrete = True, edgecolor = "brown" )
    plt.title("Distribution of income per consumer")
    plt.xlabel("Income")
    plt.ylabel("Number of consumers")
    plt.grid(True, alpha = 0.5)
    plt.show() # this is to show the graph
else:
    print("No income left. All the income was spent by all the consumers") # this happens if the consumers spend all their income



# DATA VISUALIZATION:for supplier income
revenues = []
for supplier in model.agents:
    if isinstance(supplier, Supplier_Agent):
        revenues.append(supplier.revenue)

if revenues:
    plt.figure(figsize = (10,10))
    sns.histplot(revenues, bins = range(max(revenues)+ 1), kde = True, stat = "count" , discrete = True, edgecolor = "black")
    plt.title("Distribution of revenue per supplier")
    plt.xlabel("Revenue")
    plt.ylabel("Number of suppliers")
    plt.grid(True, alpha = 0.5)
    plt.show()
else:
    print("No revenue generated at all")




