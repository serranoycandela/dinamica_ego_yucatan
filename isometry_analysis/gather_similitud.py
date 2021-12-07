from os.path import join

isometries = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
path = "/home/fidel/patung/dinamica/dinamica_isometry_runs"
with open(join(path,"similitud.csv"),"w") as pluma:
    pluma.write("isometry,promedio\n")
    for isometry in isometries:
        suma = 0
        for i in range(1,21):
            sufijo = str(i).zfill(2)

            data_path = join(path,"iso_"+str(isometry),"sim"+sufijo)
            
            with open(data_path) as f:
                contents = f.read()
                print("iso ",isometry, "_", i,contents)
                suma += float(contents)
        #print(suma)
        promedio = suma/20.0
        pluma.write(str(isometry)+","+str(promedio)+"\n")    


