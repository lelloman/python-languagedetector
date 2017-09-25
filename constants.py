#!/usr/bin/python
#coding=UTF-8

import re

LANGUAGES_JSON_FILENAME = "languages.json"
DATASET_DIR = "wikidataset"
MODEL_JSON_FILENAME = "model.json"
MODEL_WEIGHT_FILENAME = "model.h5"

MAX_SENTENCE_LENGTH = 20
MIN_TRAIN_SAMPLE_LENGTH = 10
MAX_TRAIN_SAMPLE_LENGTH = MAX_SENTENCE_LENGTH * 2


def string_to_sequence(s):
    return bytearray(re.sub(r'[^\w\s0-9\'-]', '', s.lower().replace('\n', ''), flags=re.UNICODE))


def pad_word(word):
    out = bytearray(MAX_SENTENCE_LENGTH)
    out[MAX_SENTENCE_LENGTH - len(word):] = word
    return out

TEST_TEXTS = [

    # made up words...
    '''froppicazzola scrozzata menghiceppiola''',

    '''Saviano, Napoli ha bisogno di amore non di fango». Questo striscione, firmato da Napoli Nazione, è apparso sul ponte della Sanità dove tra qualche ora lo scrittore presenterà al Teatro nato nel rione il suo libro «La paranza dei bambini». Immediata la replica dell'autore con un post su Facebook: «Questo striscione campeggia a Napoli abbarbicato sul ponte della Sanità. Questo striscione lo ha messo lì chi odia Napoli.''',
    '''Cavalieri, ufficiali o commendatori, a secondo dei casi, che il capo dello Stato ha scelto "motu proprio", fuori cioè da quelle che sono le tradizionali assegnazioni previste, come per esempio quelle dei cavalieri del lavoro, proprio a sottolineare la straordinarietà dell'evento. Nell'ottobre del 2015 il presidente scelse 18 casi meritevoli. Quest'anno sono più del doppio. Che saranno ricevuti e premiati al Quirinale probabilmente il prossimo gennaio. La lista, lo specchio dell'Italia migliore. In tutti i diversi camp''',

    '''Die Rivalität zwischen Köln und Düssel­dorf bezeichnet das Konkurrenz­verhältnis zwischen den beiden Groß­städten im Rhein­land, die 40 Kilo­meter von­einander entfernt am Rhein liegen. Diese Rivalität wird zwar auf sportlicher und kultureller Ebene als „Feindschaft“ folkloristisch zelebriert, basiert aber auf historischen und wirtschaftlichen Fakten. Während sich das größere Köln aus einer römischen Kolonie und späteren Reichs­stadt entwickelte, ist das aus einer kleinen mittel­alterlichen Ansiedlung entstandene Düssel­dorf heute Haupt­stadt des Landes Nord­rhein-West­falen''',
    '''Offen bleibt, ab wann ein Steuerzahler als superreich gilt und unter die Vermögenssteuer fällt. "Selbstverständlich legen wir dabei besonderen Wert auf den Erhalt von Arbeitsplätzen und die Innovationskraft von Unternehmen", heißt es nur recht unkonkret in dem Beschluss.''',

    '''De kamer die vrij komt bevindt zich in een huis waar in totaal 4 studenten wonen. De kamer is gestoffeerd. De TU is op de fiets in 5 minuten bereikbaar en het station en het centrum liggen op ongeveer 10 fiets minuten. Er is geen instemming. Als je belangstelling hebt voor deze kamer neem dan telefonisch of per e mail contact met mij op zodat wij een afspraak kunnen maken voor een bezichtiging.. Vermeld in ieder geval jouw telefoonnummer bij de reactie.''',
    '''Mooie huis in Amsterdam-Noord, aan de kant van water met mooi tuin met open gedeelde keuken en bar. Mooi bubbelbad in badkamer. Centrale verwarming. Snelle internet verbinding beschikbaar.''',

    '''Nothing worked for me. All I was seeing was the HTML of the login page, coming back to the client side with code 200. (302 at first but the same Ajax request loading login page inside another Ajax request, which was supposed to be a redirect rather than loading plain text of the login page).''',
    '''Your call to unicode() is working correctly. It is the concatenation, which is adding a unicode object to a byte string, that is causing trouble. If you change the first line to, (or u'<tr><td>') it should work fine.''',

    '''En el arranque de la II Convención Federalista organizada por la Fundación Rafael Campalans, vinculada al PSC, Montilla ha apostado por "el diálogo, la negociación y el acuerdo" para hacer posible una reforma federal de la Constitución, aunque ha advertido de que "no todos trabajan para solucionar los problemas"''',
    '''Marc Márquez celebrará 150 Grandes Premios en el Mundial de Motociclismo este fin de semana en Valencia. Márquez suma dos''',

    '''Em 1982, foi fundada, em Nápoles, na Itália, por Antonio Pace, a Associação da Verdadeira Pizza Napolitana, (Associazione Verace Pizza Napoletana, em italiano) com a missão de promover a culinária e a tradição da pizza napolitana, defendendo, até com certo purismo, a sua cultura, resguardando-a contra a "miscigenação" cultural que sofre a sua receita. Com estatuto preciso, normatiza as suas principais características.''',
    '''É desta massa que nós somos feitos? metade de indiferença e metade de ruindade''',

    '''Allons enfants de la patrie  Le jour de gloire est arrivé!  Contre nous de la tyrannie  L'étendard sanglant est levé!  L'étendard sanglant est levé!  Entendez-vous dans les campagnes  Mugir ces féroces soldats?  Ils viennent jusque dans vos bras  Ecorger nos fils, et nos compagnes,  Coro  Aux armes citoyens!  Formez vos bataillons!  Marchons, marchons,  Qu’un sang impur abreuve à nos sillons!  Nous entrerons dans la carrière  Quand nos aînés n'y seront plus!  Nous y trouverons leur poussière  Et la trace de leurs vertus.  Bien moins jaloux de leur cercueil,  Nous aurons le sublime orgueil  De les venger ou de les suivre''',
    '''Le tombeur de Hillary Clinton lors de la présidentielle américaine du 8 novembre tente de calmer son parti et ses détracteurs En savoir plus sur http://www.lemonde.fr/#YdtY74HrtPQGLqtj.99 '''
]


