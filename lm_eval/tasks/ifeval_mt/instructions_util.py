# Copyright 2023 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility library of instructions."""

import functools
import random
import re

import immutabledict
import nltk
import pkg_resources
from packaging import version


# Downloading 'punkt' with nltk<3.9 has a remote code vuln.
# see  https://github.com/EleutherAI/lm-evaluation-harness/issues/2210
# and https://github.com/nltk/nltk/issues/3266
# for more information.
NLTK_MIN_VERSION = "3.9.1"


def download_nltk_resources():
    """Download 'punkt' if not already installed"""
    nltk_version = pkg_resources.get_distribution("nltk").version
    assert (
        version.parse(nltk_version) >= version.parse(NLTK_MIN_VERSION)
    ), f"`nltk` version {nltk_version} is not >= {NLTK_MIN_VERSION}. Please update `nltk` before proceeding--older versions are vulnerable to a remote code execution vulnerability."

    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt_tab")


download_nltk_resources()

WORD_LIST = [
    "länsimainen",
    "tuomita",
    "signaali",
    "kaatopaikka",
    "paikalla",
    "vastapäätä",
    "pohja",
    "peruna",
    "hallinto",
    "työskentelee",
    "tervetuloa",
    "aamu",
    "hyvä",
    "virasto",
    "ensisijainen",
    "toivoa",
    "vastuuta",
    "paina",
    "ongelma",
    "presidentti",
    "varastaa",
    "harjata",
    "lukea",
    "tyyppi",
    "lyödä",
    "kouluttaja",
    "kasvu",
    "lukko",
    "luuta",
    "tapaus",
    "yhtäläinen",
    "mukava",
    "alueella",
    "korvaaminen",
    "suorituskykyä",
    "kaveri",
    "kävellä",
    "lääke",
    "elokuva",
    "asia",
    "rock",
    "napauta",
    "kokonais-",
    "kilpailua",
    "helppous",
    "etelään",
    "perustaminen",
    "kerätä",
    "pysäköinti",
    "maailman-",
    "paljon",
    "hengitys",
    "väittää",
    "alkoholia",
    "kauppaa",
    "rakas",
    "kohokohta",
    "katu",
    "asia",
    "päätös",
    "sotku",
    "sopimus",
    "studio",
    "valmentaja",
    "auttaa",
    "aivot",
    "siipi",
    "tyyli",
    "yksityinen",
    "alkuun",
    "ruskea",
    "jalka",
    "ostaa",
    "menettelyä",
    "menetelmä",
    "nopeus",
    "korkea",
    "yritys",
    "arvokasta",
    "piirakka",
    "analyytikko",
    "istunto",
    "kuvio",
    "piiri",
    "ilo",
    "päivällinen",
    "uima",
    "vitsi",
    "tilata",
    "levy",
    "osasto",
    "moottori",
    "solu",
    "viettää",
    "kaappi",
    "ero",
    "tehoa",
    "tutkimus",
    "moottori",
    "hevonen",
    "ulottuvuus",
    "maksaa",
    "varvas",
    "käyrä",
    "kirjallisuus",
    "vaivautua",
    "palo",
    "mahdollisuus",
    "keskustelu",
    "toimintaa",
    "kulku",
    "Hei",
    "sykli",
    "tausta",
    "hiljainen",
    "kirjoittaja",
    "vaikutus",
    "näyttelijä",
    "sivu",
    "polkupyörä",
    "virhe",
    "kurkku",
    "hyökkäys",
    "merkki",
    "puhelin",
    "teetä",
    "lisätä",
    "tulokset",
    "tiedosto",
    "erityisiä",
    "tarkastaja",
    "sisäinen",
    "potentiaalia",
    "henkilöstöä",
    "rakentaminen",
    "työnantaja",
    "kenkä",
    "käsi",
    "suunta",
    "puutarha",
    "ostaa",
    "haastatella",
    "opiskella",
    "tunnustaminen",
    "jäsen",
    "henkistä",
    "uuni",
    "voileipä",
    "outo",
    "matkustaja",
    "erityisesti",
    "vastaus",
    "reaktio",
    "koko",
    "vaihtelua",
    "a",
    "peruuttaa",
    "karkkia",
    "poistu",
    "vieras",
    "kunto",
    "lentää",
    "hinta",
    "heikkous",
    "muuntaa",
    "hotelli",
    "hienoa",
    "suuhun",
    "mieleen",
    "laulu",
    "sokeria",
    "epäilty",
    "puhelin",
    "korva",
    "katto",
    "maali",
    "jääkaappi",
    "organisaatio",
    "tuomaristo",
    "palkita",
    "suunnittelu",
    "päivä",
    "hallinta",
    "miehistö",
    "baari",
    "tie",
    "kuvaus",
    "juhla",
    "pisteet",
    "merkki",
    "kirje",
    "suihku",
    "ehdotus",
    "sir",
    "onnea",
    "kansallinen",
    "edistystä",
    "sali",
    "aivohalvaus",
    "teoria",
    "tarjous",
    "tarina",
    "verottaa",
    "määritelmä",
    "historia",
    "ratsastaa",
    "keskikokoinen",
    "avaaminen",
    "lasi",
    "Hissi",
    "vatsa",
    "kysymys",
    "kyky",
    "johtava",
    "kylä",
    "tietokone",
    "kaupunki",
    "suuri",
    "luottamusta",
    "kynttilä",
    "pappi",
    "suositus",
    "kohta",
    "tarpeellista",
    "kehon",
    "vastaanotto",
    "salaisuus",
    "kauhu",
    "melua",
    "kulttuuri",
    "Varoitus",
    "vettä",
    "pyöristää",
    "ruokavalio",
    "kukka",
    "linja-auto",
    "kova",
    "lupa",
    "viikko",
    "kehote",
    "yhteys",
    "väärinkäyttö",
    "korkeus",
    "tallentaa",
    "nurkkaan",
    "rajaa",
    "korostaa",
    "ajaa",
    "stop",
    "repiä",
    "ateria",
    "kuunnella",
    "hämmennystä",
    "tyttöystävä",
    "elävät",
    "suhde",
    "merkitys",
    "suunnitelma",
    "luova",
    "tunnelmaa",
    "syyttää",
    "kutsua",
    "asuminen",
    "paperia",
    "juoda",
    "rullaa",
    "hopea",
    "humalassa",
    "ikä",
    "vahingoittaa",
    "savu",
    "ympäristöön",
    "pakata",
    "säästöjä",
    "vaikutus",
    "turisti",
    "sade",
    "lähettää",
    "merkki",
    "isoäiti",
    "juosta",
    "voittoa",
    "työnnä",
    "virkailija",
    "lopullinen",
    "viiniä",
    "uida",
    "tauko",
    "tavaraa",
    "laulaja",
    "hautajaiset",
    "keskimäärin",
    "lähde",
    "näkymä",
    "perinne",
    "henkilökohtainen",
    "lumi",
    "kukaan",
    "etäisyys",
    "järjestellä",
    "herkkä",
    "eläin",
    "pääaine",
    "neuvottelu",
    "napsauta",
    "mielialaa",
    "ajanjaksoa",
    "saapuminen",
    "ilmaisua",
    "loma",
    "toistaa",
    "pöly",
    "vaatekaappi",
    "kulta",
    "huono",
    "purjehtia",
    "yhdistelmä",
    "vaatteet",
    "painotus",
    "velvollisuus",
    "musta",
    "askel",
    "kouluun",
    "hypätä",
    "asiakirja",
    "ammattilainen",
    "huuli",
    "kemiallinen",
    "edessä",
    "herätä",
    "samalla kun",
    "sisällä",
    "katsella",
    "rivi",
    "aihe",
    "rangaistus",
    "saldo",
    "mahdollista",
    "aikuinen",
    "sivuun",
    "näyte",
    "valittaa",
    "häät",
    "syvyys",
    "kuningas",
    "myöntää",
    "vaimo",
    "isku",
    "sivusto",
    "leiri",
    "musiikkia",
    "turvallinen",
    "lahja",
    "vika",
    "arvaus",
    "toimia",
    "häpeä",
    "draama",
    "pääomaa",
    "tentti",
    "tyhmä",
    "tallentaa",
    "ääni",
    "swing",
    "romaani",
    "minimi",
    "suhde",
    "kone",
    "muoto",
    "johtaa",
    "toimintaa",
    "palkkaa",
    "pilvi",
    "asia",
    "osuma",
    "luku",
    "vaiheessa",
    "määrä",
    "pääsy",
    "armeija",
    "ketju",
    "liikennettä",
    "potkia",
    "analyysi",
    "lentokenttä",
    "aika",
    "loma",
    "filosofia",
    "pallo",
    "rinnassa",
    "Kiitos",
    "paikka",
    "vuori",
    "mainonta",
    "punainen",
    "mennyt",
    "vuokrata",
    "palata",
    "kiertue",
    "talo",
    "rakentaminen",
    "net",
    "syntyperäinen",
    "sota",
    "kuva",
    "maksu",
    "spray",
    "käyttäjä",
    "lika",
    "ammuttu",
    "tehtävä",
    "keppi",
    "ystävä",
    "ohjelmisto",
    "edistäminen",
    "vuorovaikutusta",
    "surround",
    "lohko",
    "tarkoitus",
    "harjoitella",
    "konflikti",
    "rutiini",
    "vaatimus",
    "bonus",
    "reikä",
    "osavaltio",
    "juniori",
    "makea",
    "saalis",
    "repiä",
    "taita",
    "seinään",
    "toimittaja",
    "elämää",
    "asema",
    "punta",
    "kunnioittaminen",
    "kylpyhuone",
    "takki",
    "käsikirjoitus",
    "job",
    "opettaa",
    "syntymästä",
    "näkymä",
    "ratkaista",
    "teema",
    "työntekijä",
    "epäillä",
    "markkinoida",
    "koulutus",
    "palvella",
    "toipua",
    "sävy",
    "vahingoittaa",
    "neiti",
    "liitto",
    "ymmärtäminen",
    "lehmä",
    "joki",
    "yhdistys",
    "käsite",
    "koulutusta",
    "resepti",
    "suhdetta",
    "varata",
    "masennus",
    "todiste",
    "hiukset",
    "tuloja",
    "riippumaton",
    "hissi",
    "toimeksianto",
    "väliaikaista",
    "määrä",
    "menetys",
    "reuna",
    "seurata",
    "tarkista",
    "köysi",
    "arvio",
    "saastuminen",
    "vakaa",
    "viesti",
    "toimitus",
    "näkökulmasta",
    "peili",
    "avustaja",
    "edustaja",
    "todistaja",
    "luonto",
    "tuomari",
    "hedelmää",
    "kärki",
    "paholainen",
    "kaupunki",
    "hätätilanteessa",
    "ylempi",
    "pudota",
    "pysyä",
    "ihmisen",
    "kaula",
    "puhuja",
    "verkkoon",
    "laulaa",
    "vastustaa",
    "liigassa",
    "matka",
    "allekirjoitus",
    "lakimies",
    "merkitys",
    "kaasua",
    "valinta",
    "insinööri",
    "menestys",
    "osa",
    "ulkoinen",
    "työntekijä",
    "yksinkertainen",
    "neljännes",
    "opiskelija",
    "sydän",
    "syöttö",
    "paheksuntaa",
    "siirtää",
    "karkea",
    "nainen",
    "ruoho",
    "yhteisöä",
    "autotalli",
    "nuoriso",
    "standardi",
    "hame",
    "lupaus",
    "sokea",
    "televisio",
    "sairaus",
    "komissio",
    "positiivinen",
    "energiaa",
    "rauhallinen",
    "läsnäolo",
    "virittää",
    "perusteella",
    "etusija",
    "pää",
    "yleinen",
    "leikata",
    "jonnekin",
    "esittely",
    "nykyinen",
    "ajatteli",
    "vallankumous",
    "vaivaa",
    "hallita",
    "toteuttaa",
    "tasavalta",
    "kerros",
    "periaate",
    "muukalainen",
    "olkapää",
    "luokka",
    "painiketta",
    "tennis",
    "valvoa",
    "kokoelma",
    "tili",
    "rekisteröidy",
    "käsine",
    "jakaa",
    "professori",
    "tuoli",
    "etusijalla",
    "yhdistää",
    "rauhaa",
    "laajennus",
    "ehkä",
    "ilta",
    "kehys",
    "sisko",
    "aalto",
    "koodi",
    "sovellus",
    "hiiri",
    "ottelu",
    "laskuri",
    "pullo",
    "puoli",
    "poski",
    "resoluutio",
    "takaisin",
    "tietoa",
    "tehdä",
    "keskustelua",
    "ruuvi",
    "pituus",
    "onnettomuus",
    "taistelu",
    "pukeutua",
    "polvi",
    "loki",
    "paketti",
    "se",
    "käännä",
    "kuulo",
    "sanomalehti",
    "kerros",
    "varallisuus",
    "profiili",
    "mielikuvitus",
    "vastaus",
    "viikonloppu",
    "opettaja",
    "ulkonäkö",
    "tavata",
    "pyörä",
    "nousta",
    "vyö",
    "kaatua",
    "kulho",
    "vastaava",
    "tukea",
    "kuva",
    "runo",
    "riskiä",
    "jännitystä",
    "kaukana",
    "sihteeri",
    "julkinen",
    "tuottaa",
    "kone",
    "näyttö",
    "rahaa",
    "hiekka",
    "tilanne",
    "booli",
    "asiakas",
    "otsikko",
    "ravista",
    "kiinnitys",
    "vaihtoehto",
    "määrä",
    "pop",
    "ikkuna",
    "laajuus",
    "ei mitään",
    "kokea",
    "lausunto",
    "lähtöä",
    "tanssi",
    "osoitus",
    "poika",
    "materiaalia",
    "bändi",
    "johtaja",
    "aurinko",
    "kaunis",
    "lihas",
    "maanviljelijä",
    "lajike",
    "rasvaa",
    "kahva",
    "johtaja",
    "mahdollisuus",
    "kalenteri",
    "ulkopuolella",
    "vauhti",
    "kylpy",
    "kalastaa",
    "seurauksena",
    "laittaa",
    "omistaja",
    "mennä",
    "lääkäri",
    "tiedot",
    "jakaa",
    "satuttaa",
    "suojaa",
    "ura",
    "rahoitusta",
    "pakottaa",
    "golf",
    "roskat",
    "näkökohta",
    "lapsi",
    "ruokaa",
    "boot",
    "maitoa",
    "vastata",
    "tavoite",
    "todellisuutta",
    "raaka",
    "rengas",
    "ostoskeskus",
    "yksi",
    "vaikutus",
    "alueella",
    "uutiset",
    "kansainvälinen",
    "sarja",
    "tehdä",
    "äiti",
    "suojaa",
    "lakko",
    "lainata",
    "kuukausi",
    "istuin",
    "mitään",
    "viihde",
    "tuttua",
    "vihje",
    "vuosi",
    "iloinen",
    "supermarket",
    "luonnollinen",
    "jumala",
    "maksaa",
    "keskustelu",
    "solmio",
    "pilata",
    "mukavuus",
    "maata",
    "myrsky",
    "prosentteina",
    "apua",
    "budjetti",
    "vahvuus",
    "alku",
    "nukkua",
    "muu",
    "nuori",
    "yksikkö",
    "täyttää",
    "tallentaa",
    "halu",
    "piilottaa",
    "arvo",
    "kuppi",
    "huolto",
    "sairaanhoitaja",
    "toiminto",
    "torni",
    "rooli",
    "luokkaa",
    "kamera",
    "tietokanta",
    "paniikki",
    "kansakunta",
    "kori",
    "jäätä",
    "taide",
    "henki",
    "kartoittaa",
    "vaihtaa",
    "palautetta",
    "lausunto",
    "maine",
    "haku",
    "metsästää",
    "käyttää",
    "ilkeä",
    "huomautus",
    "uros",
    "piha",
    "vuosittain",
    "kaulus",
    "päivämäärä",
    "alusta",
    "kasvi",
    "onni",
    "intohimo",
    "ystävyys",
    "levitän",
    "syöpä",
    "lippu",
    "asenne",
    "saari",
    "aktiivinen",
    "esine",
    "palvelua",
    "ostaja",
    "purra",
    "kortti",
    "kasvot",
    "pihvi",
    "ehdotus",
    "kärsivällinen",
    "lämpöä",
    "sääntö",
    "asukas",
    "laaja",
    "politiikka",
    "länteen",
    "veitsi",
    "asiantuntija",
    "tyttö",
    "design",
    "suolaa",
    "baseball",
    "napata",
    "tarkastus",
    "serkku",
    "pari",
    "lehti",
    "kokki",
    "riippuvainen",
    "turvallisuus",
    "kana",
    "versio",
    "valuutta",
    "tikapuut",
    "järjestelmä",
    "keittiö",
    "työllisyyttä",
    "paikallinen",
    "Huomio",
    "johtaja",
    "tosiasia",
    "kansi",
    "surullinen",
    "vartija",
    "suhteellinen",
    "lääni",
    "korko",
    "lounas",
    "ohjelmoida",
    "aloite",
    "vaihde",
    "silta",
    "rinta",
    "puhua",
    "ruokalaji",
    "takuu",
    "olut",
    "ajoneuvoa",
    "vastaanotto",
    "nainen",
    "aine",
    "kopioida",
    "luento",
    "etu",
    "pysäköidä",
    "kylmä",
    "kuolema",
    "sekoita",
    "pidä",
    "mittakaavassa",
    "huomenna",
    "verta",
    "pyytää",
    "vihreä",
    "evästeen",
    "kirkko",
    "nauhat",
    "ikuisesti",
    "pidemmälle",
    "velkaa",
    "puuttua",
    "pestä",
    "jälkeen",
    "tuntea",
    "maksimi",
    "alalla",
    "meri",
    "omaisuutta",
    "taloustiede",
    "valikosta",
    "penkki",
    "yrittää",
    "kieli",
    "aloita",
    "soittaa",
    "kiinteä",
    "osoite",
    "tulot",
    "jalka",
    "vanhempi",
    "hunaja",
    "muutama",
    "seos",
    "käteistä",
    "päivittäistavarakauppa",
    "linkki",
    "kartta",
    "muodossa",
    "tekijä",
    "potti",
    "malli",
    "kirjailija",
    "maatilalla",
    "talvi",
    "taito",
    "missä",
    "syntymäpäivä",
    "politiikkaa",
    "vapauttaa",
    "aviomies",
    "lab",
    "kiire",
    "postia",
    "laitteet",
    "pesuallas",
    "pari",
    "kuljettaja",
    "huomioon",
    "nahka",
    "ihoa",
    "sininen",
    "vene",
    "myyntiin",
    "tiili",
    "kaksi",
    "syöttää",
    "neliö",
    "piste",
    "kiire",
    "unelma",
    "sijainti",
    "iltapäivällä",
    "valmistaja",
    "ohjata",
    "tilaisuus",
    "ongelmia",
    "esittely",
    "neuvoja",
    "veto",
    "syödä",
    "tappaa",
    "luokkaan",
    "tavalla",
    "toimisto",
    "kiinteistö",
    "ylpeys",
    "tietoisuutta",
    "lipsahdus",
    "crack",
    "asiakas",
    "naulata",
    "ampua",
    "jäsenyys",
    "pehmeä",
    "ketään",
    "web",
    "virallinen",
    "yksilöllinen",
    "pizza",
    "kiinnostaa",
    "laukku",
    "loitsu",
    "ammatti",
    "kuningatar",
    "sopimus",
    "resurssi",
    "laiva",
    "kaveri",
    "suklaa",
    "liitos",
    "muodollinen",
    "yläkerrassa",
    "auto",
    "lomakohde",
    "ulkomailla",
    "jälleenmyyjä",
    "liittolainen",
    "sormi",
    "leikkaus",
    "kommentti",
    "joukkue",
    "yksityiskohta",
    "hullu",
    "polku",
    "tarina",
    "ensimmäinen",
    "käsivarsi",
    "radio",
    "kysyntä",
    "sinkku",
    "piirtää",
    "keltainen",
    "kilpailu",
    "pala",
    "lainata",
    "Vedä",
    "kaupallinen",
    "paita",
    "panos",
    "kerma",
    "kanava",
    "puku",
    "kurinalaisuutta",
    "ohje",
    "konsertti",
    "puhetta",
    "matala",
    "tehokas",
    "ripustaa",
    "naarmuuntua",
    "teollisuus",
    "aamiainen",
    "antaa",
    "liittyä",
    "metalli",
    "makuuhuone",
    "minuutti",
    "tuote",
    "levätä",
    "lämpötila",
    "monet",
    "antaa",
    "argumentti",
    "painaa",
    "violetti",
    "nauraa",
    "terveys",
    "luotto",
    "investointi",
    "myydä",
    "asetusta",
    "oppitunti",
    "muna",
    "keskellä",
    "avioliitto",
    "taso",
    "todisteita",
    "lause",
    "rakkaus",
    "itse",
    "hyötyä",
    "opastusta",
    "vaikuttaa",
    "sinä",
    "isä",
    "ahdistusta",
    "erityistä",
    "poikaystävä",
    "testata",
    "tyhjä",
    "maksu",
    "keitto",
    "velvollisuus",
    "vastata",
    "hymy",
    "syvä",
    "valitus",
    "lisäys",
    "arvostelu",
    "laatikko",
    "pyyhe",
    "alaikäinen",
    "hauskaa",
    "maaperää",
    "antaa",
    "savuke",
    "netti",
    "saada",
    "kertoa",
    "sisääntulo",
    "varaa",
    "tapaus",
    "perhe",
    "kieltäytyä",
    "haara",
    "voi",
    "kynä",
    "isoisä",
    "vakio",
    "säiliö",
    "setä",
    "ilmasto",
    "maahan",
    "äänenvoimakkuutta",
    "viestintää",
    "kiltti",
    "runoilija",
    "lapsi",
    "näyttö",
    "minun",
    "lopettaa",
    "geeni",
    "puute",
    "hyväntekeväisyys",
    "muisti",
    "hammas",
    "pelko",
    "mainita",
    "markkinointi",
    "paljastaa",
    "syy",
    "tuomioistuin",
    "kausi",
    "vapautta",
    "maa",
    "urheilu",
    "yleisö",
    "luokkahuoneessa",
    "lakia",
    "koukku",
    "voittaa",
    "kantaa",
    "silmä",
    "haju",
    "jakelu",
    "tutkimusta",
    "maassa",
    "uskaltaa",
    "toivoa",
    "kun",
    "venyttää",
    "kirjasto",
    "jos",
    "viive",
    "college",
    "muovi",
    "kirja",
    "esittää",
    "käyttää",
    "huoli",
    "mestari",
    "tavoite",
    "taloutta",
    "maaliskuuta",
    "vaaleissa",
    "heijastus",
    "keskiyöllä",
    "liukumäki",
    "inflaatio",
    "toimintaa",
    "haaste",
    "kitara",
    "rannikolla",
    "omena",
    "kampanja",
    "ala",
    "takki",
    "järkeä",
    "tapa",
    "visuaalinen",
    "poistaa",
    "sää",
    "roskakoriin",
    "kaapeli",
    "katumusta",
    "kaveri",
    "ranta",
    "historioitsija",
    "rohkeutta",
    "myötätuntoa",
    "kuorma-auto",
    "jännitystä",
    "lupa",
    "nenä",
    "vuode",
    "poika",
    "henkilö",
    "pohja",
    "liha",
    "tavallista",
    "ilmaa",
    "kokous",
    "arvoinen",
    "peli",
    "itsenäisyys",
    "fyysistä",
    "lyhyt",
    "pelata",
    "nostaa",
    "hallitus",
    "hän",
    "avain",
    "kirjoittaminen",
    "valita",
    "komento",
    "juhliin",
    "eilen",
    "kevät",
    "ehdokas",
    "fysiikka",
    "yliopisto",
    "koskea",
    "kehitystä",
    "muuttaa",
    "merkkijono",
    "tavoite",
    "esimerkki",
    "huone",
    "katkera",
    "lintu",
    "jalkapallo",
    "normaali",
    "jakaa",
    "vaikutelma",
    "puu",
    "pitkä",
    "merkitys",
    "varastossa",
    "korkki",
    "johtajuutta",
    "media",
    "kunnianhimoa",
    "kalastus",
    "essee",
    "salaatti",
    "korjaus",
    "tänään",
    "suunnittelija",
    "yö",
    "pankki",
    "piirustus",
    "väistämätön",
    "vaihe",
    "laaja",
    "siru",
    "suututtaa",
    "kytkin",
    "itkeä",
    "kierre",
    "persoonallisuus",
    "yrittää",
    "varastointi",
    "oleminen",
    "valmistelu",
    "bat",
    "valinta",
    "valkoinen",
    "teknologiaa",
    "sopimus",
    "puolella",
    "osio",
    "asemalle",
    "asti",
    "rakenne",
    "kieli",
    "maku",
    "totuus",
    "vaikeus",
    "ryhmä",
    "rajoittaa",
    "pää",
    "liikkua",
    "tunne",
    "valoa",
    "esimerkki",
    "tehtävää",
    "saattaa",
    "odota",
    "pyörä",
    "kauppa",
    "isäntä",
    "klassinen",
    "vaihtoehto",
    "aiheuttaa",
    "agentti",
    "koostuvat",
    "taulukko",
    "lentoyhtiö",
    "teksti",
    "allas",
    "käsityö",
    "alue",
    "polttoainetta",
    "työkalu",
    "kumppani",
    "ladata",
    "sisäänkäynti",
    "tallettaa",
    "vihaa",
    "artikla",
    "video",
    "kesä",
    "ominaisuus",
    "äärimmäinen",
    "mobiili",
    "sairaala",
    "lento",
    "syksy",
    "eläkettä",
    "piano",
    "epäonnistua",
    "tulos",
    "hieroa",
    "aukko",
    "järjestelmä",
    "raportti",
    "imeä",
    "tavallinen",
    "tuuli",
    "hermo",
    "kysyä",
    "loistaa",
    "huomautus",
    "linja",
    "äiti",
    "käsitys",
    "veli",
    "viite",
    "mutka",
    "veloittaa",
    "hoitaa",
    "temppu",
    "termi",
    "kotitehtävät",
    "leipoa",
    "tarjous",
    "status",
    "hanke",
    "strategia",
    "oranssi",
    "anna",
    "innostusta",
    "vanhempi",
    "keskittyä",
    "laite",
    "matkustaa",
    "runous",
    "liiketoimintaa",
    "yhteiskuntaan",
    "suudella",
    "loppu",
    "kasvis",
    "käyttää",
    "ajoittaa",
    "tunnin",
    "rohkea",
    "keskittyä",
    "käsitellä",
    "elokuva",
    "laitonta",
    "yleistä",
    "kahvia",
    "ilmoitus",
    "valtatie",
    "kemia",
    "psykologia",
    "vuokraus",
    "kello",
    "konferenssi",
    "helpotus",
    "show",
    "siisti",
    "hauska",
    "paino",
    "laatu",
    "klubi",
    "tytär",
    "vyöhyke",
    "kosketa",
    "tänä iltana",
    "järkyttää",
    "polttaa",
    "tekosyy",
    "nimi",
    "kyselyyn",
    "maisema",
    "etukäteen",
    "tyytyväisyys",
    "leipää",
    "katastrofi",
    "kohde",
    "hattu",
    "ennen",
    "ostoksilla",
    "vierailla",
    "itään",
    "kuva",
    "kotiin",
    "idea",
    "isä",
    "vertailu",
    "kissa",
    "putki",
    "voittaja",
    "laskea",
    "järvi",
    "taistella",
    "palkinto",
    "perusta",
    "koira",
    "pitää",
    "ihanteellinen",
    "tuuletin",
    "kamppailua",
    "huippu",
    "turvallisuutta",
    "ratkaisu",
    "helvetti",
    "johtopäätös",
    "väestöstä",
    "rasitusta",
    "hälytys",
    "mittaus",
    "toinen",
    "kouluttaa",
    "rotu",
    "erääntyy",
    "vakuutus",
    "pomo",
    "puu",
    "seurata",
    "sairas",
    "tietenkin",
    "vetää",
    "nimittäminen",
    "viipale",
    "edelleen",
    "hoito",
    "kärsivällisyyttä",
    "rikas",
    "paeta",
    "tunne",
    "kuninkaallinen",
    "naaras",
    "lapsuus",
    "hallitus",
    "kuva",
    "tahtoa",
    "sukka",
    "iso",
    "portti",
    "öljy",
    "ylittää",
    "pin",
    "parantaminen",
    "mestaruus",
    "typerä",
    "auttaa",
    "taivas",
    "piki",
    "mies",
    "timantti",
    "useimmat",
    "siirtyminen",
    "työtä",
    "tiede",
    "komitea",
    "hetki",
    "korjata",
    "opetusta",
    "kaivaa",
    "asiantuntija",
    "monimutkainen",
    "opas",
    "ihmiset",
    "kuollut",
    "ääni",
    "alkuperäinen",
    "tauko",
    "aihe",
    "tiedot",
    "tutkinnon",
    "lukeminen",
    "tallennus",
    "nippu",
    "tavoittaa",
    "tuomio",
    "valehdella",
    "säännöllinen",
    "sarja",
    "maalaus",
    "tila",
    "lista",
    "pelaaja",
    "karhu",
    "pohjoinen",
    "ihme",
    "matto",
    "raskas",
    "upseeri",
    "negatiivinen",
    "kello",
    "ainutlaatuinen",
    "vauva",
    "kipu",
    "oletus",
    "levy",
    "rauta",
    "laskuttaa",
    "laatikko",
    "Katso",
    "kaksinkertainen",
    "virhe",
    "loppuun",
    "tulevaisuutta",
    "loistava",
    "ota yhteyttä",
    "matematiikka",
    "riisi",
    "lähteä",
    "ravintola",
    "alennus",
    "seksiä",
    "virus",
    "bitti",
    "luottaa",
    "tapahtuma",
    "käyttää",
    "mehu",
    "epäonnistuminen",
    "bugi",
    "yhteydessä",
    "muta",
    "koko",
    "kääri",
    "tarkoitus",
    "luonnos",
    "paine",
    "kakku",
    "tumma",
    "selitys",
    "tilaa",
    "kulma",
    "sana",
    "tehokkuutta",
    "hallinta",
    "tapa",
    "tähti",
    "mahdollisuus",
    "löytäminen",
    "kuljetus",
    "seisomaan",
    "kritiikkiä",
    "virtaus",
    "ovi",
    "vahinkoa",
    "hyönteinen",
    "yllätys",
    "huoneisto",
]  # pylint: disable=line-too-long

