from openapi_spec_validator import validate_spec

def validate_openapi(data):
    try:
        validate_spec(data)
    except Exception as e:
        raise Exception(f"OpenAPI validation failed: {str(e)}")
