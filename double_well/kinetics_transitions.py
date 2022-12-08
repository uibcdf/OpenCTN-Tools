

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
    #Los intervalos serán de a hasta b
    n = 1000 #número de intervalos
    a = -7.0 #límite inferior
    b = 7.0  #límite superior
    h = (b-a)/n #ancho de los intervalos
    m_x = [0]*n #arreglo para el histograna
    m_y = [0]*n
    m_z = [0]*n
    #Creamos la Matriz para la trayectoria discretizada
    traj_dis = []
    for i in range(len(valores)):
        a = [0]*3
        traj_dis.append(a)

    #Creación de los histogramas para cada dimensión
    for i in range(n):
        for j in range(len(valores)):
            if valores[j][1] >= a+i*h and valores[j][1] < a+(i+1)*h:
                m_x[i] += 1
            if valores[j][2] >= a+i*h and valores[j][2] < a+(i+1)*h:
                m_y[i] += 1
            if valores[j][3] >= a+i*h and valores[j][3] < a+(i+1)*h:
                m_z[i] += 1
        #print(str(m_x[i]) + " " + str(m_y[i]) + " " + str(m_z[i]))
    
    #Discretización de la trayectoria
    for i in range(len(valores)):
        for j in range(n):
            if valores[i][1] >= a+j*h and valores[i][1] < a+(j+1)*h:
                traj_dis[j][1] = j
            if valores[i][2] >= a+j*h and valores[i][2] < a+(j+1)*h:
                traj_dis[j][2] = j
            if valores[i][3] >= a+j*h and valores[i][3] < a+(j+1)*h:
                traj_dis[j][3] = j
        print(str(traj_dis[i][1]) + " " + str(traj_dis[i][2]) + " " + str(traj_dis[i][3]))