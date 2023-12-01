import pandas as pd
from sklearn.cluster import KMeans
from ququ.models import QuquVogue, QuquCatAttrEncoding
from sklearn.mixture import GaussianMixture
import random
def makeKmeansClusters(selected_item, year, season):
    print("#########make K-means clusters############")
    encoding_df = list(QuquCatAttrEncoding.objects.filter(col_year=year, col_season=season).values())
    df = pd.DataFrame(encoding_df)
    index = df['row_name']
    random_list_a = [1,2,3,4,5]
    Rr = random.choice(random_list_a)
    subset_cat_attributes = list(map(lambda x:'col_'+x, selected_item))
    checklist = list(df.columns)
    for i in subset_cat_attributes :
        if i not in checklist:
            subset_cat_attributes.remove(i)
    df = pd.DataFrame(df, columns=subset_cat_attributes)
    df.index = index
    df = df.fillna(0)
    result = {}
    for i in range(10, 21): 
        # K-means
        if i == 15:
            if season == "ss":
                #style_dict = {'cluster0': {'image': ['vogue_S_23_yohji-yamamoto_9.jpg', 'vogue_S_23_eytys_4.jpg', 'vogue_S_23_hermes_52.jpg', 'vogue_S_23_paco-rabanne_6.jpg', 'vogue_S_23_nanushka_16.jpg', 'vogue_S_23_willie-norris-for-outlier_16.jpg', 'vogue_S_23_petar-petrov_28.jpg', 'vogue_S_23_mithridate_27.jpg', 'vogue_S_23_for-restless-sleepers_8.jpg', 'vogue_S_23_rave-review_26.jpg', 'vogue_S_23_ludovic-de-saint-sernin_38.jpg', 'vogue_S_23_melitta-baumeister_6.jpg']}, 'cluster1': {'image': ['vogue_S_23_johanna-ortiz_16.jpg', 'vogue_S_23_european-culture_9.jpg', 'vogue_S_23_sid-neigum_17.jpg', 'vogue_S_23_hope-for-flowers_25.jpg', 'vogue_S_23_bronx-and-banco_21.jpg', 'vogue_S_23_rosie-assoulin_16.jpg', 'vogue_S_23_marni_6.jpg', 'vogue_S_23_di-petsa_14.jpg', 'vogue_S_23_blumarine_34.jpg', 'vogue_S_23_bronx-and-banco_9.jpg', 'vogue_S_23_ralph-lauren_100.jpg', 'vogue_S_23_sportmax_19.jpg', 'vogue_S_23_missoni_22.jpg', 'vogue_S_23_badgley-mischka_39.jpg', 'vogue_S_23_christian-cowan_13.jpg']}, 'cluster2': {'image': ['vogue_S_23_maison-rabih-kayrouz_17.jpg', 'vogue_S_23_acne-studios_15.jpg', 'vogue_S_23_vetements_7.jpg', 'vogue_S_23_khaite_8.jpg', 'vogue_S_23_priscavera_17.jpg', 'vogue_S_23_coach_41.jpg', 'vogue_S_23_thom-browne_27.jpg', 'vogue_S_23_puppets-and-puppets_23.jpg', 'vogue_S_23_row_33.jpg', 'vogue_S_23_filippa-k_14.jpg', 'vogue_S_23_ermanno-scervino_43.jpg', 'vogue_S_23_burberry-prorsum_39.jpg', 'vogue_S_23_bottega-veneta_36.jpg', 'vogue_S_23_richard-quinn_12.jpg']}, 'cluster3': {'image': ['vogue_S_23_gmbh_11.jpg', 'vogue_S_23_studio-189_44.jpg', 'vogue_S_23_officine-generale_16.jpg', 'vogue_S_23_thakoon_2.jpg', 'vogue_S_23_ralph-lauren_53.jpg', 'vogue_S_23_kenneth-nicholson_7.jpg', 'vogue_S_23_6397_16.jpg', 'vogue_S_23_maria-mcmanus_9.jpg', 'vogue_S_23_theory_19.jpg', 'vogue_S_23_deveaux_15.jpg', 'vogue_S_23_european-culture_63.jpg', 'vogue_S_23_sandy-liang_15.jpg', 'vogue_S_23_maryam-nassir-zadeh_7.jpg', 'vogue_S_23_tod-s_47.jpg', 'vogue_S_23_vtmnts_23.jpg']}, 'cluster4': {'image': ['vogue_S_23_elena-velez_25.jpg', 'vogue_S_23_sukeina_17.jpg', 'vogue_S_23_alejandra-alonso-rojas_13.jpg', 'vogue_S_23_mame-kurogouchi_20.jpg', 'vogue_S_23_toga_5.jpg', 'vogue_S_23_frederick-anderson_20.jpg', 'vogue_S_23_dolce-gabbana_14.jpg', 'vogue_S_23_autumn-adeigbo_5.jpg', 'vogue_S_23_sukeina_10.jpg', 'vogue_S_23_coperni_15.jpg', 'vogue_S_23_mowalola_20.jpg', 'vogue_S_23_acne-studios_26.jpg', 'vogue_S_23_parsons-mfa_34.jpg', 'vogue_S_23_bibhu-mohapatra_5.jpg', 'vogue_S_23_rochas_20.jpg']}, 'cluster5': {'image': ['vogue_S_23_vtmnts_30.jpg', 'vogue_S_23_all-in_12.jpg', 'vogue_S_23_masha-popova_12.jpg', 'vogue_S_23_brandon-maxwell_15.jpg', 'vogue_S_23_lafayette-148_1.jpg', 'vogue_S_23_monse_31.jpg', 'vogue_S_23_barragan_7.jpg', 'vogue_S_23_philipp-plein_61.jpg', 'vogue_S_23_ludovic-de-saint-sernin_5.jpg', 'vogue_S_23_tibi_43.jpg', 'vogue_S_23_collina-strada_16.jpg', 'vogue_S_23_ambush_10.jpg', 'vogue_S_23_gauchere_21.jpg', 'vogue_S_23_del-core_24.jpg', 'vogue_S_23_maje_1.jpg']}, 'cluster6': {'image': ['vogue_S_23_row_36.jpg', 'vogue_S_23_kenzo_4.jpg', 'vogue_S_23_ss-daley_9.jpg', 'vogue_S_23_reem-acra_28.jpg', 'vogue_S_23_agnona_5.jpg', 'vogue_S_23_christophe-lemaire_15.jpg', 'vogue_S_23_callas-milano_12.jpg', 'vogue_S_23_paolo-carzana_7.jpg', 'vogue_S_23_courreges_7.jpg', 'vogue_S_23_reem-acra_14.jpg', 'vogue_S_23_alexis-mabille_2.jpg']}, 'cluster7': {'image': ['vogue_S_23_botter_3.jpg', 'vogue_S_23_gmbh_1.jpg', 'vogue_S_23_ag_6.jpg', 'vogue_S_23_deveaux_30.jpg', 'vogue_S_23_juunj_16.jpg', 'vogue_S_23_michael-kors-collection_30.jpg', 'vogue_S_23_nehera_12.jpg', 'vogue_S_23_burberry-prorsum_72.jpg', 'vogue_S_23_brandon-maxwell_11.jpg', 'vogue_S_23_heron-preston_27.jpg', 'vogue_S_23_a-l-c_16.jpg', 'vogue_S_23_a-w-a-k-e-_56.jpg']}, 'cluster8': {'image': ['vogue_S_23_mossi_15.jpg', 'vogue_S_23_ss-daley_5.jpg', 'vogue_S_23_rta_24.jpg', 'vogue_S_23_givenchy_26.jpg', 'vogue_S_23_isabel-marant_9.jpg', 'vogue_S_23_windsor_18.jpg', 'vogue_S_23_maryam-nassir-zadeh_8.jpg', 'vogue_S_23_bottega-veneta_61.jpg', 'vogue_S_23_ulla-johnson_48.jpg', 'vogue_S_23_david-koma_17.jpg', 'vogue_S_23_kenneth-nicholson_32.jpg', 'vogue_S_23_ludovic-de-saint-sernin_15.jpg']}, 'cluster9': {'image': ['vogue_S_23_lutz-huelle_7.jpg', 'vogue_S_23_eytys_26.jpg', 'vogue_S_23_azzedine-alaia_48.jpg', 'vogue_S_23_dilara-findikoglu_8.jpg', 'vogue_S_23_altuzarra_19.jpg', 'vogue_S_23_colville_20.jpg', 'vogue_S_23_hugo-boss_62.jpg',  'vogue_S_23_eudon-choi_38.jpg',  'vogue_S_23_raf-simons_27.jpg', 'vogue_S_23_balmain_86.jpg',  'vogue_S_23_antonio-marras_52.jpg']}, 'cluster10': {'image': ['vogue_S_23_blumarine_55.jpg', 'vogue_S_23_ferrari_31.jpg', 'vogue_S_23_fabiana-filippi_8.jpg', 'vogue_S_23_kenzo_2.jpg', 'vogue_S_23_kenzo_5.jpg', 'vogue_S_23_heron-preston_21.jpg', 'vogue_S_23_rick-owens_46.jpg', 'vogue_S_23_ashlyn_19.jpg', 'vogue_S_23_marc-jacobs_18.jpg', 'vogue_S_23_tokyo-james_38.jpg', 'vogue_S_23_commission_12.jpg', 'vogue_S_23_vtmnts_26.jpg', 'vogue_S_23_european-culture_28.jpg', 'vogue_S_23_gcds_14.jpg', 'vogue_S_23_charlotte-knowles_8.jpg']}, 'cluster11': {'image': ['vogue_S_23_christian-siriano_9.jpg', 'vogue_S_23_dsquared_16.jpg', 'vogue_S_23_plan-c_16.jpg', 'vogue_S_23_emilia-wickstead_30.jpg', 'vogue_S_23_cong-tri_22.jpg', 'vogue_S_23_patrick-mcdowell_3.jpg', 'vogue_S_23_matty-bovan_11.jpg', 'vogue_S_23_fendi_13.jpg', 'vogue_S_23_loewe_32.jpg', 'vogue_S_23_ulla-johnson_11.jpg', 'vogue_S_23_mm6-maison-martin-margiela_3.jpg']}, 'cluster12': {'image': ['vogue_S_23_halpern_19.jpg', 'vogue_S_23_zuhair-murad_42.jpg', 'vogue_S_23_alexis-mabille_13.jpg', 'vogue_S_23_acne-studios_43.jpg', 'vogue_S_23_jason-wu_3.jpg', 'vogue_S_23_rochas_25.jpg', 'vogue_S_23_halpern_2.jpg', 'vogue_S_23_marques-almeida_64.jpg', 'vogue_S_23_antonio-marras_70.jpg', 'vogue_S_23_burberry-prorsum_80.jpg', 'vogue_S_23_jil-sander_19.jpg', 'vogue_S_23_mithridate_12.jpg', 'vogue_S_23_richard-quinn_3.jpg', 'vogue_S_23_roberto-cavalli_38.jpg', 'vogue_S_23_adeam_28.jpg']}, 'cluster13': {'image': ['vogue_S_23_nanushka_2.jpg', 'vogue_S_23_edeline-lee_9.jpg',  'vogue_S_23_yuhan-wang_23.jpg', 'vogue_S_23_parsons-mfa_46.jpg', 'vogue_S_23_european-culture_20.jpg', 'vogue_S_23_vivetta_22.jpg', 'vogue_S_23_gmbh_9.jpg', 'vogue_S_23_maje_8.jpg', 'vogue_S_23_nensi-dojaka_4.jpg', 'vogue_S_23_chet-lo_5.jpg', 'vogue_S_23_a-l-c_14.jpg', 'vogue_S_23_ph5_21.jpg']}, 'cluster14': {'image': ['vogue_S_23_tanya-taylor_16.jpg', 'vogue_S_23_isabel-marant_32.jpg', 'vogue_S_23_emporio-armani_43.jpg', 'vogue_S_23_sandy-liang_44.jpg', 'vogue_S_23_kitx_10.jpg', 'vogue_S_23_jacquemus_52.jpg', 'vogue_S_23_kate-spade-new-york_18.jpg', 'vogue_S_23_diesel_30.jpg', 'vogue_S_23_palmerharding_17.jpg', 'vogue_S_23_ralph-lauren_51.jpg', 'vogue_S_23_interior_18.jpg']}}
                style_dict = {'dark_punk': ['vogue_S_23_yohji-yamamoto_9.jpg', 'vogue_S_23_eytys_4.jpg', 'vogue_S_23_hermes_52.jpg', 'vogue_S_23_paco-rabanne_6.jpg', 'vogue_S_23_nanushka_16.jpg', 'vogue_S_23_willie-norris-for-outlier_16.jpg', 'vogue_S_23_petar-petrov_28.jpg', 'vogue_S_23_mithridate_27.jpg', 'vogue_S_23_for-restless-sleepers_8.jpg', 'vogue_S_23_rave-review_26.jpg', 'vogue_S_23_ludovic-de-saint-sernin_38.jpg', 'vogue_S_23_melitta-baumeister_6.jpg'], 
                'elegance': ['vogue_S_23_johanna-ortiz_16.jpg', 'vogue_S_23_european-culture_9.jpg', 'vogue_S_23_sid-neigum_17.jpg', 'vogue_S_23_hope-for-flowers_25.jpg', 'vogue_S_23_bronx-and-banco_21.jpg', 'vogue_S_23_rosie-assoulin_16.jpg', 'vogue_S_23_marni_6.jpg', 'vogue_S_23_di-petsa_14.jpg', 'vogue_S_23_blumarine_34.jpg', 'vogue_S_23_bronx-and-banco_9.jpg', 'vogue_S_23_ralph-lauren_100.jpg', 'vogue_S_23_sportmax_19.jpg', 'vogue_S_23_missoni_22.jpg', 'vogue_S_23_badgley-mischka_39.jpg', 'vogue_S_23_christian-cowan_13.jpg'], 
                'oversized_grunge': ['vogue_S_23_maison-rabih-kayrouz_17.jpg', 'vogue_S_23_acne-studios_15.jpg', 'vogue_S_23_vetements_7.jpg', 'vogue_S_23_khaite_8.jpg', 'vogue_S_23_priscavera_17.jpg', 'vogue_S_23_coach_41.jpg', 'vogue_S_23_thom-browne_27.jpg', 'vogue_S_23_puppets-and-puppets_23.jpg', 'vogue_S_23_row_33.jpg', 'vogue_S_23_filippa-k_14.jpg', 'vogue_S_23_ermanno-scervino_43.jpg', 'vogue_S_23_burberry-prorsum_39.jpg', 'vogue_S_23_bottega-veneta_36.jpg', 'vogue_S_23_richard-quinn_12.jpg'],
                'casual_simple': ['vogue_S_23_gmbh_11.jpg', 'vogue_S_23_studio-189_44.jpg', 'vogue_S_23_officine-generale_16.jpg', 'vogue_S_23_thakoon_2.jpg', 'vogue_S_23_ralph-lauren_53.jpg', 'vogue_S_23_kenneth-nicholson_7.jpg', 'vogue_S_23_6397_16.jpg', 'vogue_S_23_maria-mcmanus_9.jpg', 'vogue_S_23_theory_19.jpg', 'vogue_S_23_deveaux_15.jpg', 'vogue_S_23_european-culture_63.jpg', 'vogue_S_23_sandy-liang_15.jpg', 'vogue_S_23_maryam-nassir-zadeh_7.jpg', 'vogue_S_23_tod-s_47.jpg', 'vogue_S_23_vtmnts_23.jpg'],
                'sexy_chic': ['vogue_S_23_elena-velez_25.jpg', 'vogue_S_23_sukeina_17.jpg', 'vogue_S_23_alejandra-alonso-rojas_13.jpg', 'vogue_S_23_mame-kurogouchi_20.jpg', 'vogue_S_23_toga_5.jpg', 'vogue_S_23_frederick-anderson_20.jpg', 'vogue_S_23_dolce-gabbana_14.jpg', 'vogue_S_23_autumn-adeigbo_5.jpg', 'vogue_S_23_sukeina_10.jpg', 'vogue_S_23_coperni_15.jpg', 'vogue_S_23_mowalola_20.jpg', 'vogue_S_23_acne-studios_26.jpg', 'vogue_S_23_parsons-mfa_34.jpg', 'vogue_S_23_bibhu-mohapatra_5.jpg', 'vogue_S_23_rochas_20.jpg'],
                'street_punk': ['vogue_S_23_vtmnts_30.jpg', 'vogue_S_23_all-in_12.jpg', 'vogue_S_23_masha-popova_12.jpg', 'vogue_S_23_brandon-maxwell_15.jpg', 'vogue_S_23_lafayette-148_1.jpg', 'vogue_S_23_monse_31.jpg', 'vogue_S_23_barragan_7.jpg', 'vogue_S_23_philipp-plein_61.jpg', 'vogue_S_23_ludovic-de-saint-sernin_5.jpg', 'vogue_S_23_tibi_43.jpg', 'vogue_S_23_collina-strada_16.jpg', 'vogue_S_23_ambush_10.jpg', 'vogue_S_23_gauchere_21.jpg', 'vogue_S_23_del-core_24.jpg', 'vogue_S_23_maje_1.jpg'],
                'pure_feminine': ['vogue_S_23_row_36.jpg', 'vogue_S_23_kenzo_4.jpg', 'vogue_S_23_ss-daley_9.jpg', 'vogue_S_23_reem-acra_28.jpg', 'vogue_S_23_agnona_5.jpg', 'vogue_S_23_christophe-lemaire_15.jpg', 'vogue_S_23_callas-milano_12.jpg', 'vogue_S_23_paolo-carzana_7.jpg', 'vogue_S_23_courreges_7.jpg', 'vogue_S_23_reem-acra_14.jpg', 'vogue_S_23_alexis-mabille_2.jpg'],
                'formal': ['vogue_S_23_botter_3.jpg', 'vogue_S_23_gmbh_1.jpg', 'vogue_S_23_ag_6.jpg', 'vogue_S_23_deveaux_30.jpg', 'vogue_S_23_juunj_16.jpg', 'vogue_S_23_michael-kors-collection_30.jpg', 'vogue_S_23_nehera_12.jpg', 'vogue_S_23_burberry-prorsum_72.jpg', 'vogue_S_23_brandon-maxwell_11.jpg', 'vogue_S_23_heron-preston_27.jpg', 'vogue_S_23_a-l-c_16.jpg', 'vogue_S_23_a-w-a-k-e-_56.jpg'],
                'street_casual': ['vogue_S_23_mossi_15.jpg', 'vogue_S_23_ss-daley_5.jpg', 'vogue_S_23_rta_24.jpg', 'vogue_S_23_givenchy_26.jpg', 'vogue_S_23_isabel-marant_9.jpg', 'vogue_S_23_windsor_18.jpg', 'vogue_S_23_maryam-nassir-zadeh_8.jpg', 'vogue_S_23_bottega-veneta_61.jpg', 'vogue_S_23_ulla-johnson_48.jpg', 'vogue_S_23_david-koma_17.jpg', 'vogue_S_23_kenneth-nicholson_32.jpg', 'vogue_S_23_ludovic-de-saint-sernin_15.jpg'], 
                'feminine_grunge': ['vogue_S_23_lutz-huelle_7.jpg', 'vogue_S_23_eytys_26.jpg', 'vogue_S_23_azzedine-alaia_48.jpg', 'vogue_S_23_dilara-findikoglu_8.jpg', 'vogue_S_23_altuzarra_19.jpg', 'vogue_S_23_colville_20.jpg', 'vogue_S_23_hugo-boss_62.jpg',  'vogue_S_23_eudon-choi_38.jpg',  'vogue_S_23_raf-simons_27.jpg', 'vogue_S_23_balmain_86.jpg',  'vogue_S_23_antonio-marras_52.jpg'],
                'hip_hop': ['vogue_S_23_blumarine_55.jpg', 'vogue_S_23_ferrari_31.jpg', 'vogue_S_23_fabiana-filippi_8.jpg', 'vogue_S_23_kenzo_2.jpg', 'vogue_S_23_kenzo_5.jpg', 'vogue_S_23_heron-preston_21.jpg', 'vogue_S_23_rick-owens_46.jpg', 'vogue_S_23_ashlyn_19.jpg', 'vogue_S_23_marc-jacobs_18.jpg', 'vogue_S_23_tokyo-james_38.jpg', 'vogue_S_23_commission_12.jpg', 'vogue_S_23_vtmnts_26.jpg', 'vogue_S_23_european-culture_28.jpg', 'vogue_S_23_gcds_14.jpg', 'vogue_S_23_charlotte-knowles_8.jpg'],
                'vivid_punk': ['vogue_S_23_christian-siriano_9.jpg', 'vogue_S_23_dsquared_16.jpg', 'vogue_S_23_plan-c_16.jpg', 'vogue_S_23_emilia-wickstead_30.jpg', 'vogue_S_23_cong-tri_22.jpg', 'vogue_S_23_patrick-mcdowell_3.jpg', 'vogue_S_23_matty-bovan_11.jpg', 'vogue_S_23_fendi_13.jpg', 'vogue_S_23_loewe_32.jpg', 'vogue_S_23_ulla-johnson_11.jpg', 'vogue_S_23_mm6-maison-martin-margiela_3.jpg'],
                'chic_elegance': ['vogue_S_23_halpern_19.jpg', 'vogue_S_23_zuhair-murad_42.jpg', 'vogue_S_23_alexis-mabille_13.jpg', 'vogue_S_23_acne-studios_43.jpg', 'vogue_S_23_jason-wu_3.jpg', 'vogue_S_23_rochas_25.jpg', 'vogue_S_23_halpern_2.jpg', 'vogue_S_23_marques-almeida_64.jpg', 'vogue_S_23_antonio-marras_70.jpg', 'vogue_S_23_burberry-prorsum_80.jpg', 'vogue_S_23_jil-sander_19.jpg', 'vogue_S_23_mithridate_12.jpg', 'vogue_S_23_richard-quinn_3.jpg', 'vogue_S_23_roberto-cavalli_38.jpg', 'vogue_S_23_adeam_28.jpg'],
                'sexy_feminine': ['vogue_S_23_nanushka_2.jpg', 'vogue_S_23_edeline-lee_9.jpg',  'vogue_S_23_yuhan-wang_23.jpg', 'vogue_S_23_parsons-mfa_46.jpg', 'vogue_S_23_european-culture_20.jpg', 'vogue_S_23_vivetta_22.jpg', 'vogue_S_23_gmbh_9.jpg', 'vogue_S_23_maje_8.jpg', 'vogue_S_23_nensi-dojaka_4.jpg', 'vogue_S_23_chet-lo_5.jpg', 'vogue_S_23_a-l-c_14.jpg', 'vogue_S_23_ph5_21.jpg'],
                'bohemian_feminine': ['vogue_S_23_tanya-taylor_16.jpg', 'vogue_S_23_isabel-marant_32.jpg', 'vogue_S_23_emporio-armani_43.jpg', 'vogue_S_23_sandy-liang_44.jpg', 'vogue_S_23_kitx_10.jpg', 'vogue_S_23_jacquemus_52.jpg', 'vogue_S_23_kate-spade-new-york_18.jpg', 'vogue_S_23_diesel_30.jpg', 'vogue_S_23_palmerharding_17.jpg', 'vogue_S_23_ralph-lauren_51.jpg', 'vogue_S_23_interior_18.jpg']}
                result['k'+str(i)] = style_dict
            elif season == "fw":
                #style_dict = {'cluster0': {'image': ['vogue_F_23_giambattista-valli_53.jpg', 'vogue_F_23_miu-miu_29.jpg', 'vogue_F_23_loewe_33.jpg', 'vogue_F_23_anna-october_2.jpg', 'vogue_F_23_badgley-mischka_31.jpg', 'vogue_F_23_noir-kei-ninomiya_16.jpg', 'vogue_F_23_naeem-khan_18.jpg', 'vogue_F_23_dilara-findikoglu_34.jpg', 'vogue_F_23_cinq-a-sept_15.jpg', 'vogue_F_23_johanna-ortiz_12.jpg', 'vogue_F_23_dundas_38.jpg', 'vogue_F_23_alejandra-alonso-rojas_4.jpg', 'vogue_F_23_givenchy_44.jpg', 'vogue_F_23_etro_58.jpg']}, 'cluster1': {'image': ['vogue_F_23_we11done_10.jpg', 'vogue_F_23_chanel_31.jpg', 'vogue_F_23_veronica-beard_31.jpg', 'vogue_F_23_rodarte_6.jpg', 'vogue_F_23_jason-wu_1.jpg', 'vogue_F_23_we11done_40.jpg', 'vogue_F_23_isabel-marant_17.jpg', 'vogue_F_23_yohji-yamamoto_39.jpg', 'vogue_F_23_ferrari_1.jpg', 'vogue_F_23_salvatore-ferragamo_52.jpg', 'vogue_F_23_lala-berlin_30.jpg', 'vogue_F_23_max-mara_27.jpg', 'vogue_F_23_we11done_6.jpg']}, 'cluster2': {'image': ['vogue_F_23_luar_38.jpg', 'vogue_F_23_loro-piana_15.jpg', 'vogue_F_23_antonio-marras_39.jpg', 'vogue_F_23_margaret-howell_31.jpg', 'vogue_F_23_heron-preston_14.jpg', 'vogue_F_23_gcds_32.jpg', 'vogue_F_23_bally_47.jpg', 'vogue_F_23_prada_8.jpg', 'vogue_F_23_ashlyn_16.jpg', 'vogue_F_23_maisie-wilen_6.jpg', 'vogue_F_23_antonio-marras_81.jpg', 'vogue_F_23_prada_7.jpg']}, 'cluster3': {'image': ['vogue_F_23_ermanno-scervino_44.jpg', 'vogue_F_23_ahluwalia-studio_27.jpg', 'vogue_F_23_carolina-herrera_20.jpg', 'vogue_F_23_krizia_17.jpg', 'vogue_F_23_loveshackfancy_23.jpg', 'vogue_F_23_sara-battaglia_31.jpg', 'vogue_F_23_badgley-mischka_27.jpg', 'vogue_F_23_di-petsa_12.jpg', 'vogue_F_23_tanya-taylor_23.jpg', 'vogue_F_23_schiaparelli_4.jpg', 'vogue_F_23_ester-manas_24.jpg', 'vogue_F_23_erl_40.jpg', 'vogue_F_23_chet-lo_9.jpg', 'vogue_F_23_badgley-mischka_10.jpg', 'vogue_F_23_sunnei_13.jpg']}, 'cluster4': {'image': ['vogue_F_23_emporio-armani_65.jpg', 'vogue_F_23_marina-moscone_11.jpg', 'vogue_F_23_alyx_21.jpg', 'vogue_F_23_stella-jean_30.jpg', 'vogue_F_23_alessandra-rich_35.jpg', 'vogue_F_23_antonio-marras_58.jpg', 'vogue_F_23_kim-shui_41.jpg', 'vogue_F_23_salvatore-ferragamo_16.jpg', 'vogue_F_23_shang-xia_20.jpg', 'vogue_F_23_chloe_2.jpg', 'vogue_F_23_callas-milano_9.jpg']}, 'cluster5': {'image': ['vogue_F_23_a-w-a-k-e-_25.jpg', 'vogue_F_23_lanvin_38.jpg', 'vogue_F_23_undercover_1.jpg', 'vogue_F_23_brunello-cucinelli_27.jpg', 'vogue_F_23_emilia-wickstead_11.jpg', 'vogue_F_23_hui_32.jpg', 'vogue_F_23_gmbh_8.jpg', 'vogue_F_23_emporio-armani_40.jpg', 'vogue_F_23_antonio-marras_66.jpg', 'vogue_F_23_salvatore-ferragamo_12.jpg', 'vogue_F_23_st-john_1.jpg', 'vogue_F_23_stella-mccartney_12.jpg', 'vogue_F_23_stella-mccartney_3.jpg', 'vogue_F_23_feben_25.jpg', 'vogue_F_23_armarium_1.jpg']}, 'cluster6': {'image': ['vogue_F_23_blumarine_4.jpg', 'vogue_F_23_dsquared_13.jpg', 'vogue_F_23_philipp-plein_4.jpg', 'vogue_F_23_alice-olivia_26.jpg', 'vogue_F_23_balmain_7.jpg', 'vogue_F_23_dsquared_44.jpg', 'vogue_F_23_gmbh_19.jpg', 'vogue_F_23_alexander-mcqueen_36.jpg', 'vogue_F_23_heron-preston_11.jpg', 'vogue_F_23_diesel_41.jpg', 'vogue_F_23_ann-demeulemeester_3.jpg', 'vogue_F_23_calvin-luo_1.jpg', 'vogue_F_23_alberta-ferretti_9.jpg', 'vogue_F_23_cfcl_19.jpg']}, 'cluster7': {'image': ['vogue_F_23_susan-fang_7.jpg', 'vogue_F_23_yigal-azrouel_10.jpg', 'vogue_F_23_courreges_45.jpg', 'vogue_F_23_shuting-qiu_16.jpg', 'vogue_F_23_chufy_13.jpg', 'vogue_F_23_andreas-kronthaler-for-vivienne-westwood_25.jpg', 'vogue_F_23_ulla-johnson_11.jpg', 'vogue_F_23_anteprima_9.jpg', 'vogue_F_23_philipp-plein_78.jpg', 'vogue_F_23_giambattista-valli_40.jpg', 'vogue_F_23_polo-ralph-lauren_10.jpg', 'vogue_F_23_burberry-prorsum_49.jpg', 'vogue_F_23_jil-sander_37.jpg', 'vogue_F_23_commission_9.jpg', 'vogue_F_23_nensi-dojaka_11.jpg']}, 'cluster8': {'image': ['vogue_F_23_vivienne-westwood_49.jpg', 'vogue_F_23_sally-lapointe_17.jpg',  'vogue_F_23_duro-olowu_2.jpg', 'vogue_F_23_norma-kamali_40.jpg', 'vogue_F_23_giorgio-armani_68.jpg', 'vogue_F_23_etro_31.jpg', 'vogue_F_23_giorgio-armani_70.jpg', 'vogue_F_23_we11done_26.jpg', 'vogue_F_23_lutz-huelle_43.jpg', 'vogue_F_23_undercover_15.jpg', 'vogue_F_23_saint-laurent_28.jpg', 'vogue_F_23_la-doublej_10.jpg']}, 'cluster9': {'image': ['vogue_F_23_nensi-dojaka_2.jpg', 'vogue_F_23_bibhu-mohapatra_23.jpg', 'vogue_F_23_andreadamo_4.jpg', 'vogue_F_23_sharon-wauchob_16.jpg', 'vogue_F_23_fashion-east_32.jpg', 'vogue_F_23_msgm_34.jpg', 'vogue_F_23_gcds_8.jpg', 'vogue_F_23_hodakova_2.jpg', 'vogue_F_23_calvin-luo_40.jpg', 'vogue_F_23_chet-lo_13.jpg', 'vogue_F_23_cormio_16.jpg', 'vogue_F_23_dion-lee_39.jpg']}, 'cluster10': {'image': ['vogue_F_23_roland-mouret_19.jpg', 'vogue_F_23_sally-lapointe_25.jpg', 'vogue_F_23_melitta-baumeister_27.jpg', 'vogue_F_23_niccolo-pasqualetti_20.jpg', 'vogue_F_23_sally-lapointe_28.jpg', 'vogue_F_23_duro-olowu_22.jpg', 'vogue_F_23_6397_15.jpg', 'vogue_F_23_marni_20.jpg', 'vogue_F_23_kiko-kostadinov_34.jpg', 'vogue_F_23_beatrice-b_9.jpg']}, 'cluster11': {'image': ['vogue_F_23_frederick-anderson_38.jpg',  'vogue_F_23_alexander-wang_51.jpg', 'vogue_F_23_carolina-herrera_27.jpg', 'vogue_F_23_acne-studios_32.jpg', 'vogue_F_23_naeem-khan_43.jpg', 'vogue_F_23_ulla-johnson_50.jpg', 'vogue_F_23_schiaparelli_24.jpg', 'vogue_F_23_edeline-lee_27.jpg', 'vogue_F_23_fashion-east_13.jpg','vogue_F_23_jil-sander_24.jpg', 'vogue_F_23_miu-miu_7.jpg', 'vogue_F_23_zuhair-murad_38.jpg']}, 'cluster12': {'image': ['vogue_F_23_giorgio-armani_28.jpg', 'vogue_F_23_alyx_13.jpg',  'vogue_F_23_libertine_10.jpg', 'vogue_F_23_libertine_12.jpg', 'vogue_F_23_msgm_16.jpg', 'vogue_F_23_rosetta-getty_10.jpg', 'vogue_F_23_dries-van-noten_10.jpg', 'vogue_F_23_bibhu-mohapatra_4.jpg', 'vogue_F_23_hui_30.jpg', 'vogue_F_23_snow-xue-gao_3.jpg', 'vogue_F_23_loro-piana_9.jpg', 'vogue_F_23_nina-ricci_27.jpg', 'vogue_F_23_etro_44.jpg']}, 'cluster13': {'image': [ 'vogue_F_23_christian-dior_40.jpg', 'vogue_F_23_balmain_18.jpg', 'vogue_F_23_for-restless-sleepers_8.jpg','vogue_F_23_loewe_4.jpg', 'vogue_F_23_sacai_24.jpg', 'vogue_F_23_chet-lo_27.jpg', 'vogue_F_23_lafayette-148_6.jpg', 'vogue_F_23_zankov_12.jpg', 'vogue_F_23_antonio-marras_41.jpg', 'vogue_F_23_max-mara_26.jpg','vogue_F_23_marine-serre_28.jpg', 'vogue_F_23_autumn-adeigbo_1.jpg']}, 'cluster14': {'image': ['vogue_F_23_philosophy_19.jpg', 'vogue_F_23_institut-francais-de-la-mode_74.jpg', 'vogue_F_23_dion-lee_3.jpg', 'vogue_F_23_polo-ralph-lauren_1.jpg','vogue_F_23_heron-preston_8.jpg', 'vogue_F_23_institut-francais-de-la-mode_55.jpg', 'vogue_F_23_fforme_24.jpg', 'vogue_F_23_tory-burch_20.jpg']}}
                style_dict = {'bohemian_elegance': ['vogue_F_23_giambattista-valli_53.jpg', 'vogue_F_23_miu-miu_29.jpg', 'vogue_F_23_loewe_33.jpg', 'vogue_F_23_anna-october_2.jpg', 'vogue_F_23_badgley-mischka_31.jpg', 'vogue_F_23_noir-kei-ninomiya_16.jpg', 'vogue_F_23_naeem-khan_18.jpg', 'vogue_F_23_dilara-findikoglu_34.jpg', 'vogue_F_23_cinq-a-sept_15.jpg', 'vogue_F_23_johanna-ortiz_12.jpg', 'vogue_F_23_dundas_38.jpg', 'vogue_F_23_alejandra-alonso-rojas_4.jpg', 'vogue_F_23_givenchy_44.jpg', 'vogue_F_23_etro_58.jpg'],
                'chic_formal': ['vogue_F_23_we11done_10.jpg', 'vogue_F_23_chanel_31.jpg', 'vogue_F_23_veronica-beard_31.jpg', 'vogue_F_23_rodarte_6.jpg', 'vogue_F_23_jason-wu_1.jpg', 'vogue_F_23_we11done_40.jpg', 'vogue_F_23_isabel-marant_17.jpg', 'vogue_F_23_yohji-yamamoto_39.jpg', 'vogue_F_23_ferrari_1.jpg', 'vogue_F_23_salvatore-ferragamo_52.jpg', 'vogue_F_23_lala-berlin_30.jpg', 'vogue_F_23_max-mara_27.jpg', 'vogue_F_23_we11done_6.jpg'], 
                'tomboy': ['vogue_F_23_luar_38.jpg', 'vogue_F_23_loro-piana_15.jpg', 'vogue_F_23_antonio-marras_39.jpg', 'vogue_F_23_margaret-howell_31.jpg', 'vogue_F_23_heron-preston_14.jpg', 'vogue_F_23_gcds_32.jpg', 'vogue_F_23_bally_47.jpg', 'vogue_F_23_prada_8.jpg', 'vogue_F_23_ashlyn_16.jpg', 'vogue_F_23_maisie-wilen_6.jpg', 'vogue_F_23_antonio-marras_81.jpg', 'vogue_F_23_prada_7.jpg'], 
                'sexy_feminine': ['vogue_F_23_ermanno-scervino_44.jpg', 'vogue_F_23_ahluwalia-studio_27.jpg', 'vogue_F_23_carolina-herrera_20.jpg', 'vogue_F_23_krizia_17.jpg', 'vogue_F_23_loveshackfancy_23.jpg', 'vogue_F_23_sara-battaglia_31.jpg', 'vogue_F_23_badgley-mischka_27.jpg', 'vogue_F_23_di-petsa_12.jpg', 'vogue_F_23_tanya-taylor_23.jpg', 'vogue_F_23_schiaparelli_4.jpg', 'vogue_F_23_ester-manas_24.jpg', 'vogue_F_23_erl_40.jpg', 'vogue_F_23_chet-lo_9.jpg', 'vogue_F_23_badgley-mischka_10.jpg', 'vogue_F_23_sunnei_13.jpg'],
                'dark_romance': ['vogue_F_23_emporio-armani_65.jpg', 'vogue_F_23_marina-moscone_11.jpg', 'vogue_F_23_alyx_21.jpg', 'vogue_F_23_stella-jean_30.jpg', 'vogue_F_23_alessandra-rich_35.jpg', 'vogue_F_23_antonio-marras_58.jpg', 'vogue_F_23_kim-shui_41.jpg', 'vogue_F_23_salvatore-ferragamo_16.jpg', 'vogue_F_23_shang-xia_20.jpg', 'vogue_F_23_chloe_2.jpg', 'vogue_F_23_callas-milano_9.jpg'],
                'formal': ['vogue_F_23_a-w-a-k-e-_25.jpg', 'vogue_F_23_lanvin_38.jpg', 'vogue_F_23_undercover_1.jpg', 'vogue_F_23_brunello-cucinelli_27.jpg', 'vogue_F_23_emilia-wickstead_11.jpg', 'vogue_F_23_hui_32.jpg', 'vogue_F_23_gmbh_8.jpg', 'vogue_F_23_emporio-armani_40.jpg', 'vogue_F_23_antonio-marras_66.jpg', 'vogue_F_23_salvatore-ferragamo_12.jpg', 'vogue_F_23_st-john_1.jpg', 'vogue_F_23_stella-mccartney_12.jpg', 'vogue_F_23_stella-mccartney_3.jpg', 'vogue_F_23_feben_25.jpg', 'vogue_F_23_armarium_1.jpg'],
                'rock_chic': ['vogue_F_23_blumarine_4.jpg', 'vogue_F_23_dsquared_13.jpg', 'vogue_F_23_philipp-plein_4.jpg', 'vogue_F_23_alice-olivia_26.jpg', 'vogue_F_23_balmain_7.jpg', 'vogue_F_23_dsquared_44.jpg', 'vogue_F_23_gmbh_19.jpg', 'vogue_F_23_alexander-mcqueen_36.jpg', 'vogue_F_23_heron-preston_11.jpg', 'vogue_F_23_diesel_41.jpg', 'vogue_F_23_ann-demeulemeester_3.jpg', 'vogue_F_23_calvin-luo_1.jpg', 'vogue_F_23_alberta-ferretti_9.jpg', 'vogue_F_23_cfcl_19.jpg'],
                'hip_hop': ['vogue_F_23_susan-fang_7.jpg', 'vogue_F_23_yigal-azrouel_10.jpg', 'vogue_F_23_courreges_45.jpg', 'vogue_F_23_shuting-qiu_16.jpg', 'vogue_F_23_chufy_13.jpg', 'vogue_F_23_andreas-kronthaler-for-vivienne-westwood_25.jpg', 'vogue_F_23_ulla-johnson_11.jpg', 'vogue_F_23_anteprima_9.jpg', 'vogue_F_23_philipp-plein_78.jpg', 'vogue_F_23_giambattista-valli_40.jpg', 'vogue_F_23_polo-ralph-lauren_10.jpg', 'vogue_F_23_burberry-prorsum_49.jpg', 'vogue_F_23_jil-sander_37.jpg', 'vogue_F_23_commission_9.jpg', 'vogue_F_23_nensi-dojaka_11.jpg'],
                'vintage_street': ['vogue_F_23_vivienne-westwood_49.jpg', 'vogue_F_23_sally-lapointe_17.jpg',  'vogue_F_23_duro-olowu_2.jpg', 'vogue_F_23_norma-kamali_40.jpg', 'vogue_F_23_giorgio-armani_68.jpg', 'vogue_F_23_etro_31.jpg', 'vogue_F_23_giorgio-armani_70.jpg', 'vogue_F_23_we11done_26.jpg', 'vogue_F_23_lutz-huelle_43.jpg', 'vogue_F_23_undercover_15.jpg', 'vogue_F_23_saint-laurent_28.jpg', 'vogue_F_23_la-doublej_10.jpg'],
                'sexy_street': ['vogue_F_23_nensi-dojaka_2.jpg', 'vogue_F_23_bibhu-mohapatra_23.jpg', 'vogue_F_23_andreadamo_4.jpg', 'vogue_F_23_sharon-wauchob_16.jpg', 'vogue_F_23_fashion-east_32.jpg', 'vogue_F_23_msgm_34.jpg', 'vogue_F_23_gcds_8.jpg', 'vogue_F_23_hodakova_2.jpg', 'vogue_F_23_calvin-luo_40.jpg', 'vogue_F_23_chet-lo_13.jpg', 'vogue_F_23_cormio_16.jpg', 'vogue_F_23_dion-lee_39.jpg'], 
                'feminine_casual': ['vogue_F_23_roland-mouret_19.jpg', 'vogue_F_23_sally-lapointe_25.jpg', 'vogue_F_23_melitta-baumeister_27.jpg', 'vogue_F_23_niccolo-pasqualetti_20.jpg', 'vogue_F_23_sally-lapointe_28.jpg', 'vogue_F_23_duro-olowu_22.jpg', 'vogue_F_23_6397_15.jpg', 'vogue_F_23_marni_20.jpg', 'vogue_F_23_kiko-kostadinov_34.jpg', 'vogue_F_23_beatrice-b_9.jpg'],
                'elegance': ['vogue_F_23_frederick-anderson_38.jpg',  'vogue_F_23_alexander-wang_51.jpg', 'vogue_F_23_carolina-herrera_27.jpg', 'vogue_F_23_acne-studios_32.jpg', 'vogue_F_23_naeem-khan_43.jpg', 'vogue_F_23_ulla-johnson_50.jpg', 'vogue_F_23_schiaparelli_24.jpg', 'vogue_F_23_edeline-lee_27.jpg', 'vogue_F_23_fashion-east_13.jpg','vogue_F_23_jil-sander_24.jpg', 'vogue_F_23_miu-miu_7.jpg', 'vogue_F_23_zuhair-murad_38.jpg'],
                'cozy_casual': ['vogue_F_23_giorgio-armani_28.jpg', 'vogue_F_23_alyx_13.jpg',  'vogue_F_23_libertine_10.jpg', 'vogue_F_23_libertine_12.jpg', 'vogue_F_23_msgm_16.jpg', 'vogue_F_23_rosetta-getty_10.jpg', 'vogue_F_23_dries-van-noten_10.jpg', 'vogue_F_23_bibhu-mohapatra_4.jpg', 'vogue_F_23_hui_30.jpg', 'vogue_F_23_snow-xue-gao_3.jpg', 'vogue_F_23_loro-piana_9.jpg', 'vogue_F_23_nina-ricci_27.jpg', 'vogue_F_23_etro_44.jpg'],
                'chic_grunge': [ 'vogue_F_23_christian-dior_40.jpg', 'vogue_F_23_balmain_18.jpg', 'vogue_F_23_for-restless-sleepers_8.jpg','vogue_F_23_loewe_4.jpg', 'vogue_F_23_sacai_24.jpg', 'vogue_F_23_chet-lo_27.jpg', 'vogue_F_23_lafayette-148_6.jpg', 'vogue_F_23_zankov_12.jpg', 'vogue_F_23_antonio-marras_41.jpg', 'vogue_F_23_max-mara_26.jpg','vogue_F_23_marine-serre_28.jpg', 'vogue_F_23_autumn-adeigbo_1.jpg'],
                'basic_casual': ['vogue_F_23_philosophy_19.jpg', 'vogue_F_23_institut-francais-de-la-mode_74.jpg', 'vogue_F_23_dion-lee_3.jpg', 'vogue_F_23_polo-ralph-lauren_1.jpg','vogue_F_23_heron-preston_8.jpg', 'vogue_F_23_institut-francais-de-la-mode_55.jpg', 'vogue_F_23_fforme_24.jpg', 'vogue_F_23_tory-burch_20.jpg']}
                result['k'+str(i)] = style_dict
        elif i == 10 or i == 20:
            new_df = df[:]
            km_cluster = KMeans(n_clusters=i, max_iter = 1000, random_state=Rr)
            km_cluster.fit(new_df)
            cluster_label = km_cluster.labels_
            cluster_centers = km_cluster.cluster_centers_
            new_df['clusterlabel'] = cluster_label
            feature_names = new_df.columns
            cluster_details = get_cluster_details(cluster_model=km_cluster,
                                                cluster_data=new_df,
                                                feature_names=feature_names,
                                                cluster_num=i,
                                                top_n_features=10)
            top_dict = print_cluster_details(cluster_details)
            # print("top_dict", top_dict)
            result['k'+str(i)] = top_dict

            #########################################################
        else:
            result['k'+str(i)] = {}
            for j in range(i):
                result['k'+str(i)][str(j)] =  ['vogue_F_23_philosophy_19.jpg']
    return result

