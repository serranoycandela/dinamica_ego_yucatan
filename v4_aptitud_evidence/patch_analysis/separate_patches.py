
s3 = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/insumos/series_corregidas/usv_serie3_100m_v4_corregida.tif"
s5 = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/insumos/series_corregidas/usv_serie5_100m_v4_corregida.tif"

agg_s3 = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/agg_s3.tif"
agg_s5 = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/agg_s5.tif"
agg_s5_s3 = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/agg_s5_s3.tif"

#pre_salida = os.path.join(path,"probability_"+str(cat)+"_to_"+str(apt)+"_pre.tif")
#salida = os.path.join(path,"probability_"+str(cat)+"_to_"+str(apt)+".tif")
#input_raster_a = QgsRasterLayer(cobertura_inicial, 'rastera')      
#input_raster_b = QgsRasterLayer(aptitud, 'rasterb')

#I find it nice to create parameters as a dictionary
parameters = {'INPUT_A' : s3,
        'BAND_A' : 1,
        'FORMULA' : '(A==2)',
        'RTYPE' : 0,
        'OUTPUT' : agg_s3}

processing.run('gdal:rastercalculator', parameters)



parameters = {'INPUT_A' : s5,
        'BAND_A' : 1,
        'FORMULA' : '(A==2)',
        'RTYPE' : 0,
        'OUTPUT' : agg_s5}

processing.run('gdal:rastercalculator', parameters)



parameters = {'INPUT_A' : agg_s5,
        'BAND_A' : 1,
        'INPUT_B' : agg_s3,
        'BAND_B' : 1,
        'FORMULA' : '((A==1)*(A-B))+((A==0)*0)',
        'RTYPE' : 0,
        'OUTPUT' : agg_s5_s3}

processing.run('gdal:rastercalculator', parameters)

alg_params = {
'map':agg_s5_s3,
'setnull':0,
'null':'',
'-f':False,
'-i':False,
'-n':False,
'-c':False,
'-r':False,
'output':agg_s5_s3,
'GRASS_REGION_PARAMETER':None,
'GRASS_REGION_CELLSIZE_PARAMETER':0,
'GRASS_RASTER_FORMAT_OPT':'',
'GRASS_RASTER_FORMAT_META':''
}

processing.run("grass7:r.null", alg_params)

agg_s5_s3_clump = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/agg_s5_s3_clump.tif"


alg_params = {
            'input':agg_s5_s3,
            'title':"agg_s5_s3_clump",
            'output':agg_s5_s3_clump,
            '-d':True
            }

processing.run("grass7:r.clump", alg_params)


new_patches_path = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/new_patches.shp"
#alg_params = {
#            'INPUT':agg_s5_s3,
#            'BAND':1,
#            'FIELD':"patch_id",
#            'OUTPUT':agg_s5_s3_clump_s
#            }
#processing.run("gdal:polygonize", alg_params)

new_patches = QgsVectorLayer(new_patches_path,"new_patches")

for este_patch in new_patches.getFeatures():
    print(este_patch['patch_id'])
