"""Grupo: Ewerton de Jesus e Matheus gurjao"""

from data import word_sentiments, load_tweets
from datetime import datetime
from doctest import run_docstring_examples
from geo import us_states, geo_distance, make_position, longitude, latitude
from maps import draw_state, draw_name, draw_dot, wait, message
from string import ascii_letters
from ucb import main, trace, interact, log_current_line


# Phase 1: The Feelings in Tweets

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a python dictionary.

    text      -- A string; the text of the tweet, all in lowercase
    time      -- A datetime object; the time that the tweet was posted
    latitude  -- A number; the latitude of the tweet's location
    longitude -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_words(t)
    ['just', 'ate', 'lunch']
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}


def tweet_words(tweet):
    """ Retorna uma lista das palavras do texto no tweet."""
    return extract_words(tweet["text"])


def tweet_time(tweet):
    """ Retorna a chave time do dicionario tweet. """
    return tweet['time']


def tweet_location(tweet):
    """Retorna um tupla representando a posicao (latitude,longitude)
     da localizacao do tweet."""
    return make_position(tweet['latitude'], tweet['longitude'])


def tweet_string(tweet):
    """Return a string representing the tweet."""
    return '"{0}" @ {1}'.format(tweet['text'], tweet_location(tweet))


def extract_words(text):
    """Retorna as palavras de uma frase em um tweet, nao inclui pontuacao.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    """
    # para cada caractere na palavra verifica se eh uma letra ascii
    # retorna a frase dividida por palavras
    sempontuacao = ''
    for elemento in text:
        if elemento in ascii_letters:
            sempontuacao += elemento
        else:
            sempontuacao += ' '
    return sempontuacao.split()


def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> s = make_sentiment(0.2)
    >>> t = make_sentiment(None)
    >>> has_sentiment(s)
    True
    >>> has_sentiment(t)
    False
    >>> sentiment_value(s)
    0.2
    """
    assert value is None or (value >= -1 and value <= 1), 'Illegal value'
    # se haver setimento retorna o valor desse sentimento
    if has_sentiment(value):
        return sentiment_value(value)
    else:
        return None


def has_sentiment(s):
    """Retorna se o sentimento tem valor."""
    # se o valor do sentimento for None retorna Falso
    if s is None:
        return False
    # se o valor estiver entre -1 e 1 retorna Verdadeiro
    if s >= -1 and s <= 1:
        return True


def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    return s


def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word, if word is not in the sentiment dictionary.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    return make_sentiment(word_sentiments.get(word, None))


def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("Thinking, 'I hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet("Go bears!", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False

    """
    palavras = tweet_words(tweet)
    valor_total = 0.0
    numero_palavras = 0
    tem_sentimento = False

    # para cada palavra no tweet verifica se ela tem sentimento
    # conta quantas palavras tem sentimento e divide pelo valor total deles
    # se houver sentimento no tweet
    # caso nao tenha sentimento, retorna None.

    for palavra in palavras:
        valor_sentimento = get_word_sentiment(palavra)

        if valor_sentimento is None:
            valor_total += 0
        else:
            numero_palavras += 1
            valor_total += valor_sentimento
            tem_sentimento = True

    if tem_sentimento:
        media = valor_total/numero_palavras

        return media

    else:

        return make_sentiment(None)


# Phase 2: The Geometry of Maps


def find_centroid(polygon):
    """Find the centroid of a polygon.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    polygon -- A list of positions, in which the first and last are the same

    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area

    Hint: If a polygon has 0 area, return its first position as its centroid

    >>> p1, p2,p3 = make_position(1, 2),make_position(3, 4), make_position(5,0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> find_centroid(triangle)
    (3.0, 2.0, 6.0)
    >>> find_centroid([p1, p3, p2, p1])
    (3.0, 2.0, 6.0)
    >>> find_centroid([p1, p2, p1])
    (1, 2, 0)
    """

    vertices = len(polygon)
    somatorio_x = 0
    somatorio_y = 0

    x = 0
    y = 1
    area = polygon_area(polygon)

    # caso a area do poligono seja zero, retorna sua primeira posicao
    # como centroid
    if area == 0:
        return (polygon[0][x], polygon[0][y], int(area))

    # Aplicacao da formula Centroid x
    for i in range(0, vertices - 1):
        somatorio_x += (polygon[i][x] + polygon[i+1][x]) * \
          (polygon[i][x] * polygon[i+1][y] - polygon[i+1][x] * polygon[i][y])

    centroid_x = somatorio_x / (6 * area)

    # Aplicacao da formula Centroid y
    for j in range(0, vertices - 1):
        somatorio_y += (polygon[j][y] + polygon[j+1][y]) * \
          (polygon[j][x] * polygon[j+1][y] - polygon[j+1][x] * polygon[j][y])

    centroid_y = somatorio_y / (6 * area)

    return (centroid_x, centroid_y, abs(area))


