var edges;
var nodes;
var allNodes;
var allEdges;
var nodeColors;
var originalNodes;
var network;
var container;
var options, data;
var filter = {
  item : '',
  property : '',
  value : []
};

async function drawDeps(ele) {
    document.getElementById('processingDialog').style.display = 'block'
    try {
        return await fetch('draw', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({'resource': ele.value}),
        }).then((response) => response.json())
                .then((resp) => {
                     document.getElementById('processingDialog').style.display = 'none'
                    if (resp['error']) {
                        alert(resp['errorMsg'])
                    } else {
                        let nodeList = resp['data']['nodes']
                        let edgeList = resp['data']['edges']
                        drawGraph(nodeList,edgeList);
                    }
                })
    } catch (error) {
        console.log(error)
        alert('API error')
    }
}


function drawGraph(nodeList,edgeList) {
  let container = document.getElementById('results');
  container.height = 1000
  container.width = 4000
  container.style.width = 'auto'
  container.style.height = '1000px'
  nodes = new vis.DataSet(nodeList);
  edges = new vis.DataSet(edgeList);

  nodeColors = {};
  allNodes = nodes.get({ returnType: "Object" });
  for (nodeId in allNodes) {
    nodeColors[nodeId] = allNodes[nodeId].color;
  }
  allEdges = edges.get({ returnType: "Object" });
  data = {nodes: nodes, edges: edges};

  var options = {
    "configure": {
        "enabled": false
    },
    "edges": {
        "arrows": {
              "to": {
                "enabled": true
              }
            },
        "color": {
            "inherit": true
        },
        "smooth": {
            "enabled": true,
            "type": "dynamic"
        }
    },
    "interaction": {
        "dragNodes": true,
        "hideEdgesOnDrag": false,
        "hideNodesOnDrag": false,
        "hover": true
    },
    "physics": {
        "enabled": true,
        "stabilization": {
            "enabled": true,
            "fit": true,
            "iterations": 1000,
            "onlyDynamicEdges": false,
            "updateInterval": 50
        },
       "barnesHut": {
       "springLength": 200,
       "avoidOverlap": 0.97
        },
    "minVelocity": 0.75
    },
    "nodes": {
        "borderWidth": 1,
        "borderWidthSelected": 1,
        "opacity": 1,
        "font": {
          "size": 10,
          "face": "tahoma"},
        "shape": "hexagon",
        "size": 5
  }
};
  network = new vis.Network(container, data, options);
  return network;

}

