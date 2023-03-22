#define Condition class
class Condition:
    def __init__(self, id, diagnosed, cured, kind):
        self.id = id
        self.diagnosed = diagnosed
        self.cured = cured
        self.kind = kind

#define Therapy class
class Therapy:
    def __init__(self, id, start, end, condition, therapy, successful):
        self.id  = id
        self.start = start
        self.end = end
        self.condition = condition
        self.therapy = therapy
        self.successful = successful

    def isEnded(self):  
        if self.end == None:
            return False
        else:
            return True

    def isSuccessful(self):
        if self.successful < 75:
            return False
        else:
            return True

#define Patient class
class Patient:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.list_of_conditions = []
        self.list_of_therapies = []

    def addCondition(self, condition):
        self.list_of_conditions.append(condition)
        
    def addTherapy(self, therapy):
        self.list_of_therapies.append(therapy)