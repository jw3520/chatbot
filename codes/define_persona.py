from enum import Enum, auto

class Persona_Movie(Enum):
    NewWorld = auto()
    InsideMen = auto()
    WarOnCrime = auto()

class Movie_Info:
    @staticmethod
    def GetMovieTitle( movie):
        match movie:
            case Persona_Movie.NewWorld:
                title_string = 'new_world'
            case Persona_Movie.InsideMen:
                title_string = 'inside_men'
            case Persona_Movie.WarOnCrime:
                title_string = 'war_on_crime'
            case default :
                title_string = 'None'
        return title_string
    
    @staticmethod
    def GetMovieCharacter( movie):
        match movie:
            case Persona_Movie.NewWorld:
                character = 'jungcheong'
            case Persona_Movie.InsideMen:
                character = 'sangku'
            case Persona_Movie.WarOnCrime:
                character = 'ikhyun'
            case default :
                character = 'None'
        return character
    
    @staticmethod
    def GetMovieCharacterKorean( movie):
        match movie:
            case Persona_Movie.NewWorld:
                character_kor = '정청'
            case Persona_Movie.InsideMen:
                character_kor = '안상구'
            case Persona_Movie.WarOnCrime:
                character_kor = '익현'
            case default :
                character_kor = 'None'
        return character_kor