def polygon_area(polygon):
    """ Retorna area de um poligono fechado"""

    numero_vertices = len(polygon)

    x = 0
    y = 1
    somatorio = 0
    # Aplicacao da formula area do poligono fechado
    for i in range(0, numero_vertices - 1):
        somatorio += (polygon[i][x] * polygon[i+1][y]) - \
                                     (polygon[i+1][x] * polygon[i][y])

    area = somatorio / 2

    return area


def find_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in polygons
    weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
    # dado o retorno do us_states[estado] pega o unico elemento e retorna seu
    # centroid

    centroid = find_centroid(polygons[0])

    return (centroid[0], centroid[1])

# Phase 3: The Mood of the Nation


def find_closest_state(tweet, state_centers):
    """Return the name of the state closest to the given tweet's location.

    Use the geo_distance function (already provided) to calculate distance
    in miles between two latitude-longitude positions.

    Arguments:
    tweet -- a tweet abstract data type
    state_centers -- a dictionary from state names to positions.
    >>> us_centers = {n: find_center(s) for n, s in us_states.items()}
    >>> sf = make_tweet("Welcome to San Francisco", None, 38, -122)
    >>> ny = make_tweet("Welcome to New York", None, 41, -74)
    >>> find_closest_state(sf, us_centers)
    'CA'
    >>> find_closest_state(ny, us_centers)
    'NJ'
    """

    localizacao_tweet = (tweet['latitude'], tweet['longitude'])
    distancia_minima = None
    # em cada estado verifica qual a distancia relativa a localizacao do tweet
    # se ela for minima guarda a inicial do estado
    # ao fim retorna a inicial do estado mais proximo
    for estado in state_centers:
        distancia_estado = geo_distance(state_centers[estado], localizacao_tweet)
        if distancia_minima is None:
            distancia_minima = distancia_estado
            iniciais = estado
        else:
            if distancia_minima > distancia_estado:
                distancia_minima = distancia_estado
                iniciais = estado
    return iniciais


def group_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their nearest state center.

    The keys of the returned dictionary are state names, and the values are
    lists of tweets that appear closer to that state center than any other.

    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("Welcome to San Francisco", None, 38, -122)
    >>> ny = make_tweet("Welcome to New York", None, 41, -74)
    >>> ca_tweets = group_tweets_by_state([sf, ny])['CA']
    >>> tweet_string(ca_tweets[0])
    '"Welcome to San Francisco" @ (38, -122)'
    """
    tweets_by_state = {}
    us_centers = {}

    # gera dicionario us center com o estado como chave e seu centro como valor
    for estado, poligono in us_states.items():
        us_centers[estado] = find_center(poligono)

    # para cada tweet verifica qual estado mais proximo e os agrupa por estado
    # se exite a chave concatena a lista [tweet]
    # se nao existe, cria a chave com a lista [tweet]
    for tweet in tweets:
        estado_mais_proximo = find_closest_state(tweet, us_centers)
        if estado_mais_proximo in tweets_by_state:
            tweets_by_state[estado_mais_proximo] += [tweet]
        else:
            tweets_by_state[estado_mais_proximo] = [tweet]

    return tweets_by_state


def most_talkative_state(term):
    """Return the state that has the largest number of tweets containing term.

    >>> most_talkative_state('texas')
    'TX'
    >>> most_talkative_state('sandwich')
    'NJ'
    """
    tweets = load_tweets(make_tweet, term)
    # agrupa os tweets por estado
    por_estado = group_tweets_by_state(tweets)
    maior = 0
    # verifica o tamanho de cada lista do dicionario pro estado
    # e verifica se o tamanho dela eh maior que a variavel maior
    # caso for, declara a variavel maior como o tamanho da lista na chave valor
    # retorna o estado com mais tweets
    for valor in por_estado:
        if len(por_estado[valor]) >= maior:
            maior = len(por_estado[valor])
            maior_estado = valor
    return maior_estado


def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely. -> Do NOT include states with no tweets, or with
    tweets that have no sentiment, as 0.  0 represents neutral sentiment, not
    unknown sentiment.

    tweets_by_state -- A dictionary from state names to lists of tweets
    """
    averaged_state_sentiments = {}
    # para cada estado como chave no dicionario tweets_by_state
    # verifica qual a soma das medias dos valores dos sentimentos de cada tweet
    # e faz a media com o numero de palvras com sentimentos
    # se o numero_tweets_com_sentimentos for diff de zero coloca no dicionario

    for estado in tweets_by_state.keys():
        soma_estado = 0
        numero_tweets_com_sentimentos = 0

        list_tweets_estado = tweets_by_state[estado]
        for tweet in list_tweets_estado:
            media_tweet = analyze_tweet_sentiment(tweet)
            if media_tweet is not None:
                numero_tweets_com_sentimentos += 1
                soma_estado += media_tweet
        if numero_tweets_com_sentimentos != 0:
            averaged_state_sentiments[estado] = soma_estado / \
                                                numero_tweets_com_sentimentos

    # retorna o valor medio dos sentimentos por estado
    return averaged_state_sentiments


