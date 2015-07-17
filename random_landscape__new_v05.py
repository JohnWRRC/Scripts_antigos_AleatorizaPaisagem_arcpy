import arcpy
from arcpy import env
import os
import sys
import arcpy.mapping
arcpy.env.overwriteOutput = True

def createDb(out_folder_path,out_nam):
    arcpy.CreateFileGDB_management(out_folder_path, out_nam)
    

def remove_layers():
    mxd = arcpy.mapping.MapDocument("CURRENT")
    
    # get the data frame    
    #df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
    
    # create a new layer
    #newlayer = arcpy.mapping.Layer(map)
    #arcpy.mapping.RemoveLayer(df,newlayer )
    for df in arcpy.mapping.ListDataFrames(mxd):
        for lyr in arcpy.mapping.ListLayers(mxd, "", df):
            if lyr.name.lower() == "frags_copy":
                arcpy.mapping.RemoveLayer(df, lyr)    
    
    
    arcpy.mapping.ListLayers(mxd, "", df)
   

def insert(frags_com_pacth):
    mxd = arcpy.mapping.MapDocument("CURRENT")

    # get the data frame    
    df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

    # create a new layer
    newlayer = arcpy.mapping.Layer(frags_com_pacth)

    # add the layer to the map at the bottom of the TOC in data frame 0
    arcpy.mapping.AddLayer(df, newlayer,"BOTTOM")
    


def insert_to(interserct_explod,arc_acumula):
    cur,row = None, None
    cur = arcpy.SearchCursor(interserct_explod)
    x = 1
    for row in cur:
        shp = row.getValue("SHAPE")    
        cur,row = None, None
        cur = arcpy.InsertCursor(arc_acumula)
        first_time_lixo=0
        for i in range(0,x): 
            feat = cur.newRow()
            feat.shape = shp
            cur.insertRow(feat)


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




def con_lines(intersect_01):
    first_timeador_lihas=0
    with arcpy.da.SearchCursor(intersect_01, "OBJECTID") as idtf:
        for idt in idtf:
            first_timeador_lihas=first_timeador_lihas+1
            
        
        return first_timeador_lihas
            





# troca pelo caminho da pasta##
#################################
########################
out_folder_path=r"E:\data_2015\___john\marcos_ufrpe\shp\SAD69_teste"
os.chdir(out_folder_path)
os.mkdir('Trash')

out_folder_path=out_folder_path+'\Trash'
env.workspace = out_folder_path

# criando banco pra jogar lixo


out_nam='trash0000.gdb'
arcpy.CreateFileGDB_management(out_folder_path, out_nam)

# caimho de saida dos lixos
output_file=out_folder_path+'/'+out_nam

#________________________________________

#mapa original
frags_ori="frags_SJ_MN_CLIP_v2"
#copiando arquivo

def copy_file_ori(frags_ori,output_file):
    arcpy.CopyFeatures_management(frags_ori, output_file+'/frags_copy')
    # nome do arquivo copia mais o caminho onde ele esta salvo
    frags_com_pacth=output_file+'/frags_copy'
    #apenas o nome do arquivo copia
    frags_sem_pacth='frags_copy'
    return frags_com_pacth, frags_sem_pacth

frags_com_pacth, frags_sem_pacth=copy_file_ori(frags_ori, output_file)

#_________________________________
#calculando centroids dos arquivo copiado



#shp intersect
# cuidado com os caminhos isso tem mudar pra variavel

def create_intersect(output_file,frags_com_pacth):
    env.workspace=output_file+'/'
    out_path = output_file+'/'
    shp_intersect ='shp_intersect'
    geometry_type = "POLYGON"
    template = frags_com_pacth
    has_m = "DISABLED"
    has_z = "DISABLED"
    spatial_reference = arcpy.Describe(frags_com_pacth).spatialReference
    arcpy.CreateFeatureclass_management(out_path,shp_intersect, geometry_type, template, has_m, has_z, spatial_reference)
    return shp_intersect
