import processing
import gdal

#C:\Dropbox (LANCIS)\cambio_cobertura_ca\insumos\mapas_aptitud\agregacion_sectores

path = 'C:/Dropbox (LANCIS)/cambio_cobertura_ca/insumos/mapas_aptitud/agregacion_sectores/'
#aptitud = os.path.join(path,"urbano.tif")

cobertura_inicial = 'C:/Dropbox (LANCIS)/cambio_cobertura_ca/insumos/series_corregidas/usv_serie5_100m_v4_corregida.tif'
cats = [1,2,4,6,7,9,11,14]
for apt in cats:
    aptitud = os.path.join(path,"aptitud_"+str(apt)+".tif")

    for cat in cats:
        if apt != cat:
            salida = os.path.join(path,"probability_"+str(cat)+"_to_"+str(apt)+".tif")
            input_raster_a = QgsRasterLayer(cobertura_inicial, 'rastera')      
            input_raster_b = QgsRasterLayer(aptitud, 'rasterb')

            #I find it nice to create parameters as a dictionary
            parameters = {'INPUT_A' : input_raster_a,
                    'BAND_A' : 1,
                    'INPUT_B' : input_raster_b,
                    'BAND_B' : 1,
                    'FORMULA' : '(A=='+str(cat)+')*B*254+(A!='+str(cat)+')*255',
                    'RTYPE' : 0,
                    'OUTPUT' : salida}

            processing.run('gdal:rastercalculator', parameters)
            
lista_nombres =[]
lista_paths =[]
for cat in cats:
    for apt in cats:
        if apt != cat:
            lista_paths.append(os.path.join(path,"probability_"+str(cat)+"_to_"+str(apt)+".tif"))
            lista_nombres.append("probability_"+str(cat)+"_to_"+str(apt))
            

cubo_path = os.path.join(path,"c_probability.tif")

parameters = {'INPUT' : lista_paths,
        'DATA_TYPE' : 0,
        'SEPARATE' : True,
        'OUTPUT' : cubo_path}
processing.runAndLoadResults('gdal:merge', parameters)




cubo_info = os.path.join(path,"c_probability.html")
parameters_info = {'INPUT' : cubo_path,
        'STATS' : True,
        'OUTPUT' : cubo_info}
processing.run('gdal:gdalinfo', parameters_info)





cubo_xml = os.path.join(path,"c_probability.tif.aux.xml")
with open(cubo_xml, "r") as f:
    contents = f.readlines()

contador = 1
contador_lineas = 1
for line in contents:
    if 'band="'+str(contador)+'"' in line:
        contents.insert(contador_lineas, "    <Description>"+lista_nombres[contador-1]+"</Description>\n")
        contador += 1
    contador_lineas += 1    

with open(cubo_xml, "w") as f:
    contents = "".join(contents)
    f.write(contents)






            