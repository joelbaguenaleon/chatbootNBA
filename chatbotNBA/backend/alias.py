def obtener_alias_equipos():
    return {
        "los angeles lakers": "Los Angeles Lakers",
        "lakers": "Los Angeles Lakers",

        "boston celtics": "Boston Celtics",
        "celtics": "Boston Celtics",
        "boston": "Boston Celtics",

        "golden state warriors": "Golden State Warriors",
        "golden state": "Golden State Warriors",
        "warriors": "Golden State Warriors",

        "new york knicks": "New York Knicks",
        "knicks": "New York Knicks",
        "new york": "New York Knicks",

        "chicago bulls": "Chicago Bulls",
        "bulls": "Chicago Bulls",
        "chicago": "Chicago Bulls",

        "miami heat": "Miami Heat",
        "heat": "Miami Heat",
        "miami": "Miami Heat",

        "milwaukee bucks": "Milwaukee Bucks",
        "bucks": "Milwaukee Bucks",
        "milwaukee": "Milwaukee Bucks",

        "brooklyn nets": "Brooklyn Nets",
        "nets": "Brooklyn Nets",
        "brooklyn": "Brooklyn Nets",

        "phoenix suns": "Phoenix Suns",
        "suns": "Phoenix Suns",
        "phoenix": "Phoenix Suns",

        "san antonio spurs": "San Antonio Spurs",
        "spurs": "San Antonio Spurs",
        "san antonio": "San Antonio Spurs",

        "dallas mavericks": "Dallas Mavericks",
        "mavericks": "Dallas Mavericks",
        "mavs": "Dallas Mavericks",
        "dallas": "Dallas Mavericks",

        "la clippers": "LA Clippers",
        "clippers": "LA Clippers",

        "philadelphia 76ers": "Philadelphia 76ers",
        "sixers": "Philadelphia 76ers",
        "76ers": "Philadelphia 76ers",
        "philadelphia": "Philadelphia 76ers",

        "toronto raptors": "Toronto Raptors",
        "raptors": "Toronto Raptors",
        "toronto": "Toronto Raptors",

        "oklahoma city thunder": "Oklahoma City Thunder",
        "thunder": "Oklahoma City Thunder",
        "oklahoma": "Oklahoma City Thunder",
        "okc": "Oklahoma City Thunder",

        "memphis grizzlies": "Memphis Grizzlies",
        "grizzlies": "Memphis Grizzlies",
        "memphis": "Memphis Grizzlies",

        "new orleans pelicans": "New Orleans Pelicans",
        "pelicans": "New Orleans Pelicans",
        "new orleans": "New Orleans Pelicans",

        "orlando magic": "Orlando Magic",
        "magic": "Orlando Magic",
        "orlando": "Orlando Magic",

        "detroit pistons": "Detroit Pistons",
        "pistons": "Detroit Pistons",
        "detroit": "Detroit Pistons",

        "cleveland cavaliers": "Cleveland Cavaliers",
        "cavaliers": "Cleveland Cavaliers",
        "cavs": "Cleveland Cavaliers",
        "cleveland": "Cleveland Cavaliers",

        "indiana pacers": "Indiana Pacers",
        "pacers": "Indiana Pacers",
        "indiana": "Indiana Pacers",

        "atlanta hawks": "Atlanta Hawks",
        "hawks": "Atlanta Hawks",
        "atlanta": "Atlanta Hawks",

        "charlotte hornets": "Charlotte Hornets",
        "hornets": "Charlotte Hornets",
        "charlotte": "Charlotte Hornets",

        "minnesota timberwolves": "Minnesota Timberwolves",
        "timberwolves": "Minnesota Timberwolves",
        "wolves": "Minnesota Timberwolves",
        "minnesota": "Minnesota Timberwolves",

        "portland trail blazers": "Portland Trail Blazers",
        "trail blazers": "Portland Trail Blazers",
        "blazers": "Portland Trail Blazers",
        "portland": "Portland Trail Blazers",

        "utah jazz": "Utah Jazz",
        "jazz": "Utah Jazz",
        "utah": "Utah Jazz",

        "sacramento kings": "Sacramento Kings",
        "kings": "Sacramento Kings",
        "sacramento": "Sacramento Kings",

        "houston rockets": "Houston Rockets",
        "rockets": "Houston Rockets",
        "houston": "Houston Rockets",

        "denver nuggets": "Denver Nuggets",
        "nuggets": "Denver Nuggets",
        "denver": "Denver Nuggets",

        "washington wizards": "Washington Wizards",
        "wizards": "Washington Wizards",
        "washington": "Washington Wizards"
    }

def normalizar_abreviatura_equipo(nombre_equipo):
    mapa = {
        "Atlanta Hawks": "ATL",
        "Boston Celtics": "BOS",
        "Brooklyn Nets": "BKN",
        "Charlotte Hornets": "CHA",
        "Chicago Bulls": "CHI",
        "Cleveland Cavaliers": "CLE",
        "Dallas Mavericks": "DAL",
        "Denver Nuggets": "DEN",
        "Detroit Pistons": "DET",
        "Golden State Warriors": "GSW",
        "Houston Rockets": "HOU",
        "Indiana Pacers": "IND",
        "LA Clippers": "LAC",
        "Los Angeles Lakers": "LAL",
        "Memphis Grizzlies": "MEM",
        "Miami Heat": "MIA",
        "Milwaukee Bucks": "MIL",
        "Minnesota Timberwolves": "MIN",
        "New Orleans Pelicans": "NOP",
        "New York Knicks": "NYK",
        "Oklahoma City Thunder": "OKC",
        "Orlando Magic": "ORL",
        "Philadelphia 76ers": "PHI",
        "Phoenix Suns": "PHX",
        "Portland Trail Blazers": "POR",
        "Sacramento Kings": "SAC",
        "San Antonio Spurs": "SAS",
        "Toronto Raptors": "TOR",
        "Utah Jazz": "UTA",
        "Washington Wizards": "WAS"
    }

    return mapa.get(nombre_equipo)

def traducir_posicion(pos):
    posiciones = {
        "PG": "base",
        "SG": "escolta",
        "SF": "alero",
        "PF": "ala-pívot",
        "C": "pívot",
        "F": "alero/ala-pivot",
        "G": "base-escolta",
        "C-F": "ala-pivot/pívot",
        "F-C": "ala-pivot/pívot",
        "F-G": "alero",
        "G-F": "alero"
    }
    return posiciones.get(pos, pos)


def traducir_conferencia(conf):
    conferencias = {
        "East": "este",
        "West": "oeste"
    }
    return conferencias.get(conf, conf)


def traducir_division(division):
    divisiones = {
        "Atlantic": "atlántica",
        "Central": "central",
        "Southeast": "sudeste",
        "Northwest": "noroeste",
        "Pacific": "pacífico",
        "Southwest": "sudoeste"
    }
    return divisiones.get(division, division)
