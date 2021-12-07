
isometries = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
path = "/home/fidel/patung/dinamica/dinamica_isometry_runs"

for isometry in isometries:
    for i in range(1,21):
        sufijo = str(i).zfill(2)
    
        model_path = "dinamica_isometry_runs/iso_"+str(isometry)+"/similitud"+sufijo+".egoml"
        #command = "singularity exec --bind /srv/home/fidel/dinamica/tmp1:/tmp dinamica.sif dinamica_app/squashfs-root/usr/bin/DinamicaConsole -processors 20 -memory-allocation-policy 3 "+ model_path
        command = "singularity exec --bind /srv/home/fidel/dinamica/tmp1:/tmp dinamica.sif dinamica_app/squashfs-root/usr/bin/DinamicaConsole -processors 20 "+ model_path
        print(command)