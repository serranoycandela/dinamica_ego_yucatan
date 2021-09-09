from os.path import join, exists
from os import makedirs
from PyQt5.QtCore import QVariant


## this function separates new patches of a given category and a given start land cover and end land cover
## the final result is a shapefile conaining new patches and the asocieated table contains information on 
## if the new patch was adjacent to previous patch and what was the category from which it changed
def separa(path,result_path,old_index,new_index,cat,prefix):
    
    #make folders for processing and results
#    makedirs(path) if not exists(path)
#    makedirs(result_path) if not exists(result_path)
    if not exists(path): makedirs(path)
    if not exists(result_path): makedirs(result_path)
    #grab land cover from and to    
    land_old = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/insumos/series_corregidas/usv_serie"+str(old_index)+"_100m_v4_corregida.tif"
    land_new = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/insumos/series_corregidas/usv_serie"+str(new_index)+"_100m_v4_corregida.tif"

    cat_old = join(path,prefix+"_s"+str(old_index)+".tif")
    cat_new = join(path,prefix+"_s"+str(new_index)+".tif")
    new_cells = join(path,prefix+"_s"+str(old_index)+"_s"+str(new_index)+".tif")
    #extract category from land cover 
    parameters = {'INPUT_A' : land_old,'BAND_A' : 1,'FORMULA' : '(A=='+str(cat)+')','RTYPE' : 0,'OUTPUT' : cat_old}
    processing.run('gdal:rastercalculator', parameters)
    parameters = {'INPUT_A' : land_new,'BAND_A' : 1,'FORMULA' : '(A=='+str(cat)+')','RTYPE' : 0,'OUTPUT' : cat_new}
    processing.run('gdal:rastercalculator', parameters)
    #get new cells of this category
    parameters = {'INPUT_A' : cat_new,'BAND_A' : 1,'INPUT_B' : cat_old,'BAND_B' : 1,
                  'FORMULA' : '((A==1)*(A-B))+((A==0)*0)','RTYPE' : 0,'OUTPUT' : new_cells}
    processing.run('gdal:rastercalculator', parameters)
    alg_params = {'map':new_cells,'setnull':0,'null':'','-f':False,'-i':False,'-n':False,
                  '-c':False,'-r':False,'output':new_cells,'GRASS_REGION_PARAMETER':None,
                  'GRASS_REGION_CELLSIZE_PARAMETER':0,'GRASS_RASTER_FORMAT_OPT':'','GRASS_RASTER_FORMAT_META':''
    }
    processing.run("grass7:r.null", alg_params)
    #group new cells in patches
    clump_title = prefix+"_s"+str(old_index)+"_s"+str(new_index)+"_clump"
    clump_path = join(path,clump_title+".tif")
    alg_params = {'input':new_cells,'title':clump_title,'output':clump_path,'-d':True}
    processing.run("grass7:r.clump", alg_params)
    #vectorize patches
    new_patches_vector = join(path,prefix+"_s"+str(old_index)+"_s"+str(new_index)+"_new_patches.shp")
    alg_params = {'INPUT':clump_path,'BAND':1,'FIELD':"patch_id",'OUTPUT':new_patches_vector}
    processing.run("gdal:polygonize", alg_params)
    #vectorize old patches
    cat_old_null = join(path,prefix+"_s"+str(old_index)+"_null.tif")
    alg_params = {'map':cat_old,'setnull':0,'null':'','-f':False,'-i':False,'-n':False,
                '-c':False,'-r':False,'output':cat_old_null,'GRASS_REGION_PARAMETER':None,
                'GRASS_REGION_CELLSIZE_PARAMETER':0,'GRASS_RASTER_FORMAT_OPT':'','GRASS_RASTER_FORMAT_META':''
    }
    processing.run("grass7:r.null", alg_params)
    old_patches_vector = join(path,prefix+"_s"+str(old_index)+"_s"+str(new_index)+"_old_patches.shp")
    alg_params = {'INPUT':cat_old_null,'BAND':1,'FIELD':"expander",'OUTPUT':old_patches_vector}
    processing.run("gdal:polygonize", alg_params)
    #buffer old patches
    old_patches_buffer = join(path,prefix+"_s"+str(old_index)+"_s"+str(new_index)+"_old_patches_buffer.shp")
    alg_params = {'INPUT':old_patches_vector,'DISTANCE':100,'OUTPUT':old_patches_buffer}
    processing.run("native:buffer", alg_params)
    #distinguish adjacent patches by knowing if new patch intersects old patches buffer
    new_patches_adjacent = join(path,prefix+"_s"+str(old_index)+"_s"+str(new_index)+"_new_patches_adjacent.shp")
    processing.run("qgis:joinattributesbylocation",{"INPUT":new_patches_vector,"JOIN":old_patches_buffer,
                        "PREDICATE":0,"SUMMARY":0,"KEEP":1,"OUTPUT":new_patches_adjacent})
    #add the category from which the ne patch changed
    new_patches_adjacent_from = join(path,prefix+"_s"+str(old_index)+"_s"+str(new_index)+"_new_patches_adjacent_from.shp")
    processing.run("native:zonalstatisticsfb",{'COLUMN_PREFIX' : '_','INPUT':new_patches_adjacent,
                        'INPUT_RASTER' :land_old,'RASTER_BAND' : 1,'STATISTICS' : [9],
                        'OUTPUT':new_patches_adjacent_from})
                        
    layer = QgsVectorLayer(new_patches_adjacent_from,"new_patches_adjacent_from")
    layer.startEditing()
    layer_provider=layer.dataProvider()
    layer_provider.addAttributes([QgsField("from", QVariant.Int)])
    layer.updateFields()
    for feature in layer.getFeatures():
        feature["from"] = int(feature["_majority"])
        layer.updateFeature(feature)
    
    layer.commitChanges()
    layer.startEditing()
    fields = layer.fields()
    fieldIndex = fields.indexFromName('_majority')
    layer.deleteAttribute(fieldIndex)
    layer.commitChanges()
    #dissolve on patch_id to have 1 row for each patch
    new_patches_result = join(result_path,prefix+"_s"+str(old_index)+"_s"+str(new_index)+"_new_patches_result.shp")
    processing.run("qgis:dissolve",{"INPUT":new_patches_adjacent_from,"FIELD":"patch_id","OUTPUT":new_patches_result})
    #add area
    layer_a = QgsVectorLayer(new_patches_result,"new_patches_result")
    layer_a.startEditing()
    layer_provider_a=layer_a.dataProvider()
    layer_provider_a.addAttributes([QgsField('area', QVariant.Double, 'double', 20, 2)])
    layer_a.updateFields()
    for feature in layer_a.getFeatures():
        feature["area"] = feature.geometry().area()/10000.0
        layer_a.updateFeature(feature)
    
    layer_a.commitChanges()
    
    

path = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/processing/"
result_path = "C:/Dropbox (LANCIS)/cambio_cobertura_ca/v4_aptitud_evidence/patch_analysis/result/"
separa(path,result_path,1,3,2,"agro")
separa(path,result_path,1,3,4,"urb")
separa(path,result_path,1,3,9,"selva")
separa(path,result_path,1,3,7,"manglar")

separa(path,result_path,3,5,2,"agro")
separa(path,result_path,3,5,4,"urb")
separa(path,result_path,3,5,9,"selva")
separa(path,result_path,3,5,7,"manglar")

separa(path,result_path,5,6,2,"agro")
separa(path,result_path,5,6,4,"urb")
separa(path,result_path,5,6,9,"selva")
separa(path,result_path,5,6,7,"manglar")