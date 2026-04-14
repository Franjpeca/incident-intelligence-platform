import pytest

from app.core.exceptions import InvalidModelOutputError
from app.core.output_parser import extract_json

# Test para comprobar la correcta extracion de un JSON
def test_extract_json_returns_dict_when_json_is_valid():
    # Texto a comprobar
    text = 'Texto previo {"summary":"ok","category":"software","priority":"high","confidence":90} texto posterior'

    # Llamamos al componente
    result = extract_json(text)

    # Comprobamos que los valores de los campos son los esperados
    assert isinstance(result, dict)
    assert result["summary"] == "ok"
    assert result["category"] == "software"
    assert result["priority"] == "high"