# ISO 639-1 codes to language names.
LANGUAGE_CODES = immutabledict.immutabledict(
    {
        "en": "English",
        "es": "Spanish",
        "pt": "Portuguese",
        "ar": "Arabic",
        "hi": "Hindi",
        "fr": "French",
        "ru": "Russian",
        "de": "German",
        "ja": "Japanese",
        "it": "Italian",
        "bn": "Bengali",
        "uk": "Ukrainian",
        "th": "Thai",
        "ur": "Urdu",
        "ta": "Tamil",
        "te": "Telugu",
        "bg": "Bulgarian",
        "ko": "Korean",
        "pl": "Polish",
        "he": "Hebrew",
        "fa": "Persian",
        "vi": "Vietnamese",
        "ne": "Nepali",
        "sw": "Swahili",
        "kn": "Kannada",
        "mr": "Marathi",
        "gu": "Gujarati",
        "pa": "Punjabi",
        "ml": "Malayalam",
        "fi": "Finnish",
    }
)

_ALPHABETS = "([A-Za-z])"
# _PREFIXES = "(Mr|St|Mrs|Ms|Dr)[.]"
_PREFIXES = "(Herra|St|Rouva|Neiti|Dr)[.]" 
_SUFFIXES = "(Inc|Ltd|Jr|Sr|Co|Oy)"
#_STARTERS = r"(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
_STARTERS = r"(Herra|Rouva|Neiti|Tohtori|Profi|Kapteeni|Kpt|Luttn|Hän\s|Se\s|He\s|Heidän\s|Meidän|Me\s|Mutta\s|Kuitenkin\s|Tämä\s|Missä tahansa)"
_ACRONYMS = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
_WEBSITES = "[.](com|net|org|io|gov|edu|me|fi|eu)"
_DIGITS = "([0-9])"
_MULTIPLE_DOTS = r"\.{2,}"


