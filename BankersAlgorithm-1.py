class Algorithm:
    def __init__(self, resources, processes):
        self.resources = resources
        self.processes = processes
    def runAlgorithm(self):
        #The default return message
        finalMessage = "Banker's Algorithm complete!"
        #list of the history of Available resources
        resourceHistory = []
        print("Initial Resources: " + str(self.resources))
        print("Allocation   Max")
        #formatting purposes
        for i in self.processes:
            print(i)
        
        #how many processes the algorithm can fail to complete before it's declared a deadlock. The amount of processes is usually the ideal tolerance number
        tolerance = len(self.processes)
        #tracks the current index the algorithm is on
        i = 0
        #checks how many processes are finished
        finishChecker = 0
        while(True):
            #does not count finished processes towards the tolerance counter
            if not self.processes[i].finished():
                if not self.processes[i].finished() and self.resources.finishProcess(self.processes[i]):
                    #adding the current change in resources to resourceHistory along with what process it just finished
                    resourceHistory.append(str(self.resources) + " (p" + str(i) + ")")
                    finishChecker += 1
                    #if the amount of finished processes equal the amount of processes, then that means every process is finished and we can end the algorithm
                    if finishChecker == len(self.processes):
                        break;
                    tolerance = len(self.processes)
                    #print("Process completed. Resetting tolerance level.")
                else:
                    tolerance -= 1
                    #print("Tolerance level: " + str(tolerance))
                    if tolerance <= 0: 
                        finalMessage += " (WARNING: COULD NOT FINISH EVERY PROCESS)"
                        break;
            i += 1
            i = i%len(self.processes)
        #formatting purposes
        print("Allocation   Max     Available")
        #using enumerate to get list index and the object in the list
        for index, i in enumerate(self.processes):
            print(i, end="")
            #using try for if the resourceHistory list is shorter than the list of processes. Typically happens if it runs into what it believes to be a deadlock
            try:
                print("      " + str(resourceHistory[index]))
            except: 
                print("")
        return finalMessage

class Resources:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def finishProcess(self, other):
        #checks if other is a Process object. If it is, then checks if this Resources object has enough resources to complete the process. If it does, spend resources and then get the resources back from the process who no longer needs it because it's finished.
        #The return boolean is there to simplify the algorithm
        if type(other) is Process:
            a, b, c = other.getNeedResources()
            if self.a >= a and self.b >= b and self.c >= c:
                #print(a,b,c)
                other.allocate(self.spendResources(a, b, c))
                self.receiveResources(other.getResources())
                return True
        return False
    #remove a set amount of resources from the object and return it as a tuple
    def spendResources(self, a, b, c):
        self.a -= a
        self.b -= b
        self.c -= c
        return a, b, c #returns a tuple of a, b, and c
    #gets a set amount of resources. resources has to be a tuple
    def receiveResources(self, resources):
        a, b, c = resources #unpacks tuple received from Process.getResources()
        self.a += a
        self.b += b
        self.c += c
    #returns how many resources in this Resources object
    def getResources(self):
        return self.a, self.b, self.c
    #for formatting purposes
    def __str__(self):
        #return (f"                       {self.a} {self.b} {self.c}")
        return (f"{self.a} {self.b} {self.c}")
    #another way of seeing how many resources in the Resources object
    def status(self):
        return (f"This resource currently has {self.a} of resource A, {self.b} of resource B, and {self.c} of resource C.")

class Process:
    def __init__(self, maxA, maxB, maxC):
        self.a = 0
        self.maxA = maxA
        self.b = 0
        self.maxB = maxB
        self.c = 0
        self.maxC = maxC
    #adds a set amount of resources to this process. resources variable must be a tuple
    def allocate(self, resources):
        a, b, c = resources #unpacks tuple received from Resource.spendResources()
        self.a += a
        self.b += b
        self.c += c
    #checks if the Process is finished by if its current resources is the same or more than the amount of resources it needs to finish
    def finished(self):
        if self.a >= self.maxA and self.b >= self.maxB and self.c >= self.maxC:
            return True
        return False
    #does not subtract from the current amount of resources it has to keep track of if the process is finished or not
    def getResources(self):
        return self.a, self.b, self.c
    #returns amount of resources the process needs to finish
    def getNeedResources(self):
        return self.maxA-self.a, self.maxB-self.b, self.maxC-self.c
    def __str__(self):
        return (f"  {self.a} {self.b} {self.c}     {self.maxA} {self.maxB} {self.maxC}")
    #Returns the amount of resources it has and the amount it needs to finish
    def status(self):
        return (f"This process currently has {self.a} of resource A, {self.b} of resource B, and {self.c} of resource C. It needs {self.maxA-self.a} of resource A, {self.maxB-self.b} of resource B, and {self.maxC-self.c} of resource C to finish its task.")
    
processes = []
r0 = Resources(2, 4, 6)
p0 = Process(2, 4, 6)
p1 = Process(1, 0, 1)
p1.allocate((1, 0, 0))
p2 = Process(3, 2, 0)
p2.allocate((2, 0, 0))
p3 = Process(7, 7, 7)
p3.allocate((1, 1, 1))
processes.append(p0)
processes.append(p3)
processes.append(p1)
processes.append(p2)

#Adding p4 to the processes list will provide enough resources to prevent a deadlock!
print("Put in p4? Enter Y for yes.")
x = input()
if x.lower() == "y":
    p4 = Process(4, 4, 4)
    p4.allocate((2, 2, 2))
    processes.append(p4)

a0 = Algorithm(r0, processes)
print(a0.runAlgorithm())
