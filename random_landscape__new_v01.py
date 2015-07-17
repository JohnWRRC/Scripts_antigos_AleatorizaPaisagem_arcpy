import arcpy
from arcpy import env
import os
import sys
import arcpy.mapping
arcpy.env.overwriteOutput = True

#______________________________________________
def insert(frags_com_pacth):
    mxd = arcpy.mapping.MapDocument("CURRENT")

    # get the data frame    
    df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

    # create a new layer
    newlayer = arcpy.mapping.Layer(frags_com_pacth)

    # add the layer to the map at the bottom of the TOC in data frame 0
    arcpy.mapping.AddLayer(df, newlayer,"BOTTOM")


#____________________________________________________



def shift_features(in_features, x_shift=None, y_shift=None):
    
    """
    Shifts features by an x and/or y value. The shift values are in
    the units of the in_features coordinate system.
 
    Parameters:
    in_features: string
        An existing feature class or feature layer.  If using a
        feature layer with a selection, only the selected features
        will be modified.
 
    x_shift: float
        The distance the x coordinates will be shifted.
 
    y_shift: float
        The distance the y coordinates will be shifted.
    """
 
    with arcpy.da.UpdateCursor(in_features, ['SHAPE@XY']) as cursor:
        for row in cursor:
            cursor.updateRow([[row[0][0] + (x_shift or 0),
                               row[0][1] + (y_shift or 0)]])
 
    return


#________________________________________________________________________________________



# definindo local de trabalho
env.workspace = r"C:\Users\Marcos\Dropbox\ANALISE_R_MESTRADO_MARCOS_UFRPE\DADOS_PAISAGEM\marcos_ufrpe\shp\SAD69_test"

# criando banco pra jogar lixo
out_folder_path=r"C:\Users\Marcos\Dropbox\ANALISE_R_MESTRADO_MARCOS_UFRPE\DADOS_PAISAGEM\marcos_ufrpe\shp\SAD69_test"
out_nam='trash05.gdb'
arcpy.CreateFileGDB_management(out_folder_path, out_nam)

# caimho de saida dos lixos
output_file=r'C:\Users\Marcos\Dropbox\ANALISE_R_MESTRADO_MARCOS_UFRPE\DADOS_PAISAGEM\marcos_ufrpe\shp\SAD69_test\trash05.gdb'

#________________________________________

#mapa original
frags_ori="frags_SJ_MN_5"
#copiando arquivo
arcpy.CopyFeatures_management(frags_ori, output_file+'/frags_copy')
# nome do arquivo copia mais o caminho onde ele esta salvo
frags_com_pacth=output_file+'/frags_copy'
#apenas o nome do arquivo copia
frags_sem_pacth='frags_copy'

#_________________________________
#calculando centroids dos arquivo copiado

arcpy.AddGeometryAttributes_management(frags_com_pacth, 'CENTROID', '#', '#', '#')

#shp acumula
# cuidado com os caminhos isso tem mudar pra variavel
env.workspace=r'C:\Users\Marcos\Dropbox\ANALISE_R_MESTRADO_MARCOS_UFRPE\DADOS_PAISAGEM\marcos_ufrpe\shp\SAD69_test\trash05.gdb\\'
out_path = r'C:\Users\Marcos\Dropbox\ANALISE_R_MESTRADO_MARCOS_UFRPE\DADOS_PAISAGEM\marcos_ufrpe\shp\SAD69_test\trash05.gdb\\'
out_name = 'Acumula_frags_v01'
geometry_type = "POLYGON"
template = frags_com_pacth
has_m = "DISABLED"
has_z = "DISABLED"
spatial_reference = arcpy.Describe(frags_com_pacth).spatialReference
arcpy.CreateFeatureclass_management(out_path,out_name, geometry_type, template, has_m, has_z, spatial_reference)
#___________________________________________________

#cria intersect

out_path = out_folder_path
out_name = frags_ori+'_rnd.shp'
geometry_type = "POLYGON"
template = frags_com_pacth
has_m = "DISABLED"
has_z = "DISABLED"
spatial_reference = arcpy.Describe(frags_com_pacth).spatialReference
arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type, template, has_m, has_z, spatial_reference)



#____________________________________
#inserindo mapa para poder selecionar
insert(frags_com_pacth)
#__________




#___________________________________________________________________

env.workspace = r"C:\Users\Marcos\Dropbox\ANALISE_R_MESTRADO_MARCOS_UFRPE\DADOS_PAISAGEM\marcos_ufrpe\shp\SAD69_test"


# vai guardando os poligono que estao em interseccao



