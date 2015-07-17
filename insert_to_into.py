out_folder_path=r"C:\Users\Marcos\Dropbox\ANALISE_R_MESTRADO_MARCOS_UFRPE\DADOS_PAISAGEM\marcos_ufrpe\shp\SAD69_test"
out_nam='trash.gdb'
arcpy.CreateFileGDB_management(out_folder_path, out_nam)

output_file=r'C:\Users\Marcos\Dropbox\ANALISE_R_MESTRADO_MARCOS_UFRPE\DADOS_PAISAGEM\marcos_ufrpe\shp\SAD69_test\trash.gdb'


cur,row = None, None
cur = arcpy.SearchCursor("frags_SJ_MN_5")

x = 1

for row in cur:
    print row
    shp = row.getValue("SHAPE")

cur,row = None, None
cur = arcpy.InsertCursor("Arquivo_acumula_poligonos")
cont_lixo=0
for i in range(0,x):
    format='000'
    format=format+`cont_lixo`
    format=format[-4:]
    
    
    feat = cur.newRow()
    feat.shape = shp
    cur.insertRow(feat)
    arcpy.Intersect_analysis("Arquivo_acumula_poligonos #", output_file+'\lixo'+format, "ONLY_FID", "", "INPUT")
    arcpy.AddGeometryAttributes_management(output_file+'\lixo'+format, 'CENTROID', '#', '#', '#')
    
    cont_lixo=cont_lixo+1

#saida intersect
#C:\Users\Marcos\Dropbox\ANALISE_R_MESTRADO_MARCOS_UFRPE\DADOS_PAISAGEM\marcos_ufrpe\shp\SAD69_test\trash.gdb\lixo1