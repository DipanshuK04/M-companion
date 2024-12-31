from flask import Flask,render_template,request

import pandas as pd
import networkx as nx

data = pd.read_csv('Mumbai Local Train Dataset.csv', encoding='latin1')

G = nx.MultiGraph()

for i in range(154 - 1):  
    if data['Line'][i] == data['Line'][i + 1]:  
        G.add_edge(
            data['Station'][i],
            data['Station'][i + 1],
            key=f"{data['Line'][i]}_{i}",  
            line=data['Line'][i]  
        )

def find_shortest_path(graph, start, end):
    # Get the shortest path (unweighted)
    path = nx.shortest_path(graph, source=start, target=end)
    detailed_path = []
    short_path = []
    short_path.append(start)
    prev_line = None

    for i in range(len(path) - 1):
        station = path[i]
        next_station = path[i + 1]
        
        # Access edge attributes (line) from MultiGraph
        edge_data = graph.get_edge_data(station, next_station)
        if edge_data:
            # Extract the line attribute (fetch from the first edge, assuming one exists)
            line = list(edge_data.values())[0]['line']
            if line != prev_line:
                if prev_line:  # Only add this if it's not the first station
                    detailed_path.append(f"Change to {line} line at {station} station")
                    short_path.append(f"--{prev_line} line-->")
                    short_path.append(station)
            prev_line = line
        
        detailed_path.append(station)
    detailed_path.append(end)
    short_path.append(f"--{line} line-->")
    short_path.append(end)
    return detailed_path, short_path
   
app = Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def hello_world():
    if request.method == "POST" and request.form['departure']!='' and request.form['dest']!='':
        Departure = request.form['departure']
        Destination = request.form['dest']
        # print(Departure,Destination)
        # print(type(Departure))
        # print(type(Destination))
        Detail,Short = find_shortest_path(G,Departure,Destination)
        print(Detail)
        print(Short)
        return render_template('index.html',Detail = Detail,Short = Short,stat = data['Station'].tolist())
    
    return render_template('index.html')

@app.route("/getlivestatus")
def livestatus():
    return render_template('livestatus.html')

@app.route("/aboutus")
def aboutUs():
    return render_template('aboutus.html')

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=3000)
    
    
    
# import pandas as pd
# import networkx as nx

# data = pd.read_csv('Mumbai Local Train Dataset.csv', encoding='latin1')
# data['Time taken From Previous of the Line'] = data['Time taken From Previous of the Line'].str.extract(r'(\d+)').astype(int)
# G = nx.Graph()

# for i in range(154 - 1):  # Use len(data) for flexibility
#     if data['Line'][i] == data['Line'][i + 1]:  # Check if the line matches
#         G.add_edge(
#             data['Station'][i],
#             data['Station'][i + 1],
#             weight=data['Time taken From Previous of the Line'][i],
#             line=data['Line'][i],
#         )

# def find_shortest_path(graph, start, end):
#     path = nx.shortest_path(graph, source=start, target=end, weight='weight')
#     detailed_path = []
#     short_path = []
#     prev_line = graph[path[0]][path[1]]['line']
#     short_path.append(start)
#     for i in range(len(path) - 1):
#         station = path[i]
#         next_station = path[i + 1]
#         line = graph[station][next_station]['line']
#         detailed_path.append(station)
#         if line != prev_line:
#             short_path.append({station,i})
#             detailed_path.append(f"Change line to {line} line at {station} station")
#         prev_line = line
    
#     detailed_path.append(end)
#     short_path.append(end)
#     return detailed_path,short_path
