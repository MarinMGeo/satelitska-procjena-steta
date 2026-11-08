# Povijest geoprocesiranja iz ArcGIS Pro (Python export History). Putanje su skraćene na <PROJEKT>.
import arcpy
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="JLS",
    selection_type="NEW_SELECTION",
    where_clause="JLS_IME_HR = 'KARLOVAC' Or JLS_IME_HR = 'LASINJA' Or JLS_IME_HR = 'DUGA RESA' Or JLS_IME_HR = 'BARILOVIĆ'",
    invert_where_clause=None
)
arcpy.ImportToolbox(r"@\Analysis Tools.tbx")
arcpy.analysis.Statistics(
    in_table="ARKOD_2024_ekonomski_scenarij_kukuruz",
    out_table=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\ARKOD_2024_scenarij_kukuruz_ukupno",
    statistics_fields="gubitak_25 SUM;gubitak_50 SUM;gubitak_100 SUM",
    case_field=None,
    concatenation_separator=""
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateField(
    in_table="ARKOD_2024_ekonomski_scenarij_kukuruz",
    field="gubitak_100",
    expression="(!SUM_poplava_ha_1! or 0) * !prinos_t_ha! * !cijena_eur!",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateField(
    in_table="ARKOD_2024_ekonomski_scenarij_kukuruz",
    field="gubitak_50",
    expression="(!SUM_poplava_ha_1! or 0) * !prinos_t_ha! * !cijena_eur! * 0.50",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateField(
    in_table="ARKOD_2024_ekonomski_scenarij_kukuruz",
    field="gubitak_25",
    expression="(!SUM_poplava_ha_1! or 0) * !prinos_t_ha! * !cijena_eur! * 0.25",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateField(
    in_table="ARKOD_2024_ekonomski_scenarij",
    field="cijena_eur",
    expression="166.65",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateField(
    in_table="ARKOD_2024_ekonomski_scenarij",
    field="prinos_t_ha",
    expression="7.70",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.ImportToolbox(r"@\Conversion Tools.tbx")
arcpy.conversion.ExportFeatures(
    in_features=r"ARKOD\ARKOD_2024_analiza",
    out_features=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\ARKOD_2024_ekonomski_scenarij",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping=r'ogc_fid "ogc_fid" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,ogc_fid,-1,-1;id "id" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,id,-1,-1;land_use_i "land_use_i" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,land_use_i,-1,-1;home_name "home_name" true true false 60 Text 0 0,First,#,ARKOD\ARKOD_2024_analiza,home_name,0,59;area "area" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,area,-1,-1;perim "perim" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,perim,-1,-1;slope "slope" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,slope,-1,-1;z_avg "z_avg" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,z_avg,-1,-1;eligibilit "eligibilit" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,eligibilit,-1,-1;mines_stat "mines_stat" true true false 1 Text 0 0,First,#,ARKOD\ARKOD_2024_analiza,mines_stat,0,254;mines_year "mines_year" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_analiza,mines_year,-1,-1;water_prot "water_prot" true true false 10 Text 0 0,First,#,ARKOD\ARKOD_2024_analiza,water_prot,0,9;natura2000 "natura2000" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,natura2000,-1,-1;natura20_1 "natura20_1" true true false 20 Text 0 0,First,#,ARKOD\ARKOD_2024_analiza,natura20_1,0,19;natura20_2 "natura20_2" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,natura20_2,-1,-1;natura20_3 "natura20_3" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,natura20_3,-1,-1;anc "anc" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_analiza,anc,-1,-1;anc_area "anc_area" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,anc_area,-1,-1;rp "rp" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_analiza,rp,-1,-1;sanitary_p "sanitary_p" true true false 25 Text 0 0,First,#,ARKOD\ARKOD_2024_analiza,sanitary_p,0,24;tvpv "tvpv" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_analiza,tvpv,-1,-1;ot_nat "ot_nat" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_analiza,ot_nat,-1,-1;ot_nat_are "ot_nat_are" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,ot_nat_are,-1,-1;irrigation "irrigation" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_analiza,irrigation,-1,-1;irrigati_1 "irrigati_1" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_analiza,irrigati_1,-1,-1;irrigati_2 "irrigati_2" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_analiza,irrigati_2,-1,-1;ARKOD_ha "ARKOD_ha" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,ARKOD_ha,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,Shape_Area,-1,-1;SUM_poplava_ha "SUM_poplava_ha" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,SUM_poplava_ha,-1,-1;postotak_poplavljenosti "postotak_poplavljenosti" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,postotak_poplavljenosti,-1,-1;SUM_poplava_ha_1 "SUM_poplava_ha_filtri" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,SUM_poplava_ha_1,-1,-1;posto_poplavljenosti_filtri "posto_poplavljenosti_filtri" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_analiza,posto_poplavljenosti_filtri,-1,-1;razred_poplavljenost "razred_poplavljenost" true true false 2 Short 0 0,First,#,ARKOD\ARKOD_2024_analiza,razred_poplavljenost,-1,-1',
    sort_field=None
)
arcpy.ImportToolbox(r"@\Analysis Tools.tbx")
arcpy.analysis.Statistics(
    in_table=r"ARKOD\ARKOD_2024_analiza",
    out_table=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\ARKOD_2024_statistika_razredi_filtrirano",
    statistics_fields="SUM_poplava_ha_1 SUM",
    case_field="razred_poplavljenost",
    concatenation_separator=""
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateField(
    in_table=r"ARKOD\ARKOD_2024_analiza",
    field="razred_poplavljenost",
    expression="klasa(!posto_poplavljenosti_filtri!)",
    expression_type="PYTHON3",
    code_block="""def klasa(p):
    if p is None:
        return None
    if p <= 0:
        return 0
    if p <= 25:
        return 1
    if p <= 50:
        return 2
    if p <= 75:
        return 3
    return 4""",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateField(
    in_table=r"ARKOD\ARKOD_2024_analiza",
    field="posto_poplavljenosti_filtri",
    expression="""round(
    100 * (!SUM_poplava_ha_1! or 0) / !ARKOD_ha!,
    2
) if !ARKOD_ha! and !ARKOD_ha! > 0 else None""",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.JoinField(
    in_data=r"ARKOD\ARKOD_2024_analiza",
    in_field="id",
    join_table="ARKOD_2024_poplava_filtrirano_SUM",
    join_field="id",
    fields="SUM_poplava_ha",
    fm_option="NOT_USE_FM",
    field_mapping=None,
    index_join_fields="NO_INDEXES"
)
arcpy.ImportToolbox(r"@\Analysis Tools.tbx")
arcpy.analysis.Statistics(
    in_table="ARKOD_2024_poplava_vremenska_filtrirano_presjek",
    out_table=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\ARKOD_2024_poplava_filtrirano_SUM",
    statistics_fields="poplava_ha SUM",
    case_field="id",
    concatenation_separator=""
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateGeometryAttributes(
    in_features="ARKOD_2024_poplava_vremenska_filtrirano_presjek",
    geometry_property="poplava_ha AREA",
    length_unit="",
    area_unit="HECTARES",
    coordinate_system='PROJCS["HTRS96_Croatia_TM",GEOGCS["GCS_HTRS96",DATUM["D_Croatian_Terrestrial_Reference_System",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",16.5],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
    coordinate_format="SAME_AS_INPUT"
)
arcpy.ImportToolbox(r"@\Analysis Tools.tbx")
arcpy.analysis.PairwiseIntersect(
    in_features=r"ARKOD\ARKOD_2024_analiza;poplava\S1A_VV_17_5_23_poplava_vremenska_poligoni_filtrirano_005ha_radna_verzija",
    out_feature_class=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\ARKOD_2024_poplava_vremenska_filtrirano_presjek",
    join_attributes="ALL",
    cluster_tolerance=None,
    output_type="INPUT"
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateField(
    in_table=r"ARKOD\ARKOD_2024_analiza",
    field="postotak_poplavljenosti",
    expression="""round(
    100 * (!SUM_poplava_ha! or 0) / !ARKOD_ha!,
    2
) if !ARKOD_ha! and !ARKOD_ha! > 0 else None""",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.JoinField(
    in_data=r"ARKOD\ARKOD_2024_analiza",
    in_field="id",
    join_table="ARKOD_2024_poplava_SUM",
    join_field="id",
    fields="SUM_poplava_ha",
    fm_option="NOT_USE_FM",
    field_mapping=None,
    index_join_fields="NO_INDEXES"
)
arcpy.ImportToolbox(r"@\Analysis Tools.tbx")
arcpy.analysis.Statistics(
    in_table="ARKOD_2024_poplava_vremenska_presjek",
    out_table=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\ARKOD_2024_poplava_SUM",
    statistics_fields="poplava_ha SUM",
    case_field="id",
    concatenation_separator=""
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view=r"ARKOD\ARKOD_2024_podrucje_istrazivanja_3km",
    selection_type="NEW_SELECTION",
    where_clause="home_name = 'POLOJAC'",
    invert_where_clause=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view=r"ARKOD\ARKOD_2024_podrucje_istrazivanja_3km",
    selection_type="NEW_SELECTION",
    where_clause="home_name = 'POLJAC'",
    invert_where_clause=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateGeometryAttributes(
    in_features="ARKOD_2024_poplava_vremenska_presjek",
    geometry_property="poplava_ha AREA",
    length_unit="",
    area_unit="HECTARES",
    coordinate_system='PROJCS["HTRS96_Croatia_TM",GEOGCS["GCS_HTRS96",DATUM["D_Croatian_Terrestrial_Reference_System",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",16.5],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
    coordinate_format="SAME_AS_INPUT"
)
arcpy.ImportToolbox(r"@\Analysis Tools.tbx")
arcpy.analysis.PairwiseIntersect(
    in_features=r"ARKOD\ARKOD_2024_analiza;poplava\S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija",
    out_feature_class=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\ARKOD_2024_poplava_vremenska_presjek",
    join_attributes="ALL",
    cluster_tolerance=None,
    output_type="INPUT"
)
arcpy.ImportToolbox(r"@\Conversion Tools.tbx")
arcpy.conversion.ExportFeatures(
    in_features=r"ARKOD\ARKOD_2024_podrucje_istrazivanja_3km",
    out_features=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\ARKOD_2024_analiza",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping=r'ogc_fid "ogc_fid" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,ogc_fid,-1,-1;id "id" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,id,-1,-1;land_use_i "land_use_i" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,land_use_i,-1,-1;home_name "home_name" true true false 60 Text 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,home_name,0,59;area "area" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,area,-1,-1;perim "perim" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,perim,-1,-1;slope "slope" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,slope,-1,-1;z_avg "z_avg" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,z_avg,-1,-1;eligibilit "eligibilit" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,eligibilit,-1,-1;mines_stat "mines_stat" true true false 1 Text 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,mines_stat,0,254;mines_year "mines_year" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,mines_year,-1,-1;water_prot "water_prot" true true false 10 Text 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,water_prot,0,9;natura2000 "natura2000" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,natura2000,-1,-1;natura20_1 "natura20_1" true true false 20 Text 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,natura20_1,0,19;natura20_2 "natura20_2" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,natura20_2,-1,-1;natura20_3 "natura20_3" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,natura20_3,-1,-1;anc "anc" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,anc,-1,-1;anc_area "anc_area" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,anc_area,-1,-1;rp "rp" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,rp,-1,-1;sanitary_p "sanitary_p" true true false 25 Text 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,sanitary_p,0,24;tvpv "tvpv" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,tvpv,-1,-1;ot_nat "ot_nat" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,ot_nat,-1,-1;ot_nat_are "ot_nat_are" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,ot_nat_are,-1,-1;irrigation "irrigation" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,irrigation,-1,-1;irrigati_1 "irrigati_1" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,irrigati_1,-1,-1;irrigati_2 "irrigati_2" true true false 4 Long 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,irrigati_2,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,Shape_Area,-1,-1;ARKOD_ha "ARKOD_ha" true true false 8 Double 0 0,First,#,ARKOD\ARKOD_2024_podrucje_istrazivanja_3km,ARKOD_ha,-1,-1',
    sort_field=None
)
arcpy.ImportToolbox(r"@\Analysis Tools.tbx")
arcpy.analysis.Frequency(
    in_table=r"ARKOD\ARKOD_2024_podrucje_istrazivanja_3km",
    out_table=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\ARKOD_2024_provjera_id",
    frequency_fields="id",
    summary_fields=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateGeometryAttributes(
    in_features=r"ARKOD\ARKOD_2024_podrucje_istrazivanja_3km",
    geometry_property="ARKOD_ha AREA",
    length_unit="",
    area_unit="HECTARES",
    coordinate_system='PROJCS["HTRS96_Croatia_TM",GEOGCS["GCS_HTRS96",DATUM["D_Croatian_Terrestrial_Reference_System",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",16.5],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
    coordinate_format="SAME_AS_INPUT"
)
arcpy.ImportToolbox(r"@\Conversion Tools.tbx")
arcpy.conversion.ExportFeatures(
    in_features="arkod_sve_parcele selection",
    out_features=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\ARKOD_2024_podrucje_istrazivanja_3km",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='ogc_fid "ogc_fid" true true false 20 Double 0 20,First,#,arkod_sve_parcele selection,ogc_fid,-1,-1;id "id" true true false 20 Double 0 20,First,#,arkod_sve_parcele selection,id,-1,-1;land_use_i "land_use_i" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,land_use_i,-1,-1;home_name "home_name" true true false 60 Text 0 0,First,#,arkod_sve_parcele selection,home_name,0,59;area "area" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,area,-1,-1;perim "perim" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,perim,-1,-1;slope "slope" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,slope,-1,-1;z_avg "z_avg" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,z_avg,-1,-1;eligibilit "eligibilit" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,eligibilit,-1,-1;mines_stat "mines_stat" true true false 1 Text 0 0,First,#,arkod_sve_parcele selection,mines_stat,0,254;mines_year "mines_year" true true false 10 Long 0 10,First,#,arkod_sve_parcele selection,mines_year,-1,-1;water_prot "water_prot" true true false 10 Text 0 0,First,#,arkod_sve_parcele selection,water_prot,0,9;natura2000 "natura2000" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,natura2000,-1,-1;natura20_1 "natura20_1" true true false 20 Text 0 0,First,#,arkod_sve_parcele selection,natura20_1,0,19;natura20_2 "natura20_2" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,natura20_2,-1,-1;natura20_3 "natura20_3" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,natura20_3,-1,-1;anc "anc" true true false 10 Long 0 10,First,#,arkod_sve_parcele selection,anc,-1,-1;anc_area "anc_area" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,anc_area,-1,-1;rp "rp" true true false 10 Long 0 10,First,#,arkod_sve_parcele selection,rp,-1,-1;sanitary_p "sanitary_p" true true false 25 Text 0 0,First,#,arkod_sve_parcele selection,sanitary_p,0,24;tvpv "tvpv" true true false 10 Long 0 10,First,#,arkod_sve_parcele selection,tvpv,-1,-1;ot_nat "ot_nat" true true false 10 Long 0 10,First,#,arkod_sve_parcele selection,ot_nat,-1,-1;ot_nat_are "ot_nat_are" true true false 24 Double 15 23,First,#,arkod_sve_parcele selection,ot_nat_are,-1,-1;irrigation "irrigation" true true false 10 Long 0 10,First,#,arkod_sve_parcele selection,irrigation,-1,-1;irrigati_1 "irrigati_1" true true false 10 Long 0 10,First,#,arkod_sve_parcele selection,irrigati_1,-1,-1;irrigati_2 "irrigati_2" true true false 10 Long 0 10,First,#,arkod_sve_parcele selection,irrigati_2,-1,-1',
    sort_field=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.SelectLayerByLocation(
    in_layer="arkod_sve_parcele",
    overlap_type="INTERSECT",
    select_features=r"podrucje_istrazivanja\podrucje_istrazivanja_3km",
    search_distance=None,
    selection_type="NEW_SELECTION",
    invert_spatial_relationship="NOT_INVERT"
)
arcpy.ImportToolbox(r"@\Conversion Tools.tbx")
arcpy.conversion.ExportFeatures(
    in_features=r"poplava\S1A_VV_17_5_23_poplava_vremenska_poligoni_filtrirano_005ha",
    out_features=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_poplava_vremenska_poligoni_filtrirano_005ha_radna_verzija",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping=r'Id "Id" true true false 4 Long 0 0,First,#,poplava\S1A_VV_17_5_23_poplava_vremenska_poligoni_filtrirano_005ha,Id,-1,-1;gridcode "gridcode" true true false 4 Long 0 0,First,#,poplava\S1A_VV_17_5_23_poplava_vremenska_poligoni_filtrirano_005ha,gridcode,-1,-1;povrsina_ha "povrsina_ha" true true false 8 Double 0 0,First,#,poplava\S1A_VV_17_5_23_poplava_vremenska_poligoni_filtrirano_005ha,povrsina_ha,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,poplava\S1A_VV_17_5_23_poplava_vremenska_poligoni_filtrirano_005ha,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,poplava\S1A_VV_17_5_23_poplava_vremenska_poligoni_filtrirano_005ha,Shape_Area,-1,-1',
    sort_field=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.DefineProjection(
    in_dataset="arkod_sve_parcele",
    coor_system='PROJCS["HTRS96_Croatia_TM",GEOGCS["GCS_HTRS96",DATUM["D_Croatian_Terrestrial_Reference_System",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",16.5],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.Project(
    in_dataset="arkod_sve_parcele",
    out_dataset=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\arkod_sve_parcele_htrs96tm",
    out_coor_system='PROJCS["HTRS96_Croatia_TM",GEOGCS["GCS_HTRS96",DATUM["D_Croatian_Terrestrial_Reference_System",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",16.5],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
    transform_method=None,
    in_coor_system='PROJCS["WGS_1984_ARC_System_Zone_01",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Equidistant_Cylindrical"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",22.94791772],UNIT["Meter",1.0]]',
    preserve_shape="NO_PRESERVE_SHAPE",
    max_deviation=None,
    vertical="NO_VERTICAL"
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.DefineProjection(
    in_dataset="arkod_sve_parcele",
    coor_system='PROJCS["WGS_1984_ARC_System_Zone_01",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Equidistant_Cylindrical"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",22.94791772],UNIT["Meter",1.0]]'
)
arcpy.ImportToolbox(r"@\Conversion Tools.tbx")
arcpy.conversion.ExportFeatures(
    in_features="S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija",
    out_features=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_poplava_vremenska_poligoni_filtrirano_005ha",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='Id "Id" true true false 4 Long 0 0,First,#,S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija,Id,-1,-1;gridcode "gridcode" true true false 4 Long 0 0,First,#,S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija,gridcode,-1,-1;povrsina_ha "povrsina_ha" true true false 8 Double 0 0,First,#,S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija,povrsina_ha,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija,Shape_Area,-1,-1',
    sort_field=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija",
    selection_type="NEW_SELECTION",
    where_clause="povrsina_ha >= 0.05",
    invert_where_clause=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija",
    selection_type="NEW_SELECTION",
    where_clause="povrsina_ha < 0.05",
    invert_where_clause=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija",
    selection_type="NEW_SELECTION",
    where_clause="povrsina_ha < 5",
    invert_where_clause=None
)
arcpy.ImportToolbox(r"@\Conversion Tools.tbx")
arcpy.conversion.ExportFeatures(
    in_features="S1A_VV_17_5_23_poplava_vremenska_poligoni",
    out_features=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_poplava_vremenska_poligoni_radna_verzija",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='Id "Id" true true false 4 Long 0 0,First,#,S1A_VV_17_5_23_poplava_vremenska_poligoni,Id,-1,-1;gridcode "gridcode" true true false 4 Long 0 0,First,#,S1A_VV_17_5_23_poplava_vremenska_poligoni,gridcode,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,S1A_VV_17_5_23_poplava_vremenska_poligoni,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,S1A_VV_17_5_23_poplava_vremenska_poligoni,Shape_Area,-1,-1;povrsina_ha "povrsina_ha" true true false 8 Double 0 0,First,#,S1A_VV_17_5_23_poplava_vremenska_poligoni,povrsina_ha,-1,-1',
    sort_field=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="S1A_VV_17_5_23_poplava_vremenska_poligoni",
    selection_type="NEW_SELECTION",
    where_clause="povrsina_ha < 5",
    invert_where_clause=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateGeometryAttributes(
    in_features="S1A_VV_17_5_23_poplava_vremenska_poligoni",
    geometry_property="povrsina_ha AREA",
    length_unit="",
    area_unit="HECTARES",
    coordinate_system='PROJCS["HTRS96_Croatia_TM",GEOGCS["GCS_HTRS96",DATUM["D_Croatian_Terrestrial_Reference_System",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",16.5],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
    coordinate_format="SAME_AS_INPUT"
)
arcpy.ImportToolbox(r"@\Conversion Tools.tbx")
with arcpy.EnvManager(outputZFlag="Disabled", outputMFlag="Disabled"):
    arcpy.conversion.RasterToPolygon(
        in_raster="S1A_VV_17_5_23_poplava_vremenska_detekcija_samo1",
        out_polygon_features=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_poplava_vremenska_poligoni",
        simplify="NO_SIMPLIFY",
        raster_field="Value",
        create_multipart_features="SINGLE_OUTER_PART",
        max_vertices_per_feature=None
    )
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression='SetNull(   "S1A_VV_17_5_23_poplava_vremenska_detekcija"  == 0,   "S1A_VV_17_5_23_poplava_vremenska_detekcija" )'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_poplava_vremenska_detekcija_samo1")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(outputCoordinateSystem='PROJCS["HTRS96_Croatia_TM",GEOGCS["GCS_HTRS96",DATUM["D_Croatian_Terrestrial_Reference_System",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",16.5],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', snapRaster=r"S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB", extent='410027.82 5007050.1946 458067.94 5054721.6854 PROJCS["HTRS96_Croatia_TM".GEOGCS["GCS_HTRS96".DATUM["D_Croatian_Terrestrial_Reference_System".SPHEROID["GRS_1980".6378137.0.298.257222101]].PRIMEM["Greenwich".0.0].UNIT["Degree".0.0174532925199433]].PROJECTION["Transverse_Mercator"].PARAMETER["False_Easting".500000.0].PARAMETER["False_Northing".0.0].PARAMETER["Central_Meridian".16.5].PARAMETER["Scale_Factor".0.9999].PARAMETER["Latitude_Of_Origin".0.0].UNIT["Meter".1.0]]', cellSize=10, scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression='SetNull(    ("occurrence_10E_50N_v1_5_2024.tif" < 1) |    ("occurrence_10E_50N_v1_5_2024.tif" > 100),   "occurrence_10E_50N_v1_5_2024.tif" )'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\GSW_pojavljivanje_vode")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(outputCoordinateSystem='PROJCS["HTRS96_Croatia_TM",GEOGCS["GCS_HTRS96",DATUM["D_Croatian_Terrestrial_Reference_System",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",16.5],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', snapRaster=r"S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB", extent='410027.82 5007050.1946 458067.94 5054721.6854 PROJCS["HTRS96_Croatia_TM".GEOGCS["GCS_HTRS96".DATUM["D_Croatian_Terrestrial_Reference_System".SPHEROID["GRS_1980".6378137.0.298.257222101]].PRIMEM["Greenwich".0.0].UNIT["Degree".0.0174532925199433]].PROJECTION["Transverse_Mercator"].PARAMETER["False_Easting".500000.0].PARAMETER["False_Northing".0.0].PARAMETER["Central_Meridian".16.5].PARAMETER["Scale_Factor".0.9999].PARAMETER["Latitude_Of_Origin".0.0].UNIT["Meter".1.0]]', cellSize=10, scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression='Con(    ("occurrence_10E_50N_v1_5_2024.tif" >= 90) &    ("occurrence_10E_50N_v1_5_2024.tif" <= 100),    1,    0)'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\GSW_stalne_vode")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(outputCoordinateSystem='PROJCS["HTRS96_Croatia_TM",GEOGCS["GCS_HTRS96",DATUM["D_Croatian_Terrestrial_Reference_System",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",16.5],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', snapRaster=r"S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB", extent='410027.82 5007050.1946 458067.94 5054721.6854 PROJCS["HTRS96_Croatia_TM".GEOGCS["GCS_HTRS96".DATUM["D_Croatian_Terrestrial_Reference_System".SPHEROID["GRS_1980".6378137.0.298.257222101]].PRIMEM["Greenwich".0.0].UNIT["Degree".0.0174532925199433]].PROJECTION["Transverse_Mercator"].PARAMETER["False_Easting".500000.0].PARAMETER["False_Northing".0.0].PARAMETER["Central_Meridian".16.5].PARAMETER["Scale_Factor".0.9999].PARAMETER["Latitude_Of_Origin".0.0].UNIT["Meter".1.0]]', cellSize=10, scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression='Con(   "occurrence_10E_50N_v1_5_2024.tif"  >= 90,    1,    0)'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\GSW_stalne_vode_probno")
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster="occurrence_10E_50N_v1_5_2024.tif",
    location_point="427775 5040492",
    band_index=1
)
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=r'Con(    ("S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB" < -16) &    ("rasteri_promjene\S1A_razlika_VV_17_5_5_23" < -3) &    ("rasteri_promjene\S1A_razlika_VV_29_17_5_23" > 3),    1,    0)'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_poplava_vremenska_detekcija")
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster=r"rasteri_promjene\S1A_razlika_VV_29_17_5_23",
    location_point="428100 5039349",
    band_index=1
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster=r"rasteri_promjene\S1A_razlika_VV_29_17_5_23",
    location_point="427514 5040344",
    band_index=1
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster=r"rasteri_promjene\S1A_razlika_VV_29_17_5_23",
    location_point="427775 5040492",
    band_index=1
)
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=r'Con(    ("S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB" < -14) &    ("rasteri_promjene\S1A_razlika_VV_17_5_5_23" < -2),    1, 0)'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_poplava_blago_probno")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=r'Con(    ("S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB" < -19) &    ("rasteri_promjene\S1A_razlika_VV_17_5_5_23" < -5),    1, 0)'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_poplava_strogo_probno")
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster="S1A_VV_17_5_23_poplava_probno",
    location_point="428100 5039349",
    band_index=1
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster="S1A_VV_17_5_23_poplava_probno",
    location_point="427775 5040492",
    band_index=1
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster="S1A_VV_17_5_23_poplava_probno",
    location_point="427514 5040344",
    band_index=1
)
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression='SetNull("S1A_VV_17_5_23_poplava_probno" == 0, "S1A_VV_17_5_23_poplava_probno")'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_prikaz_poplave_probno")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(outputCoordinateSystem='PROJCS["HTRS96_Croatia_TM",GEOGCS["GCS_HTRS96",DATUM["D_Croatian_Terrestrial_Reference_System",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",16.5],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', snapRaster=r"S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB", extent="MINOF", cellSize=r"S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB", scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=r'Con(    ("S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB" < -16) &    ("rasteri_promjene\S1A_razlika_VV_17_5_5_23" < -3),    1,    0)'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_poplava_probno")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=r'Con(    ("S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB" < -16) &    ("rasteri_promjene\S1A_razlika_VV_17_5_5_23" < -3),    1,    0)'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_poplava_probno")
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster=r"rasteri_promjene\S1A_razlika_VV_17_5_5_23",
    location_point="427514 5040344",
    band_index=1
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster=r"rasteri_promjene\S1A_razlika_VV_17_5_5_23",
    location_point="427775 5040492",
    band_index=1
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster=r"rasteri_promjene\S1A_razlika_VV_17_5_5_23",
    location_point="428100 5039349",
    band_index=1
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster=r"S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB",
    location_point="428100 5039349",
    band_index=1
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster=r"S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB",
    location_point="427514 5040344",
    band_index=1
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster=r"S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB",
    location_point="427775 5040492",
    band_index=1
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.GetCellValue(
    in_raster=r"S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB",
    location_point="1774 1424",
    band_index=1
)
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r' "S1A_29_5_2023\S1A_VV_29_5_23_izrezano_dB" - "S1A_5_5_2023\S1A_VV_5_5_23_izrezano_dB"'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_razlika_VV_29_5_5_23")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r' "S1A_29_5_2023\S1A_VH_29_5_23_izrezano_dB" -  "S1A_5_5_2023\S1A_VH_5_5_23_izrezano_dB"'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_razlika_VH_29_5_5_23")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r' "S1A_29_5_2023\S1A_VH_29_5_23_izrezano_dB" - "S1A_17_5_2023\S1A_VH_17_5_23_izrezano_dB"'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_razlika_VH_29_17_5_23")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r' "S1A_29_5_2023\S1A_VV_29_5_23_izrezano_dB" - "S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB"'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_razlika_VV_29_17_5_23")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r' "S1A_17_5_2023\S1A_VV_17_5_23_izrezano_dB" -  "S1A_5_5_2023\S1A_VV_5_5_23_izrezano_dB"'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_razlika_VV_17_5_5_23")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r' "S1A_17_5_2023\S1A_VH_17_5_23_izrezano_dB" - "S1A_5_5_2023\S1A_VH_5_5_23_izrezano_dB"'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_razlika_VH_17_5_5_23")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r'10 * Log10(SetNull("S1A_29_5_2023\S1A_VV_29_5_23_izrezano" <= 0, "S1A_29_5_2023\S1A_VV_29_5_23_izrezano"))'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_29_5_23_izrezano_dB")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r'10 * Log10(SetNull("S1A_29_5_2023\S1A_VH_29_5_23_izrezano" <= 0, "S1A_29_5_2023\S1A_VH_29_5_23_izrezano"))'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VH_29_5_23_izrezano_dB")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r'10 * Log10(SetNull("S1A_17_5_2023\S1A_VV_17_5_23_izrezano" <= 0, "S1A_17_5_2023\S1A_VV_17_5_23_izrezano"))'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_izrezano_dB")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r'10 * Log10(SetNull("S1A_17_5_2023\S1A_VH_17_5_23_izrezano" <= 0, "S1A_17_5_2023\S1A_VH_17_5_23_izrezano"))'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VH_17_5_23_izrezano_dB")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r'10 * Log10(SetNull("S1A_5_5_2023\S1A_VV_5_5_23_izrezano" <= 0, "S1A_5_5_2023\S1A_VV_5_5_23_izrezano"))'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_5_5_23_izrezano_dB")
arcpy.ImportToolbox(r"@\Image Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    output_raster = arcpy.ia.RasterCalculator(
        expression=r'10 * Log10(SetNull("S1A_5_5_2023\S1A_VH_5_5_23_izrezano" <= 0, "S1A_5_5_2023\S1A_VH_5_5_23_izrezano"))'
    )
    output_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VH_5_5_23_izrezano_dB")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster=r"S1A_29_5_2023\S1A_VV_29_5_23",
        in_mask_data=r"podrucje_istrazivanja\podrucje_istrazivanja_3km",
        extraction_area="INSIDE",
        analysis_extent='410027.82 5007050.1946 458067.94 5054721.6854 PROJCS["HTRS96_Croatia_TM".GEOGCS["GCS_HTRS96".DATUM["D_Croatian_Terrestrial_Reference_System".SPHEROID["GRS_1980".6378137.0.298.257222101]].PRIMEM["Greenwich".0.0].UNIT["Degree".0.0174532925199433]].PROJECTION["Transverse_Mercator"].PARAMETER["False_Easting".500000.0].PARAMETER["False_Northing".0.0].PARAMETER["Central_Meridian".16.5].PARAMETER["Scale_Factor".0.9999].PARAMETER["Latitude_Of_Origin".0.0].UNIT["Meter".1.0]]'
    )
    out_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_29_5_23_izrezano")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster=r"S1A_29_5_2023\S1A_VH_29_5_23",
        in_mask_data=r"podrucje_istrazivanja\podrucje_istrazivanja_3km",
        extraction_area="INSIDE",
        analysis_extent='410027.82 5007050.1946 458067.94 5054721.6854 PROJCS["HTRS96_Croatia_TM".GEOGCS["GCS_HTRS96".DATUM["D_Croatian_Terrestrial_Reference_System".SPHEROID["GRS_1980".6378137.0.298.257222101]].PRIMEM["Greenwich".0.0].UNIT["Degree".0.0174532925199433]].PROJECTION["Transverse_Mercator"].PARAMETER["False_Easting".500000.0].PARAMETER["False_Northing".0.0].PARAMETER["Central_Meridian".16.5].PARAMETER["Scale_Factor".0.9999].PARAMETER["Latitude_Of_Origin".0.0].UNIT["Meter".1.0]]'
    )
    out_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VH_29_5_23_izrezano")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster=r"S1A_17_5_2023\S1A_VV_17_5_23",
        in_mask_data=r"podrucje_istrazivanja\podrucje_istrazivanja_3km",
        extraction_area="INSIDE",
        analysis_extent='410027.82 5007050.1946 458067.94 5054721.6854 PROJCS["HTRS96_Croatia_TM".GEOGCS["GCS_HTRS96".DATUM["D_Croatian_Terrestrial_Reference_System".SPHEROID["GRS_1980".6378137.0.298.257222101]].PRIMEM["Greenwich".0.0].UNIT["Degree".0.0174532925199433]].PROJECTION["Transverse_Mercator"].PARAMETER["False_Easting".500000.0].PARAMETER["False_Northing".0.0].PARAMETER["Central_Meridian".16.5].PARAMETER["Scale_Factor".0.9999].PARAMETER["Latitude_Of_Origin".0.0].UNIT["Meter".1.0]]'
    )
    out_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_17_5_23_izrezano")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster=r"S1A_17_5_2023\S1A_VH_17_5_23",
        in_mask_data=r"podrucje_istrazivanja\podrucje_istrazivanja_3km",
        extraction_area="INSIDE",
        analysis_extent='410027.82 5007050.1946 458067.94 5054721.6854 PROJCS["HTRS96_Croatia_TM".GEOGCS["GCS_HTRS96".DATUM["D_Croatian_Terrestrial_Reference_System".SPHEROID["GRS_1980".6378137.0.298.257222101]].PRIMEM["Greenwich".0.0].UNIT["Degree".0.0174532925199433]].PROJECTION["Transverse_Mercator"].PARAMETER["False_Easting".500000.0].PARAMETER["False_Northing".0.0].PARAMETER["Central_Meridian".16.5].PARAMETER["Scale_Factor".0.9999].PARAMETER["Latitude_Of_Origin".0.0].UNIT["Meter".1.0]]'
    )
    out_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VH_17_5_23_izrezano")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster=r"S1A_5_5_2023\S1A_VV_5_5_23",
        in_mask_data=r"podrucje_istrazivanja\podrucje_istrazivanja_3km",
        extraction_area="INSIDE",
        analysis_extent='410027.82 5007050.1946 458067.94 5054721.6854 PROJCS["HTRS96_Croatia_TM".GEOGCS["GCS_HTRS96".DATUM["D_Croatian_Terrestrial_Reference_System".SPHEROID["GRS_1980".6378137.0.298.257222101]].PRIMEM["Greenwich".0.0].UNIT["Degree".0.0174532925199433]].PROJECTION["Transverse_Mercator"].PARAMETER["False_Easting".500000.0].PARAMETER["False_Northing".0.0].PARAMETER["Central_Meridian".16.5].PARAMETER["Scale_Factor".0.9999].PARAMETER["Latitude_Of_Origin".0.0].UNIT["Meter".1.0]]'
    )
    out_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VV_5_5_23_izrezano")
arcpy.ImportToolbox(r"@\Spatial Analyst Tools.tbx")
with arcpy.EnvManager(scratchWorkspace=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster=r"S1A_5_5_2023\S1A_VH_5_5_23",
        in_mask_data=r"podrucje_istrazivanja\podrucje_istrazivanja_3km",
        extraction_area="INSIDE",
        analysis_extent='410027.82 5007050.1946 458067.94 5054721.6854 PROJCS["HTRS96_Croatia_TM".GEOGCS["GCS_HTRS96".DATUM["D_Croatian_Terrestrial_Reference_System".SPHEROID["GRS_1980".6378137.0.298.257222101]].PRIMEM["Greenwich".0.0].UNIT["Degree".0.0174532925199433]].PROJECTION["Transverse_Mercator"].PARAMETER["False_Easting".500000.0].PARAMETER["False_Northing".0.0].PARAMETER["Central_Meridian".16.5].PARAMETER["Scale_Factor".0.9999].PARAMETER["Latitude_Of_Origin".0.0].UNIT["Meter".1.0]]'
    )
    out_raster.save(r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\S1A_VH_5_5_23_izrezano")
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.CalculateStatistics(
    in_raster_dataset=r"S1A_5_5_2023\S1A_VH_5_5_23",
    x_skip_factor=1,
    y_skip_factor=1,
    ignore_values=[],
    skip_existing="OVERWRITE",
    area_of_interest=r"in_memory\feature_set1"
)
arcpy.ImportToolbox(r"@\Conversion Tools.tbx")
arcpy.conversion.ExportFeatures(
    in_features="vodotoci_RH_3km_KA selection",
    out_features=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\Kupa_Korana_Dobra_Mreznica",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='BDNT_MID "BDNT_MID" true true false 4 Long 0 0,First,#,vodotoci_RH_3km_KA selection,BDNT_MID,-1,-1;WFD_WB_ID "WFD_WB_ID" true true false 4 Long 0 0,First,#,vodotoci_RH_3km_KA selection,WFD_WB_ID,-1,-1;WB_SIFRA "WB_SIFRA" true true false 25 Text 0 0,First,#,vodotoci_RH_3km_KA selection,WB_SIFRA,0,24;NAZIV "NAZIV" true true false 50 Text 0 0,First,#,vodotoci_RH_3km_KA selection,NAZIV,0,49;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,vodotoci_RH_3km_KA selection,Shape_Length,-1,-1',
    sort_field=None
)
arcpy.ImportToolbox(r"@\Data Management Tools.tbx")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="vodotoci_RH_3km_KA",
    selection_type="NEW_SELECTION",
    where_clause="NAZIV = 'Dobra' Or NAZIV = 'Korana' Or NAZIV = 'Kupa' Or NAZIV = 'Mreznica'",
    invert_where_clause=None
)
arcpy.ImportToolbox(r"@\Analysis Tools.tbx")
arcpy.analysis.Clip(
    in_features="vodotoci_RH",
    clip_features="podrucje_istrazivanja_3km",
    out_feature_class=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\vodotoci_RH_3km_KA",
    cluster_tolerance=None
)
arcpy.ImportToolbox(r"@\Conversion Tools.tbx")
arcpy.conversion.ExportFeatures(
    in_features="vodotoci_rh",
    out_features=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\vodotoci_RH",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='BDNT_MID "BDNT_MID" true true false 7 Long 0 7,First,#,vodotoci_rh,BDNT_MID,-1,-1;WFD_WB_ID "WFD_WB_ID" true true false 5 Long 0 5,First,#,vodotoci_rh,WFD_WB_ID,-1,-1;WB_SIFRA "WB_SIFRA" true true false 25 Text 0 0,First,#,vodotoci_rh,WB_SIFRA,0,24;NAZIV "NAZIV" true true false 50 Text 0 0,First,#,vodotoci_rh,NAZIV,0,49',
    sort_field=None
)
arcpy.ImportToolbox(r"@\Analysis Tools.tbx")
arcpy.analysis.Buffer(
    in_features="podrucje_istrazivanja",
    out_feature_class=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\podrucje_istrazivanja_3km",
    buffer_distance_or_field="3 Kilometers",
    line_side="FULL",
    line_end_type="ROUND",
    dissolve_option="ALL",
    dissolve_field=None,
    method="PLANAR"
)
arcpy.ImportToolbox(r"@\Conversion Tools.tbx")
arcpy.conversion.ExportFeatures(
    in_features="JLS selection",
    out_features=r"<PROJEKT>\DATATHON_poplave\DATATHON_poplave.gdb\podrucje_istrazivanja",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='JLS_ID "JLS_ID" true true false 254 Text 0 0,First,#,JLS selection,JLS_ID,0,253;JLS_IDv "JLS_IDv" true true false 254 Text 0 0,First,#,JLS selection,JLS_IDv,0,253;JLS_MB "JLS_MB" true true false 254 Text 0 0,First,#,JLS selection,JLS_MB,0,253;JLS_IME "JLS_IME" true true false 254 Text 0 0,First,#,JLS selection,JLS_IME,0,253;JLS_IME_HR "JLS_IME_HR" true true false 254 Text 0 0,First,#,JLS selection,JLS_IME_HR,0,253;JLS_IME_S1 "JLS_IME_S1" true true false 254 Text 0 0,First,#,JLS selection,JLS_IME_S1,0,253;JLS_IME_J1 "JLS_IME_J1" true true false 254 Text 0 0,First,#,JLS selection,JLS_IME_J1,0,253;JLS_IME_S2 "JLS_IME_S2" true true false 254 Text 0 0,First,#,JLS selection,JLS_IME_S2,0,253;JLS_IME_J2 "JLS_IME_J2" true true false 254 Text 0 0,First,#,JLS selection,JLS_IME_J2,0,253;JLS_IME_KR "JLS_IME_KR" true true false 254 Text 0 0,First,#,JLS selection,JLS_IME_KR,0,253;JLS_ST "JLS_ST" true true false 254 Text 0 0,First,#,JLS selection,JLS_ST,0,253;JLS_SJ "JLS_SJ" true true false 254 Text 0 0,First,#,JLS selection,JLS_SJ,0,253;ZU_RB "ZU_RB" true true false 254 Text 0 0,First,#,JLS selection,ZU_RB,0,253;ZU_IME "ZU_IME" true true false 254 Text 0 0,First,#,JLS selection,ZU_IME,0,253;ZU_SJ "ZU_SJ" true true false 254 Text 0 0,First,#,JLS selection,ZU_SJ,0,253;Shape_Leng "Shape_Leng" true true false 33 Double 31 32,First,#,JLS selection,Shape_Leng,-1,-1;Shape_Area "Shape_Area" true true false 33 Double 31 32,First,#,JLS selection,Shape_Area,-1,-1',
    sort_field=None
)
