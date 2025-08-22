from flask import Flask, render_template, request
from dataManager import dataManager


app = Flask(__name__)
dm = dataManager()
# dm.genRandData()
# print(dm.dataFrame.columns)

@app.route("/", methods=["GET",'POST'])
def load():
    graph = None
    if request.method == "POST":
        match request.form["action"]:
            case "Generate random data frame":
                dm.genRandData()
            case "Graph Data":
                Xaxis = request.form.get("Xaxis")
                Yaxis = request.form.get("Yaxis")
                graphType = request.form.get("graphType")
                graph = dm.getGraph(Xaxis, Yaxis, graphType)
    
        
    return render_template("home.html",dataFrame = dm.getHTML(),columns = dm.getColumns(),graph = graph)

if __name__== "__main__":
    app.run(debug=True)