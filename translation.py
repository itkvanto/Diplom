import requests

# Функция получения перевода слова через Yandex API
def get_word_translation(word):
    IAM_TOKEN = ''
    folder_id = ''
    target_language = 'ru'

    body = {
        "targetLanguageCode": target_language,
        "texts": word,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )

    data = response.json()

    if response.status_code == 200:
        translation = data['translations'][0]['text']
        return translation
    else:
        return None


# Функция получения примера использования слова через dictionaryapi
def get_word_example(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    examples=[]
    response = requests.get(url)
    try:
        data = response.json()
        meanings = data[0].get('meanings')
        if response.status_code == 200:
            for k in range(len(meanings)):
                for l in range(len(meanings[k]['definitions'])):
                    try:
                        examples.append(meanings[k]['definitions'][l]['example'])
                    except:
                        pass
            return(examples[0])
        else:
            return None
    except:
        return None


