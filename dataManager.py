import faker
import polars
import matplotlib.pyplot as plt

gen = faker.Faker()

class dataManager:
    def __init__(self):
        self.dataFrame = polars.DataFrame()

    def genRandData(self,units=5):
        data = []
        for _ in range(units):
            firstName = gen.first_name()
            lastName = gen.last_name()
            email = f"{firstName}_{lastName}@user.com"
            user = {
                "First Name": firstName,
                "Last Name": lastName,
                "Email": email,
                "Phone": gen.phone_number(),
                "Salary": gen.pyint(min_value=8, max_value=10000)
            }
            data.append(user)
        self.dataFrame = polars.DataFrame(data)
    
    def getHTML(self):
        if self.dataFrame.is_empty():
            return None
        return self.dataFrame._repr_html_()
    
    def getColumns(self):
        if self.dataFrame.is_empty():
            return None
        return self.dataFrame.columns
    
    def getGraph(self,Xaxis,Yaxis,graphType):
        if self.dataFrame.is_empty():
            return None
        fig, ax = plt.subplots(figsize=(10,6))
        plt.style.use("fivethirtyeight")
        if graphType == "lineGraph":
            ax.plot(self.dataFrame[Xaxis],self.dataFrame[Yaxis])
        else:
            ax.bar(self.dataFrame[Xaxis],self.dataFrame[Yaxis])
        ax.set_title("Graph Data Frame")
        ax.set_xlabel(Xaxis)
        ax.set_ylabel(Yaxis)
        plt.tight_layout()
        fig.savefig("static/images/graph.png")
        return "static/images/graph.png"
        
