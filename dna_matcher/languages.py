"""Module for handling multiple languages."""

import locale

message_map = {
    "en_GB": {
        "load_sample": "No \"DNA\" sample selected",
        "match": "Fill all the sample's boxes",
        "matchit": "The samples have {}% of chance to being from the guy.",
        "load": "Select your sample",
        "loaded": "Ready and loaded",
        "match_ready": "You are all free now"

    },
    "pt_BR": {
        "load_sample": "Nenhuma amostra selecionada.",
        "match": "Preencha todas as caixas",
        "matchit": "Há {}% de chance desses DNAs serem do alvo.",
        "load": "Selecione a sua amostra",
        "loaded": "Carregada",
        "match_ready": "Tudo pronto para a análise"
    } 
}


def get_message(code: str) -> str:
    """Returns a message within a map according to the current system
    locale.
    
    Args:
        code: Key to the message.
    
    Returns:
        The requested message translated to the user.
    """

    global message_map

    cur_locale = locale.getlocale()[0]

    return message_map[cur_locale][code]
 