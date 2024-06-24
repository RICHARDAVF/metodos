
$(function(){
    $("#submit").on("click",function(){
        var form = new FormData()
        var csrf = $("input[name='csrfmiddlewaretoken']").val()
        form.append("csrfmiddlewaretoken",csrf)
        var x_values = $("#x_values").val()
        var y_values = $("#y_values").val()
        var y_d_values = $("#y_d_values").val()
        var is_function = $("#is_function").prop("checked")
        var point = $("#point").val()
        if(x_values.trim()!=='' && y_values.trim()!=="" && y_d_values.trim()!==""){
            var url = window.location.pathname
            form.append('x_values',x_values)
            form.append('y_values',y_values)
            form.append('y_d_values',y_d_values)
            form.append('metodos',"hermite")
            form.append('point',point)
            form.append('is_funtion',is_function)
            submit(form,url,function(data){
            
                document.getElementById("polinomio").innerHTML = '\\['+data.pol+'\\]'
                MathJax.typeset()
                document.getElementById("image-hermite").src = data.img
                const xdata1 = data.values["x"]
                const ydata1 = data.values["y"]
                const xdata2 = data.values["x_"]
                const ydata2 = data.values["y_"]
             
                const trace1 = {
                    x:xdata1,
                    y:ydata1,
                    type:"scatter",
                    mode:"markers",
                    name:"Puntos",
                    marker:{size:10}
                }
                const trace2 = {
                    x:xdata2,
                    y:ydata2,
                    type:"scatter",
                    mode:"lines",
                    name:"Pol Interpolador",
                    marker:{size:10}  
                }
                const trace3 = {
                    x:[data.values["x_e"]],
                    y:[data.values["y_res"]],
                    type:"scatter",
                    mode:"markers",
                    name:"Punto evaluado",
                    marker:{size:15}  
                }
                const dates = [trace1,trace2,trace3]
                const layout = {
                    title:"GRAFICO",
                    xaxis:{title:"X"},
                    yaxis:{title:"Y"},
                }
                Plotly.newPlot("grafico",dates,layout)
            })
        }
    })
})