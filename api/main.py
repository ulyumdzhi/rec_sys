import os
from api.core.update_artist_names import upd_artist_name
from api.core.recommendation import recommendation
from api.core.parcer import pars
from api.core.update_dictionary_words import dict_words, dict_all_words
from api.checkers.name_checker import name_checker
from api.checkers.input_checker import input_checker
from api.loader import API_TOKEN
import pickle
from api.core.tf_idf import tfidf
import pandas as pd

tfidf_not_exists = 'TF_IDF.csv' not in os.listdir('database/')
if tfidf_not_exists:
    dictionary_words = dict_all_words()
    pickle.dump(dictionary_words, open("database/dictionary_words.pickle", "wb"))
    artists_similarity = tfidf(pickle.load(open("database/dictionary_words.pickle", 'rb')))
    pd.DataFrame(artists_similarity, index=dictionary_words.keys()).to_csv('database/TF_IDF.csv')

def recommender(name: str):
    """
    pass
    """
    
    name = input_checker(name)
    name = name_checker(name, API_TOKEN)
    df = pd.read_csv('database/artist_names.csv', sep='\t')
    if name in df['authors'].to_list():
        recommend = recommendation(name)
        return recommend
    if name not in df['authors'].to_list():
        # print('Not')
        pars(name)
        upd_artist_name(name)
        dictionary_words = dict_words(name)
        print(dictionary_words)
        pickle.dump(dictionary_words, open("database/dictionary_words.pickle", "wb"))
        artists_similarity = tfidf(pickle.load(open("database/dictionary_words.pickle", 'rb')))
        pd.DataFrame(artists_similarity, index=dictionary_words.keys()).to_csv('database/TF_IDF.csv')
        recommend = recommendation(name)
        return recommend
