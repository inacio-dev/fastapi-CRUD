import json
import re


def clean_invalid_chars(json_string):
    # Remove ou substitui caracteres de controle inválidos
    cleaned_string = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", json_string)
    re_cleaned_string = re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", cleaned_string)

    return re_cleaned_string


def get_json_response(response):
    # Tenta limpar o JSON e fazer o parse novamente
    cleaned_body = clean_invalid_chars(response.text)
    try:
        cleaned_json = json.loads(cleaned_body)
        # Novo passo: Limpar espaços em branco de strings em cada elemento do JSON
        # e substituir padrões específicos por uma string vazia
        if isinstance(cleaned_json, list):
            return [{k: process_value(v) for k, v in element.items()} for element in cleaned_json]
        elif isinstance(cleaned_json, dict):
            return {k: process_value(v) for k, v in cleaned_json.items()}
        return cleaned_json
    except json.JSONDecodeError as e:
        # Se ainda assim falhar, relança a exceção
        raise e from None


def process_value(value):
    if isinstance(value, str):
        # Remove espaços desnecessários e verifica se o valor é apenas '/' ou espaços
        cleaned_value = value.strip()
        if cleaned_value == "/" or all(c in " /" for c in cleaned_value):
            return ""
        return cleaned_value
    return value
