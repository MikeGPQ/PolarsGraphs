import faker
import polars
import matplotlib.pyplot as plt
import os

gen = faker.Faker()

class dataManager:
    def __init__(self):
        self.dataFrame = polars.DataFrame().lazy()
        self.copy = self.dataFrame

    def setDataFrame(self,dataFile):
        match os.path.splitext(dataFile.filename)[1]:
            case ".csv":
                self.dataFrame = polars.read_csv(dataFile).lazy()
            case ".xlsx":
                self.dataFrame = polars.read_excel(dataFile.read()).lazy()
            case ".json":
                self.dataFrame = polars.read_json(dataFile).lazy()
        self.copy = self.dataFrame.clone()

    def genRandData(self,units):
        data = []
        for _ in range(units):
            firstName = gen.first_name()
            lastName = gen.last_name()
            email = f"{firstName}_{lastName}@user.com"
            user = {
                "First Name": firstName,
                "Last Name": lastName,
                "Email": email,
                "Country": gen.country(),
                "Phone": gen.phone_number(),
                "Salary": gen.pyint(min_value=8, max_value=10000)
            }
            data.append(user)
        self.dataFrame = polars.DataFrame(data).lazy()
        self.copy = self.dataFrame.clone()
    
    def getHTML(self):
        if self.dataFrame.limit(1).collect().is_empty():
            return None
        
        return self.dataFrame.collect()._repr_html_()
    
    def getColumns(self):
        if self.dataFrame.limit(1).collect().is_empty():
            return None
        return self.dataFrame.columns
    
    def getGraph(self,Xaxis,Yaxis,graphType,format):
        if self.dataFrame.limit(1).collect().is_empty():
            return None
        nRows = self.dataFrame.select(polars.count()).collect().item()

        width = 15
        height = 10
        xFactor = 1 + (nRows/500)
        yFactor = 1 + (nRows/1000)
        height = min(max(height*yFactor,10),50)
        width = min(max(width*xFactor,15),50)

        fig, ax = plt.subplots(figsize=(width, height))

        plt.style.use("fivethirtyeight")
        graphDF = self.dataFrame.select(polars.col(Xaxis),polars.col(Yaxis)).collect()
        if graphType == "lineGraph":
            ax.plot(graphDF[Xaxis],graphDF[Yaxis])
        else:
            ax.bar(graphDF[Xaxis],graphDF[Yaxis])

        ax.set_title("Graph Data Frame")
        ax.set_xlabel(Xaxis)
        ax.set_ylabel(Yaxis)
        if nRows > 20:
            plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        if format == "PNG":
            fig.savefig("static/images/graph.png")
            return "static/images/graph.png"
        else:
            fig.savefig("static/images/graph.pdf")
            return "static/images/graph.pdf"
        
    def getFilterData(self,filterCol,filterVal):
        col_type = self.dataFrame.schema[filterCol]
        if col_type == "foo":
            if polars.Int64 in (polars.Int8, polars.Int16, polars.Int32, polars.Int64):
                filterVal = int(filterVal)
            elif polars.Float64 in (polars.Float32, polars.Float64):
                filterVal = float(filterVal)

        self.dataFrame = self.dataFrame.filter(polars.col(filterCol)==filterVal)
    
    def getSortData(self,sortColumn,descendingValue):
        self.dataFrame = self.dataFrame.sort(by=sortColumn,descending=descendingValue)
        
    