def split_into_sentences(text):
    """Split the text into sentences.

    Args:
      text: A string that consists of more than or equal to one sentences.

    Returns:
      A list of strings where each string is a sentence.
    """
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(_PREFIXES, "\\1<prd>", text)
    text = re.sub(_WEBSITES, "<prd>\\1", text)
    text = re.sub(_DIGITS + "[.]" + _DIGITS, "\\1<prd>\\2", text)
    text = re.sub(
        _MULTIPLE_DOTS,
        lambda match: "<prd>" * len(match.group(0)) + "<stop>",
        text,
    )
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub(r"\s" + _ALPHABETS + "[.] ", " \\1<prd> ", text)
    text = re.sub(_ACRONYMS + " " + _STARTERS, "\\1<stop> \\2", text)
    text = re.sub(
        _ALPHABETS + "[.]" + _ALPHABETS + "[.]" + _ALPHABETS + "[.]",
        "\\1<prd>\\2<prd>\\3<prd>",
        text,
    )
    text = re.sub(_ALPHABETS + "[.]" + _ALPHABETS + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + _SUFFIXES + "[.] " + _STARTERS, " \\1<stop> \\2", text)
    text = re.sub(" " + _SUFFIXES + "[.]", " \\1<prd>", text)
    text = re.sub(" " + _ALPHABETS + "[.]", " \\1<prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if '"' in text:
        text = text.replace('."', '".')
    if "!" in text:
        text = text.replace('!"', '"!')
    if "?" in text:
        text = text.replace('?"', '"?')
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]:
        sentences = sentences[:-1]
    return sentences


def count_words(text):
    """Counts the number of words."""
    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text)
    num_words = len(tokens)
    return num_words


@functools.lru_cache(maxsize=None)
def _get_sentence_tokenizer():
    return nltk.data.load("nltk:tokenizers/punkt/english.pickle")


def count_sentences(text):
    """Count the number of sentences."""
    tokenizer = _get_sentence_tokenizer()
    tokenized_sentences = tokenizer.tokenize(text)
    return len(tokenized_sentences)


def generate_keywords(num_keywords):
    """Randomly generates a few keywords."""
    return random.sample(WORD_LIST, k=num_keywords)