def insert_to(interserct_explod,arc_acumula):
    cur,row = None, None
    cur = arcpy.SearchCursor(interserct_explod)
    x = 1
    for row in cur:
        shp = row.getValue("SHAPE")    
        cur,row = None, None
        cur = arcpy.InsertCursor(arc_acumula)
        cont_lixo=0
        for i in range(0,x): 
            feat = cur.newRow()
            feat.shape = shp
            cur.insertRow(feat)
    
            
            





#

# contar linhas

def con_lines(intersect_01):
    contador_lihas=0
    with arcpy.da.SearchCursor(intersect_01, "OBJECTID") as idtf:
        for idt in idtf:
            contador_lihas=contador_lihas+1
            
        
        return contador_lihas
            







#









cont=0
cont_lixo=0

arcpy.AddGeometryAttributes_management(frags_com_pacth, "AREA","METERS","SQUARE_METERS")
arcpy.AddField_management(frags_com_pacth, "AR_SHORT", "DOUBLE", 20, 20)
expressao='!POLY_AREA!*-1'

arcpy.CalculateField_management(frags_com_pacth,"AR_SHORT",expressao,"PYTHON_9.3","#")
arcpy.Sort_management(frags_sem_pacth,output_file+"/apoio_order",[["AR_SHORT","ASCENDING"]])
arcpy.CopyFeatures_management(output_file+"/apoio_order",frags_com_pacth)

insert(frags_com_pacth)
rows_frag = arcpy.SearchCursor(frags_sem_pacth,fields="CENTROID_X;CENTROID_Y")







for row in rows_frag:
    
    format='000'
    format=format+`cont_lixo`
    format=format[-4:]    
    print format  
    
    if cont==0:
        arcpy.CreateRandomPoints_management(output_file, 'pnt_rnd'+format,'Limite_SJ_MN_original', '', '1', '0 Meters', 'POINT', '0')
        arcpy.AddGeometryAttributes_management(output_file+'\'pnt_rnd'+format, 'POINT_X_Y_Z_M', '#', '#', '#')
    else:
        arcpy.Erase_analysis('Limite_SJ_MN_original', frags_sem_pacth, output_file+'/new_limit'+format, '#')
        arcpy.CreateRandomPoints_management(output_file, 'pnt_rnd'+format,output_file+'/new_limit'+format, '', '1', '0 Meters', 'POINT', '0')
        arcpy.AddGeometryAttributes_management(output_file+'\'pnt_rnd'+format, 'POINT_X_Y_Z_M', '#', '#', '#')
        
    rows_rnd_pnt = arcpy.SearchCursor(output_file+"\pnt_rnd"+format,
                              fields="POINT_X;POINT_Y",
                              sort_fields="OID") 
    
    for getval in rows_rnd_pnt:
        x_pnt=getval.getValue("POINT_X")
        y_pnt=getval.getValue("POINT_Y")        
        
    
    #print FID_pnt
    x_frag=row.getValue("CENTROID_X")
    y_frag=row.getValue("CENTROID_Y")    
    FID=row.getValue("OBJECTID")
    query="OBJECTID=%d"%FID
    #print FID 
    
    arcpy.SelectLayerByAttribute_management(frags_sem_pacth,"NEW_SELECTION",query)
    
    
    resultadoX=x_pnt-x_frag
    resultadoY=y_pnt-y_frag
    
    
####acho que aqui, John, Deveriamos exportar esse frag selecionado e já movido para um novo ""shape"
#### e lá rodar o intersect e os demais arquivos. Oq acha?


    
    
    arcpy.Intersect_analysis(output_file+'/frags_copy',
                             output_file+'/intersect'+format, 'ALL', '#', 'INPUT')
    
    cont_lines_result=con_lines(output_file+'/intersect'+format)
    
    
    if cont_lines_result>0:
        arcpy.Dissolve_management(output_file+'/intersect'+format,
                                  output_file+'/intersect_diss'+format, '#', '#', 'MULTI_PART', 'DISSOLVE_LINES')
        
        arcpy.MultipartToSinglepart_management(output_file+'/intersect_diss'+format,
                                               output_file+'/intersect_diss_explod'+format)        
        insert_to(output_file+'/intersect_diss_explod'+format, output_file+'/Acumula_frags_v01')
        arcpy.AddGeometryAttributes_management(output_file+'/Acumula_frags_v01', 'CENTROID', '#', '#', '#')
    
    shift_features(frags_sem_pacth, x_shift=resultadoX, y_shift=resultadoY)
        
    arcpy.SelectLayerByAttribute_management(frags_sem_pacth,"CLEAR_SELECTION")
    
    cont=cont+1
    cont_lixo=cont_lixo+1
    

    