shp_intersect=create_intersect(output_file, frags_ori)
#___________________________________________________


#shp apoio
# cuidado com os caminhos isso tem mudar pra variavel
def shp_to_def(output_file,frags_com_pacth):
    env.workspace=output_file+'/'
    out_path = output_file+'/'
    out_name = 'shp_to'
    geometry_type = "POLYGON"
    template = frags_com_pacth
    has_m = "DISABLED"
    has_z = "DISABLED"
    spatial_reference = arcpy.Describe(frags_com_pacth).spatialReference
    arcpy.CreateFeatureclass_management(out_path,out_name, geometry_type, template, has_m, has_z, spatial_reference)
shp_to_def(output_file, frags_com_pacth)
#___________________________________________________


#____________________________________
#inserindo mapa no projeto para poder selecionar
insert(frags_com_pacth)
#__________




#___________________________________________________________________


env.workspace = out_folder_path




#definindo variavel 
shape_to_aleat=frags_sem_pacth

# declarando variavel
shp_to='shp_to'



limite_area='Limite_SJ_MN_original'
for db in range(100):
    frag_left=1
    
    first_time=1
    first_time_lixo=0    
    # criando um prefixo de nomes    
    format_name_db='0000'
    format_name_db=format_name_db+`db`
    format_name_db=format_name_db[-4:]      
    if db>0:
        out_nam='trash'+format_name_db+'.gdb'
        createDb(out_folder_path, out_nam)
        output_file=out_folder_path+'/'+out_nam
        frags_com_pacth, frags_sem_pacth=copy_file_ori(frags_ori, output_file)
        shp_intersect=create_intersect(output_file, frags_ori)
        shp_to_def(output_file, frags_com_pacth)
        insert(frags_com_pacth)
        env.workspace = out_folder_path
        
    
    
    while frag_left==1:
        # criadno centroid no arquivo a ser aleatorizado
        arcpy.AddGeometryAttributes_management(shape_to_aleat, 'CENTROID', '#', '#', '#')
        
        # criando area em metros arquivo a ser aleatorizado
        arcpy.AddGeometryAttributes_management(shape_to_aleat, "AREA","METERS","SQUARE_METERS")
        
        #coluna para ordenar pro fragmentos maiores
        arcpy.AddField_management(shape_to_aleat, "AR_SHORT", "DOUBLE", 20, 20)
        
        #expresao para criar coluna com valores negativos
        expressao='!POLY_AREA!*-1'
        
        # field calculator
        arcpy.CalculateField_management(shape_to_aleat,"AR_SHORT",expressao,"PYTHON_9.3","#")
        
        # ordenando o shp pela coluna AR_SHORT
        arcpy.Sort_management(shape_to_aleat,output_file+"/apoio_order",[["AR_SHORT","ASCENDING"]])
        
        # copiando o arquivo com o mesmo nome para voltar a ser o aleat
        arcpy.CopyFeatures_management(output_file+"/apoio_order",shape_to_aleat)    
        
        # inserindo o arquivo novamente no projeto
        insert(output_file+"/"+shape_to_aleat)
        
        # lendo tabela de atributos do shp a ser aleatorizado
        rows_frag = arcpy.SearchCursor(shape_to_aleat,fields="CENTROID_X;CENTROID_Y",sort_fields="AR_SHORT")
        
        
        # fazendo um laco nas linhas do arquivo shp
        for row in rows_frag:
            
            # criando um prefixo de nomes 
              
            
            
            # se first_time for igual a 1, o limite a serusado será o original definido pelo usuario
            if first_time==1:
                arcpy.CreateRandomPoints_management(output_file, 'pnt_rnd',limite_area, '', '1', '0 Meters', 'POINT', '0')
                arcpy.AddGeometryAttributes_management(output_file+'\'pnt_rnd', 'POINT_X_Y_Z_M', '#', '#', '#')
            
            # se nao, o limite a ser usado para sortear pontos vai ser o limite menos o poligono que foi acresentado na rodada anterior, e isso vai
            else:
                arcpy.Erase_analysis(limite_area, shape_to_aleat, output_file+'/new_limit', '#')
                arcpy.CreateRandomPoints_management(output_file, 'pnt_rnd',output_file+'/new_limit', '', '1', '0 Meters', 'POINT', '0')
                arcpy.AddGeometryAttributes_management(output_file+'\'pnt_rnd', 'POINT_X_Y_Z_M', '#', '#', '#')
                
            rows_rnd_pnt = arcpy.SearchCursor(output_file+"\pnt_rnd",
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
            
            arcpy.SelectLayerByAttribute_management(shape_to_aleat,"NEW_SELECTION",query)
            
            
            resultadoX=x_pnt-x_frag
            resultadoY=y_pnt-y_frag      
            
            shift_features(shape_to_aleat, x_shift=resultadoX, y_shift=resultadoY)
            insert_to(shape_to_aleat, output_file+'/'+shp_to)
            
            arcpy.Intersect_analysis(output_file+'/'+shp_to,output_file+'/'+shp_intersect+'_apoio', 'ALL', '#', 'INPUT')
            arcpy.Dissolve_management(output_file+'/'+shp_intersect+'_apoio',output_file+'/'+shp_intersect+'_apoio_diss', '#', '#', 'MULTI_PART', 'DISSOLVE_LINES') 
            arcpy.MultipartToSinglepart_management(output_file+'/'+shp_intersect+'_apoio_diss',output_file+'/'+shp_intersect+'_apoio_diss_exp')         
            count_intersect_lines=con_lines(output_file+'/'+shp_intersect+'_apoio_diss_exp')
            
            
            if count_intersect_lines>0:
                insert_to(output_file+'/'+shp_intersect+'_apoio_diss_exp',output_file+'/'+shp_intersect)
            
            arcpy.Dissolve_management(output_file+'/'+shp_to,output_file+'/'+shp_to+'_diss', '#', '#', 'MULTI_PART', 'DISSOLVE_LINES')   
            arcpy.MultipartToSinglepart_management(output_file+'/'+shp_to+'_diss',
                                                                output_file+'/'+shp_to+'_diss_exp')        
            
            arcpy.CopyFeatures_management(output_file+'/'+shp_to+'_diss_exp',output_file+'/'+shp_to)
            
            
            
            arcpy.SelectLayerByAttribute_management(shape_to_aleat,"CLEAR_SELECTION")
            
            first_time=0
            first_time_lixo=first_time_lixo+1
            
        #aasd
        arcpy.Erase_analysis(output_file+'/'+shp_to,limite_area, output_file+'/out_patchs', '#')
        
        insert_to(output_file+'/out_patchs',output_file+'/'+shp_intersect)
        
        count_intersect_lines=con_lines(output_file+'/'+shp_intersect)
        arcpy.Clip_analysis(output_file+'/'+shp_to,limite_area,output_file+'/temp_clip')
        arcpy.CopyFeatures_management(output_file+'/temp_clip',output_file+'/'+shp_to)
        if count_intersect_lines>0:
            
            insert(output_file+'/'+shp_intersect)
            arcpy.CopyFeatures_management(output_file+'/'+shp_intersect,output_file+'/'+shape_to_aleat)
            
            env.workspace=output_file+'/'
            out_path=output_file+'/'
            shp_intersect ='shp_intersect'
            geometry_type = "POLYGON"
            template = frags_com_pacth
            has_m = "DISABLED"
            has_z = "DISABLED"
            spatial_reference = arcpy.Describe(frags_com_pacth).spatialReference
            arcpy.CreateFeatureclass_management(out_path,shp_intersect, geometry_type, template, has_m, has_z, spatial_reference)        
            
            
            
        else:
            frag_left=0
            remove_layers()
            arcpy.CopyFeatures_management(output_file+'/'+shp_to,out_folder_path+'/'+frags_ori+'_random_'+format_name_db)
            #insert(out_folder_path+'/'+frags_ori+'_random_'+format_name_db+'.shp')
            
                
            
    
        

