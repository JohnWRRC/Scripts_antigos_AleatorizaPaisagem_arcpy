import arcpy
from arcpy import env


hexag="hex_5000"
AE_belem_flor="AE_belem_flor"


env.workspace=r'C:\Users\User\Documents\Projetos_2014\Cezar\Dados_Cezar\Hex_clipados_buffer_8k'

with arcpy.da.SearchCursor(hexag, "Unique_ID") as idtf:
    for idt in idtf:
        
        
        query="Unique_ID=%d"%idt
        formato='0000'+`idt[0]`
        formato=formato[-4:]
        #print query
        out_buffer=hexag+'_buffer_8k_hex_'+formato
        out_clip=AE_belem_flor+'_buffer_8k_clip_hex_'+formato
        buffer_inclip="C:\Users\User\Documents\Projetos_2014\Cezar\Dados_Cezar\Hex_clipados_buffer_8k\\"+out_buffer+'.shp'
        arcpy.SelectLayerByAttribute_management(hexag,"NEW_SELECTION",query)
        arcpy.Buffer_analysis(hexag,out_buffer,8000,"FULL","FLAT","NONE")
        arcpy.Clip_analysis(AE_belem_flor,buffer_inclip,out_clip,"")
        arcpy.SelectLayerByAttribute_management(hexag, "CLEAR_SELECTION")
        input_clipado="C:\Users\User\Documents\Projetos_2014\Cezar\Dados_Cezar\Hex_clipados_buffer_8k\\"+out_clip+'.shp'
        arcpy.DeleteField_management(input_clipado, ["area_ha"])
        arcpy.AddField_management(input_clipado, "Area_m2", "DOUBLE", 20, 20)
        arcpy.AddField_management(input_clipado, "Area_ha", "DOUBLE", 20, 20)            
        arcpy.CalculateField_management(input_clipado,"Area_m2","!shape.area@squaremeters!","PYTHON_9.3","#") 
        expressao='!Area_m2!/10000'
        arcpy.CalculateField_management(input_clipado,"area_ha",expressao,"PYTHON_9.3","#")            
