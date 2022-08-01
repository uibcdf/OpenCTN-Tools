

#leemos la base de datos de la trayectoria
with open("double_well/traj.txt", "r") as datos:
    lineas = datos.readlines()
    #print(type(lineas))
    valores = []
    #sacamos los datos de las posiciones y el tiempo
    #guardamos en la variable valores
    for i in range(1,len(lineas)):
        valores.append([float(x) for x in lineas[i].strip().split(" ")])
    #print(valores[0][1])

    #Sacamos los intervalos 
    h_x = (max(valores[1][:])-min(valores[1][:]))
    #i = 99999
    #j = 3
    #print("Valor de (" + str(i) + "," + str(j) + "): " + str(valores[i][j]))
    #Los intervalos serán de -1 amstrong a 7 amstrings
    n = 1000 #número de intervalos
    a = -7.0 #límite inferior
    b = 7.0  #límite superior
    h = (b-a)/n #ancho de los intervalos
    m_x = [0]*n #arreglo para el histograna
    m_y = [0]*n
    m_z = [0]*n
    for i in range(n):
        for j in range(len(valores)):
            if valores[j][1] >= a+i*h and valores[j][1] < a+(i+1)*h:
                m_x[i] += 1
            if valores[j][2] >= a+i*h and valores[j][2] < a+(i+1)*h:
                m_y[i] += 1
            if valores[j][3] >= a+i*h and valores[j][3] < a+(i+1)*h:
                m_z[i] += 1
        print(str(m_x[i]) + " " + str(m_y[i]) + " " + str(m_z[i]))