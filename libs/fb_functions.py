
import pandas as pd
import facebook
import json

def get_reaction_from_post( row : pd.core.series.Series ) -> pd.core.series.Series:
    from extracting_data_fb_to_mongo_few_functional import graph
    post_id = row['id']
    reactions = graph.get_connections(post_id, 'reactions', fields='pic,name,pic_large,profile_type,pic_crop,can_post,type,link,id')
    #Para irnos moviendo entre las páginas
    paging = reactions.get('paging')
    reactions = reactions['data']

    for react in reactions:
        row[ react['type'].lower() ] +=1
        row[ 'users_likes' ].append( react['name'] )
    return row

def create_document( row : pd.Series ) -> pd.Series :
    return row.to_dict()