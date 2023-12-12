// Get data
d3.csv("https://raw.githubusercontent.com/EnLin0903/LATIA112-1/main/HW4/111_休學原因.csv").then(
    res =>{
        // console.log(res);
        drawPieChart(res);
        drawBarChart(res);
        // drawlineChart(res);
    }
);

d3.csv("https://raw.githubusercontent.com/EnLin0903/LATIA112-1/main/HW4/各學年休學人數.csv").then(
    res1 =>{
        console.log(res1);
        // const newData = res1.slice(2);
        // console.log(newData);
        drawlineChart(res1);
    }
);


function drawBarChart(res){
    let myGraph = document.getElementById('myGraph');

    let trace1 = {};
    trace1.type = "bar";
    
    trace1.x = ["博士班","碩士班","學士班","其他"];
    trace1.y = [0, 0, 0, 0];
    
    
    for(let x = 0; x < res.length; x++){
        let totalCount = parseInt(res[x]['總計']);


        if (res[x]['等級'] == '博士' && res[x]['總計']!=""){
            trace1.y[0] += totalCount;
        }else if(res[x]['等級'] == "碩士" && res[x]['總計']!=""){
            trace1.y[1] += totalCount;
        }else if(res[x]['等級'] == '學士' && res[x]['總計']!=""){
            trace1.y[2] += totalCount;
        }else{
            if(res[x]['總計']!=""){
                trace1.y[3] += totalCount;
            }
            
        }
    };

    trace1.text = trace1.y;
    trace1.textfont = {
        size:12,
        color:'white'
    };
    let data = [];
    data.push(trace1); 
    let layout = {
        margin:{
            t:50,
            b:80
        },
        barmode:'stack',
        title: {
            text: '111學年度各等級學生休學人數',  
            font: {
                size: 20
            }
        },
        annotations: [{
            text: '以上為111學年度各等級學生的休學人數，其中歸類為「其他」的學生是標記為「4+X」、<br>「四技」等學生。可發現除了歸類為其他的學生以外，在111學年休學人數最多的學生為<br>碩士班的學生。',
            showarrow: false,
            x: 0.5,
            y: -0.2,
            xref: 'paper',
            yref: 'paper',
            font: {
                size: 14,
                color: 'black'
            }
        }]
    };
    
    Plotly.newPlot(myGraph, data, layout);
};

function drawPieChart(res){

    let myGraph2 = document.getElementById('myGraph2');

    let trace1 = {};
    trace1.type = "pie";
    trace1.labels = ['國立大學', '私立大學'];
    trace1.values = [0, 0];

    let ck = 0;

    for(let x=0;x<res.length;x++){
        let totalCount = parseInt(res[x]['總計']);
        if(res[x]['學校'].startsWith('國立')){
            ck = 1;
            trace1.values[0] += totalCount;
        }else{
            if(ck == 1 && res[x]['學校'] == "" && res[x]['總計'] != ""){
                trace1.values[0] += totalCount; 
            }else if(res[x]['總計'] != ""){
                trace1.values[1] += totalCount;
                
                ck = 0;
            }
        }
    
    };
    console.log('國立的有：',trace1.values[0]);
    console.log('私立的有：',trace1.values[1]);
    let data = [];
    data.push(trace1);

    let layout = {
        margin:{
            t:50
        },
        title: {
            text: '111學年度國立大學與非國立大學的休學人數比例',  
            font: {
                size: 20
            }
        },
        annotations: [{
            text: '此為111學年度國立與非國立大學休學人數比例圓餅圖。私立大學的休學人數<br>為51428人，較國立大學的35972人還要高出17.6%。',
            showarrow: false,
            x: 0.5,
            y: -0.15,
            xref: 'paper',
            yref: 'paper',
            font: {
                size: 14,
                color: 'black'
            }
        }]
    }

    Plotly.newPlot(myGraph2, data, layout);
};

function drawlineChart(res1){

    let myGraph3 = document.getElementById('myGraph3');

    let trace1 ={};
    trace1.mode = "line";
    trace1.type = "scatter";
    trace1.name = "budget";
    trace1.x = [];
    trace1.y = [];
    trace1.text = [];

    for(let i=0;i<res1.length;i++){
        trace1.x[i] = res1[i]["統計期"];
        trace1.y[i] = res1[i]["學年間退學人數"];
    }


    let data =[];
    data.push(trace1);

    let layout ={
        margin:{
            t:50
        },
        title:{
            text: '103至110學年休學人數',  
            font: {
                size: 20
            }
        },
        annotations: [{
            text: '此為近幾年休學人數折線趨勢圖。最近每年的休學人數約在8.9萬人附近，在106學年<br>出現人數高峰，而後人數大致呈現下降趨勢',
            showarrow: false,
            x: 0.5,
            y: -0.2,
            xref: 'paper',
            yref: 'paper',
            font: {
                size: 14,
                color: 'black'
            }
        }]
    }

    Plotly.newPlot(myGraph3, data, layout)
};




