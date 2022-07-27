
from tokenize import Double


with open("double_well/traj.txt", "r") as datos:
    lineas = datos.readlines
    print(type(lineas))
    valores = []
    for linea in lineas:
        valores.append([Double(x) for x in linea.strip().split(" ")])
    print(valores)

