from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from sympy import Symbol,sympify,lambdify,diff,latex
from numpy import zeros,diag,round,arange,linspace
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib
import os
matplotlib.use('agg')
x = Symbol('x')
class Metodos:
    def __init__(self,x,y,yd,a):
        self.x = x
        self.y = y
        self.yd = yd
        self.a = a
    def PLi(self,i,x):
        polinomio = 1
        for j in range(len(self.x)):
            if j!=i:
                polinomio*=(x-self.x[j])/(self.x[i]-self.x[j])
        return polinomio
    def derivar(self,i,x):
        return diff(self.PLi(i,x))
    def tables(self,values):
        return [i for i in values for j in range(2)]

    
    def polHermite(self):
        x_values = self.tables(self.x)
        
        tabla = diag(self.tablahermite()[0:,1:])

        pol = tabla[0]
        for i in range(1,len(x_values)):
            factor = tabla[i]
            termino = 1
            for j in range(i):
                termino*=(x-x_values[j])
            pol+=termino*factor

        return pol

    def tablahermite(self):
        valoresx=self.tables(self.x)
        valoresy=self.tables(self.y)
        valoresd=self.tables(self.yd)
        tabla=zeros(shape=(2*len(self.x),2*len(self.x)+1),dtype=float)

        for i in range(len(tabla)):
            tabla[i][0]=valoresx[i]
            tabla[i][1]=valoresy[i]
        for j in range(2,len(tabla[0])):
            if j%2==0:
                tabla[j-1][2]=valoresd[j-2]
            else:
                tabla[j-1][2]=(tabla[j-2][1]-tabla[j-1][1])/(tabla[j-2][0]-tabla[j-1][0])
        for j in range(2,len(tabla)):
            for i in range(j,len(tabla[j])-1):

                tabla[i][j+1]=(tabla[i-1][j]-tabla[i][j])/(tabla[i-j][0]-tabla[i][0]) 

        return tabla 
    def hermite(self):
        polinomio = 0
        for i in range(len(self.yd)):
            dl = lambdify(x,self.derivar(i,x))
            polH = (1-2*(self.a-self.x[i])*dl(self.x[i]))*self.PLi(i,self.a)**2
            polHC = (self.a-self.x[i])*(self.PLi(i,self.a))**2
            polinomio+=self.y[i]*polH+self.yd[i]*polHC
  
    
def validate(x_value):
    try:
        float(x_value)
    except:
        return False
    return True

def process(x_:str,y_:str,yd_:str,is_function:str):
    try:
        x_values = x_.split(",")
        for value in x_values:
            if not validate(value):
                raise Exception(f"El valor {value} no es numerico pra 'X' " )
        x_values = [float(i) for i in x_values]
        if is_function:
            try:
                fun = sympify(y_)
                f = lambdify(x,fun)
                
                yd = lambdify(x,fun.diff(x))
                y_values = [float(f(i)) for i in x_values]
                y_d_values = [float(yd(i)) for i in x_values]
            except Exception as e:
                raise Exception("La funcion no es valida")
        else:
            y_values = y_.split(',')
            for value in y_values:
                if not validate(value):
                    raise Exception (f"El valor {value} no es numerivo para 'Y' ")
            y_values = [float(i) for i in y_values]
            y_d_values = yd_.split(',')
            for value in y_d_values:
                if not validate(value):
                    raise Exception (f"El valor {value} no es numerivo para  Y'  ")
            y_d_values = [float(i) for i in y_d_values]
            if len(x_values)!=len(y_values) or len(y_values)!=len(y_d_values) or len(x_values)!=len(y_d_values):
                raise Exception("Las cantidades de puntos son coinciden")
            
        return {"x":x_values,"y":y_values,"yd":y_d_values}
    except Exception as e:
        raise Exception(str(e))
def index(request):
    return render(request=request,template_name="index.html")
def generate_table(table_values,request):
    df = DataFrame(table_values)

    fig,ax = plt.subplots()
    ax.axis('off')
    tabla = ax.table(cellText=df.values,colLabels=df.columns,cellLoc="center",loc="center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    for key,cell in tabla.get_celld().items():
        cell.set_width(0.1)
        cell.set_height(0.1)
    path = os.path.join(settings.BASE_DIR,f'media/img/hermite/tabla.png')
    plt.savefig(path,bbox_inches='tight')
def hermite(request):
    data = {}
    if request.method == "POST":
        try:
            fun = request.POST["is_funtion"]=='true'
  
            res = process(request.POST["x_values"],request.POST["y_values"],request.POST["y_d_values"],fun)
            point = float(request.POST["point"])
            metodo = Metodos(res["x"],res["y"],res["yd"],point)
            pol = metodo.polHermite()
            tabla = metodo.tablahermite().round(2)
            generate_table(tabla,request)
            pol_str = str(latex(pol.expand()))
            path = '/media/img/hermite/tabla.png'
            f = lambdify(x,pol)
            xmin,xmax = min(res["x"])-1,max(res["x"])+1
      
            x_values = list(linspace(int(xmin),int(xmax)))
            y_values = [float(f(i)) for i in x_values]
            y_res = f(point)
            content = {
                "x":res["x"],
                "y":res["y"],
                "y_":y_values,
                "x_":x_values,
                "x_e":point,
                "y_res":y_res
            }
       
            return JsonResponse({"pol":pol_str,"img":path,"values":content},safe=False)
        except Exception as e:
            data["error"] =  str(e)
            return JsonResponse(data)
    return render(request=request,template_name="hermite.html")