from flask import Flask, render_template, request, send_file
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
                units = int(request.form.get("units4DataFrame"))
                dm.genRandData(units)
            case "Export":
                Xaxis = request.form.get("Xaxis")
                Yaxis = request.form.get("Yaxis")
                graphType = request.form.get("graphType")
                format = request.form.get("graphFormat")
                graph = dm.getGraph(Xaxis, Yaxis, graphType,format)
                if format == "PNG":
                    return send_file(graph,as_attachment=True,download_name="graph.png")
                else:
                    return send_file(graph,as_attachment=True,download_name="graph.pdf")
            case "Upload":
                dm.setDataFrame(request.files["dataFile"])
            case "Filter":
                filertCol = request.form.get("filterColumn")
                filterVal = request.form.get("filterValue")
                dm.getFilterData(filertCol,filterVal)
            case "Restore":
                dm.dataFrame = dm.copy
            case "Sort":
                sortColumn = request.form.get("sortColumn")
                descendingValue = eval(request.form.get("descendingValue"))
                dm.getSortData(sortColumn,descendingValue)

    
        
    return render_template("home.html",dataFrame = dm.getHTML(),columns = dm.getColumns())

if __name__== "__main__":
    app.run(debug=True)