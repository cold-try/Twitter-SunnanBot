import tweepy
import random
import csv
import re


def connexion():
    " Connecting to tweeter API "

    client = tweepy.Client(
        consumer_key="",
        consumer_secret="",
        access_token="",
        access_token_secret=""
    )
    return client


def tweet_creation(client, toTweet):
    " Publication of the tweet (thread, or normal) "

    length_of_hadith = len(toTweet)

    if length_of_hadith > 1:
        last_tweet_id = None       
        for i in range(0, length_of_hadith):
            if i==0:
                last_tweet = client.create_tweet(text=toTweet[0])
            else:
                last_tweet = client.create_tweet(text=toTweet[i], in_reply_to_tweet_id=last_tweet_id)
            last_tweet_id = last_tweet.data['id']
    else: 
        client.create_tweet(text=toTweet)


def white_space_finder(text):
    """ If the last character of the string is not a white space 
    the function returns the corrective index to the next space """

    correction = 1
    while True:
        if text[-correction] != ' ':
            correction += 1
        else:
            break
    return correction


def formatageHadith(hadith_base):
    """ If the length of the text is greater than the character limit of a tweet (280) 
    then the function will return the undercut text in the form of a list (thread) """

    final_hadith = []
    hadith_length = len(hadith_base)
    tweet_limit = 252

    corrector_index = 1
    last_corrector_index = 0
    
    if hadith_length > 280:
        counter_limit = hadith_length // tweet_limit

        for i in range(0, counter_limit+1):
            piece = hadith_base[tweet_limit*i:tweet_limit*(i+1)]
            
            if i != counter_limit:
                corrector_index = white_space_finder(piece)
                
                if corrector_index > 1:
                    final_hadith.append( hadith_base[tweet_limit*i - last_corrector_index : tweet_limit*(i+1)-corrector_index ].strip() + ' (...) ⬇️' )
                    last_corrector_index = corrector_index
                    corrector_index = 1
                else:
                    final_hadith.append( hadith_base[tweet_limit*i - last_corrector_index : (tweet_limit*(i+1))].strip() + ' (...) ⬇️')
                    last_corrector_index = corrector_index

            else:
                final_hadith.append(hadith_base[tweet_limit*i - last_corrector_index : tweet_limit*(i+1)].strip())
    else:
        final_hadith.append(hadith_base)

    return final_hadith


def getHadith():
    " Returns a hadith randomly "

    selectionned_hadith = None
    kutub = [
        ['muslim', 514],
        ['ibnmajah', 157],
        ['nasai', 57],
        ['abidaoud', 275],
        ['albukhari', 618],
        ['tirmidhi', 336],
        ['ryadassalihine', 71],
        ['nawawi', 42],
        ['alalbany', 1181]
    ]

    random.shuffle(kutub)
    random.shuffle(kutub)

    max_index_kitab = kutub[4][1]
    selectionned_kitab = kutub[4][0]
    selectionned_hadith_index = random.randint(0,max_index_kitab)

    with open(f'datas/{selectionned_kitab}.csv', 'r',) as file:
        reader = csv.reader(file)
        counter = 0
        for row in reader:
            if counter == selectionned_hadith_index:
                selectionned_hadith = row
                break
            else:
                counter += 1

    return selectionned_hadith


def cleaner(hadith):
    " Remove unexpected characters from text "

    selectionned_hadith_first_cleaner = str(hadith).strip("[]")
    selectionned_hadith_second_cleaner = re.sub(r'\\n', '', selectionned_hadith_first_cleaner)
    cleaned_hadith = re.sub(r'\n', '', selectionned_hadith_second_cleaner)
    return cleaned_hadith.strip("'")


def launcher():
    " Application entry point "

    client = connexion()
    selectionned_hadith = getHadith()
    cleaned_hadith = cleaner(selectionned_hadith)
    hadith_to_tweet = formatageHadith(cleaned_hadith)
    tweet_creation(client, hadith_to_tweet)