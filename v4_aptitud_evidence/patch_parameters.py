


import csv

with open('C:/Users/arabela/Desktop/insumos/mapas_aptitud/agregacion_sectores/patchParameters.csv', 'w', newline='') as f:
    patch_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    patch_writer.writerow(['From*','To*','Mean_Patch_Size','Patch_Size_Variance','Patch_Isometry'])
    
    cats = [1,2,4,6,7,9,11,14]
    for apt in cats:
        for cat in cats:
            if apt != cat:
                patch_writer.writerow([str(apt), str(cat), '0','0.0001','0'])