def makeGMMClusters(cat_attributes, year, season):
    print("#########make GMM clusters############")
    result = {}
    for i in range(13, 18):
        print("gmm_{}".format(i))
        # new_df = df.copy()
        result['g'+str(i)] = {}
        for j in range(i):
            result['g'+str(i)][str(j)] =  ['vogue_F_23_philosophy_19.jpg']
    return result
            
def print_cluster_details(cluster_details):
    top_dict = {}
    for cluster_num, cluster_detail in cluster_details.items():
        if len(cluster_detail['filenames']) > 15:
            file_num = 15
        else:
            file_num = len(cluster_detail['filenames'])
        top_dict[cluster_num] = cluster_detail['filenames'][:file_num]
    return top_dict

def get_cluster_details(cluster_model, cluster_data, feature_names,
                       cluster_num, top_n_features):
    cluster_details = {}
    center_feature_idx = cluster_model.cluster_centers_.argsort()[:,::-1]
    
    for cluster_num in range(cluster_num):
        cluster_details[cluster_num] = {}
        cluster_details[cluster_num]['cluster'] = cluster_num
        top_ftr_idx = center_feature_idx[cluster_num, :top_n_features]
        top_ftr = [feature_names[idx] for idx in top_ftr_idx]

        top_ftr_val = cluster_model.cluster_centers_[cluster_num, top_ftr_idx].tolist()
        
        cluster_details[cluster_num]['top_features'] = top_ftr
        cluster_details[cluster_num]['top_featrues_value'] = top_ftr_val
        filenames = cluster_data[cluster_data['clusterlabel']==cluster_num].index
        filenames = filenames.values.tolist()
        cluster_details[cluster_num]['filenames'] = filenames
    
    return cluster_details