# Phase 4: Into the Fourth Dimension


def group_tweets_by_hour(tweets):

    """Return a dictionary that groups tweets by the hour they were posted.
    The keys of the returned dictionary are the integers 0 through 23.

    The values are lists of tweets, where tweets_by_hour[i] is the list of all
    tweets that were posted between hour i and hour i + 1. Hour 0 refers to
    midnight, while hour 23 refers to 11:00PM.

    To get started, read the Python Library documentation for datetime objects:
    http://docs.python.org/py3k/library/datetime.html#datetime.datetime

    tweets -- A list of tweets to be grouped
    """
    # cria um dicionario com chaves de 0 a 23 e listas como valor
    tweets_by_hour = {hora: [] for hora in range(24)}

    # para cada tweet ve a hora e concatena na lista da chave hora
    for tweet in tweets:
        tempo = tweet_time(tweet)
        horas = tempo.hour
        tweets_by_hour[horas] += [tweet]

    return tweets_by_hour


# Interaction.  You don't need to read this section of the program.


def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    assert words, 'No words extracted from "' + text + '"'
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in extract_words(text.lower()):
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))


def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    us_centers = {n: find_center(s) for n, s in us_states.items()}
    center = us_centers[center_state.upper()]
    dist_from_center = lambda name: geo_distance(center, us_centers[name])
    for name in sorted(us_states.keys(), key=dist_from_center)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, us_centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()


def draw_state_sentiments(state_sentiments={}):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        sentiment = state_sentiments.get(name, None)
        draw_state(shapes, sentiment)
    for name, shapes in us_states.items():
        center = find_center(shapes)
        if center is not None:
            draw_name(name, center)


def draw_map_for_term(term='my job'):
    """Draw the sentiment map corresponding to the tweets that contain term.

    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()


def draw_map_by_hour(term='my job', pause=0.5):
    """Draw the sentiment map for tweets that match term, for each hour."""
    tweets = load_tweets(make_tweet, term)
    tweets_by_hour = group_tweets_by_hour(tweets)

    for hour in range(24):
        current_tweets = tweets_by_hour.get(hour, [])
        tweets_by_state = group_tweets_by_state(current_tweets)
        state_sentiments = average_sentiments(tweets_by_state)
        draw_state_sentiments(state_sentiments)
        message("{0:02}:00-{0:02}:59".format(hour))
        wait(pause)


def run_doctests(names):
    """Run verbose doctests for all functions in space-separated names."""
    g = globals()
    errors = []
    for name in names.split():
        if name not in g:
            print("No function named " + name)
        else:
            if run_docstring_examples(g[name], g, True) is not None:
                errors.append(name)
    if len(errors) == 0:
        print("Test passed.")
    else:
        print("Error(s) found in: " + ', '.join(errors))


@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--run_doctests', '-t', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_term', '-m', action='store_true')
    parser.add_argument('--draw_map_by_hour', '-b', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    for name, execute in args.__dict__.items():
        if name != 'text' and execute:
            globals()[name](' '.join(args.text))
