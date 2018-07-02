#!coding=UTF-8
import unittest

from languagedetector.detector import LanguageDetector, load_model as _load_model
from languagedetector.constants import MODEL_JSON_FILENAME, MODEL_WEIGHT_FILENAME, LANGUAGES_JSON_FILENAME
from os import getcwd
from os.path import join as join_path
import json

TEST_CASES = (
    ('en', [
        "You might want to look into a Python package manager like pip. If you don't want to use a Python package manager, you should be able to",
        "Catalonia crisis: Spain plans for elections as independence row grows"
    ]),
    ('it', [
        "Esplode fabbrica fuochi d'artificio morto un operaio di 54 anni",
        "froppicazzola scrozzata menghiceppiola",
        "Saviano, Napoli ha bisogno di amore non di fango». Questo striscione, firmato da Napoli Nazione, è apparso sul ponte della Sanità dove tra qualche ora lo scrittore presenterà al Teatro nato nel rione il suo libro «La paranza dei bambini». Immediata la replica dell'autore con un post su Facebook: «Questo striscione campeggia a Napoli abbarbicato sul ponte della Sanità. Questo striscione lo ha messo lì chi odia Napoli."
    ]),
    ('nl', [
        '''De kamer die vrij komt bevindt zich in een huis waar in totaal 4 studenten wonen. De kamer is gestoffeerd. De TU is op de fiets in 5 minuten bereikbaar en het station en het centrum liggen op ongeveer 10 fiets minuten. Er is geen instemming. Als je belangstelling hebt voor deze kamer neem dan telefonisch of per e mail contact met mij op zodat wij een afspraak kunnen maken voor een bezichtiging.. Vermeld in ieder geval jouw telefoonnummer bij de reactie.''',
        '''Mooie huis in Amsterdam-Noord, aan de kant van water met mooi tuin met open gedeelde keuken en bar. Mooi bubbelbad in badkamer. Centrale verwarming. Snelle internet verbinding beschikbaar.''',
    ]),
    ('es', [
        '''En el arranque de la II Convención Federalista organizada por la Fundación Rafael Campalans, vinculada al PSC, Montilla ha apostado por "el diálogo, la negociación y el acuerdo" para hacer posible una reforma federal de la Constitución, aunque ha advertido de que "no todos trabajan para solucionar los problemas"''',
        '''Marc Márquez celebrará 150 Grandes Premios en el Mundial de Motociclismo este fin de semana en Valencia. Márquez suma dos''',
    ]),
    ('pt', [
        '''Em 1982, foi fundada, em Nápoles, na Itália, por Antonio Pace, a Associação da Verdadeira Pizza Napolitana, (Associazione Verace Pizza Napoletana, em italiano) com a missão de promover a culinária e a tradição da pizza napolitana, defendendo, até com certo purismo, a sua cultura, resguardando-a contra a "miscigenação" cultural que sofre a sua receita. Com estatuto preciso, normatiza as suas principais características.''',
        '''É desta massa que nós somos feitos? metade de indiferença e metade de ruindade''',
    ]),
    ('fr', [
        '''Allons enfants de la patrie  Le jour de gloire est arrivé!  Contre nous de la tyrannie  L'étendard sanglant est levé!  L'étendard sanglant est levé!  Entendez-vous dans les campagnes  Mugir ces féroces soldats?  Ils viennent jusque dans vos bras  Ecorger nos fils, et nos compagnes,  Coro  Aux armes citoyens!  Formez vos bataillons!  Marchons, marchons,  Qu’un sang impur abreuve à nos sillons!  Nous entrerons dans la carrière  Quand nos aînés n'y seront plus!  Nous y trouverons leur poussière  Et la trace de leurs vertus.  Bien moins jaloux de leur cercueil,  Nous aurons le sublime orgueil  De les venger ou de les suivre''',
        '''Le tombeur de Hillary Clinton lors de la présidentielle américaine du 8 novembre tente de calmer son parti et ses détracteurs En savoir plus sur http://www.lemonde.fr/#YdtY74HrtPQGLqtj.99 '''
    ]),
    ('de', [
        '''Die Rivalität zwischen Köln und Düssel­dorf bezeichnet das Konkurrenz­verhältnis zwischen den beiden Groß­städten im Rhein­land, die 40 Kilo­meter von­einander entfernt am Rhein liegen. Diese Rivalität wird zwar auf sportlicher und kultureller Ebene als „Feindschaft“ folkloristisch zelebriert, basiert aber auf historischen und wirtschaftlichen Fakten. Während sich das größere Köln aus einer römischen Kolonie und späteren Reichs­stadt entwickelte, ist das aus einer kleinen mittel­alterlichen Ansiedlung entstandene Düssel­dorf heute Haupt­stadt des Landes Nord­rhein-West­falen''',
        '''Offen bleibt, ab wann ein Steuerzahler als superreich gilt und unter die Vermögenssteuer fällt. "Selbstverständlich legen wir dabei besonderen Wert auf den Erhalt von Arbeitsplätzen und die Innovationskraft von Unternehmen", heißt es nur recht unkonkret in dem Beschluss.'''
    ]),
    ('sv', [
        "Nordstjernan är ett familjekontrollerat investeringsföretag vars affärsidé är att genom aktivt ägande utveckla företag och skapa god långsiktig värdetillväxt genom ökning av substansvärdet. Nordstjernan är idag ägare i ett tjugotal noterade och onoterade bolag med huvudkontor i Norden",
        "Elfsborgstränaren nobbade kontrakt med Varberg"
    ]),
    ('vi', [
        "Theo đài truyền hình Fox News, bà Alicia Legall, 46 tuổi, ra trình diện tòa hôm Thứ Ba về các tội danh, trộm cắp tiền bạc và danh tính cá nhân.",
        "Sau khi một thân nhân của ông Harp cho tiệm nữ trang Robbins Brothers ở Fullerton biết câu chuyện, chủ tiệm quyết định tặng ông chiếc nhẫn mới, cùng mẫu với chiếc nhẫn cũ, miễn phí"
    ]),
    # ('fi', [
    #     "HS Digi -palvelusta löydät lehden koko sisällön digitaalisena ja jopa vielä enemmän. Voit lukea viimeisimmät uutiset kaikilla päätelaitteilla - tietokoneella, älypuhelimella ja tabletilla missä ja milloin vain.",
    #     "Suomen metsien käyttöä EU:ssa puolustaa erään pienen puolueen presidenttiehdokas"
    # ]),
    ('ru', [
        "Надо сидеть и ждать. Станислав Белковский о новой эпохе политической истории России",
        "Цена расписок на акции \"Магнита\" на Лондонской фондовой бирже упала на 17% после публикации квартальной отчетности по МСФО, следует из данных биржи. На минимуме акции стоили $31,34 за бумагу. Капитализация компании составила $16 млрд, отмечал Bloomberg. На Московской бирже акции \"Магнита\" подешевели до 8492 рубля (–10,1%) при объеме торгов 7,187 млрд рублей."
    ]),
    ('uk', [
        "У Google Play з'явилася можливість запустити додаток без установки",
        "Водночас Нищук додав, що до оголошення проекту-переможця неможливо говорити ні про обсяги витрат, ні про дату відкриття Меморіалу."
    ]),
    # ('hu', [
    #     "Elértünk egy határig, amely cselekvésre kötelezi a kormányt – mondta a spanyol miniszterelnök Brüsszelben tartott sajtótájékoztatóján az uniós vezetők csúcstalálkozója után.",
    #     "„Regionális összehasonlításban a magyar bérek továbbra is a középmezőny végén vannak. Ám ez a hátrány az idén már látható és a következő években is kitartó bérdinamikával csökkenthető lesz” – írja Horváth András, a TakarékBank elemzője."
    # ]),
    ('pl', [
        "Ronald Reagan w czasie swej prezydentury (1981-1989) “ściśle współpracując z Fundacją Heritage obniżył podatki, aby dokonać gospodarczego cudu lat 80.” – mówił Trump podczas spotkania Klubu Prezydenta tej fundacji, skupiającego najhojniejszych darczyńców tego waszyngtońskiego think tanku.",
        "Uroczystości w Waszyngtonie zakończyły Rok Kościuszkowski w USA"
    ])
)


def load_model():
    return _load_model(
        json_filename=join_path(getcwd(), "..", "languagedetector", MODEL_JSON_FILENAME),
        weights_filename=join_path(getcwd(), "..", "languagedetector", MODEL_WEIGHT_FILENAME))


def load_languages():
    return json.load(open(join_path(getcwd(), "..", "languagedetector", LANGUAGES_JSON_FILENAME), 'r'))


class DetectorTest(unittest.TestCase):
    def test_exact_number_of_languages(self):
        n_languages = 12
        languages = load_languages()
        self.assertEqual(len(languages), n_languages)
        self.assertEqual(len(TEST_CASES), n_languages)

    def test_detect_languages(self):
        detector = LanguageDetector(load_model(), load_languages())

        for test_case in TEST_CASES:
            lang = test_case[0]
            for sentence in test_case[1]:
                analysis = sorted(detector.analyze_raw(sentence), key=lambda x: x[1], reverse=True)
                print analysis
                self.assertEqual(analysis[0][0], lang)
