
import os
from os.path import join
import pandas
import shutil
import numpy as np

## /bin/python3 /home/fidel/patung/dinamica/dinamica_isometry_runs/create_run_folders.py > ../todos.sh

def create_folders(tm_variations,patcher_variations,expander_variations):
    pass

def create_folders_isometry(path, isometries):
    for isometry in isometries:
        #print("iso_"+str(isometry))
        folder_name = "iso_"+str(isometry)
        folder_path = join(path,folder_name)
        os.mkdir(folder_path)

        # tm = pandas.read_csv(join(path,"corrida_x","tm3_5_custom.csv"))
        # for idx,row in tm.iterrows():
        #     if int(row[0]) == 9 and int(row[1]) == 2:
        #         tm.iat[idx,2] = value_9_2  
        # tm_path = join(folder_path,"tm3_5_custom.csv")
        # tm.to_csv(tm_path, index = False, header=True)

        patcher_params = pandas.read_csv(join(path,"corrida_x","patcher_parameters.csv"))
        patcher_params.loc[:,'Patch_Isometry'] = isometry
        patcher_params_path = join(folder_path,"patcher_parameters.csv")
        patcher_params.to_csv(patcher_params_path, index = False, header=True)

        expander_params = pandas.read_csv(join(path,"corrida_x","expander_parameters.csv"))
        expander_params.loc[:,'Patch_Isometry'] = isometry
        expander_params_path = join(folder_path,"expander_parameters.csv")
        expander_params.to_csv(expander_params_path, index = False, header=True)

        shutil.copy2(join(path,"corrida_x","c_coeficents_3_5.dcf"),folder_path)
        shutil.copy2(join(path,"corrida_x","allocate_change_5_6_anual.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","modulate_tm.csv"),folder_path)
        shutil.copy2(join(path,"corrida_x","tm5_6_custom.csv"),folder_path)

        shutil.copy2(join(path,"corrida_x","similitud01.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud02.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud03.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud04.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud05.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud06.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud07.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud08.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud09.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud10.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud11.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud12.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud13.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud14.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud15.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud16.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud17.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud18.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud19.egoml"),folder_path)
        shutil.copy2(join(path,"corrida_x","similitud20.egoml"),folder_path)
            
         
#isometries = np.arange(0, 2, 0.1).tolist()
isometries = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
path = "/home/fidel/patung/dinamica/dinamica_isometry_runs"
create_folders_isometry(path, isometries)


for isometry in isometries:
    model_path = "dinamica_isometry_runs/iso_"+str(isometry)+"/allocate_change_5_6_anual.egoml"
    #command = "singularity exec --bind /srv/home/fidel/dinamica/tmp1:/tmp dinamica.sif dinamica_app/squashfs-root/usr/bin/DinamicaConsole -processors 20 -memory-allocation-policy 3 "+ model_path
    command = "singularity exec --bind /srv/home/fidel/dinamica/tmp1:/tmp dinamica.sif dinamica_app/squashfs-root/usr/bin/DinamicaConsole -processors 20 "+ model_path
    print(command)