def make_K_dict(selected_item,year,season):
    result = {}
    result['K-means'] = {}
    result['K-means']['clusters'] ={}
    clusters = makeKmeansClusters(list(set(selected_item)), year, season)
    for k, arr_c in enumerate(clusters):
        if arr_c == "k15":
            result['K-means']['clusters'][arr_c] = {}
            for i, c in enumerate(clusters[arr_c]):
                result['K-means']['clusters'][arr_c]['cluster'+str(i)] = {}
                result['K-means']['clusters'][arr_c]['cluster'+str(i)]['image'] = {}
                result['K-means']['clusters'][arr_c]['cluster'+str(i)]['image'] = clusters[arr_c][c]
    return result

def make_G_dict(selected_item, year,season):
    result = {}
    result['K-means'] = {}
    result['K-means']['clusters'] ={}
    print(selected_item)
    clusters = makeKmeansClusters(list(set(selected_item)), year, season)
    for k, arr_c in enumerate(clusters):
        result['K-means']['clusters'][arr_c] = {}

        if arr_c == "k15":
            for i, c in enumerate(clusters[arr_c]):
                result['K-means']['clusters'][arr_c][c] = {}
                result['K-means']['clusters'][arr_c][c]['image'] = {}
                result['K-means']['clusters'][arr_c][c]['image'] = clusters[arr_c][c]

        else:
            for i, c in enumerate(clusters[arr_c]):
                result['K-means']['clusters'][arr_c]['cluster'+str(i)] = {}
                result['K-means']['clusters'][arr_c]['cluster'+str(i)]['image'] = {}
                result['K-means']['clusters'][arr_c]['cluster'+str(i)]['image'] = clusters[arr_c][c]
    result['GMM'] = {}
    result['GMM']['clusters'] ={}
    clusters = makeGMMClusters(list(set(selected_item)), year, season)
    for k, arr_c in enumerate(clusters):
        result['GMM']['clusters'][arr_c] = {}
        for i, c in enumerate(clusters[arr_c]):
            result['GMM']['clusters'][arr_c]['cluster'+str(i)] = {}
            result['GMM']['clusters'][arr_c]['cluster'+str(i)]['image'] = {}
            result['GMM']['clusters'][arr_c]['cluster'+str(i)]['image'] = clusters[arr_c][c]
    return result