def model_to_dict(model) -> dict:
    ''' Convert sqlalchemy model to dict '''
    return {k: v for k, v in model.__dict__.items() if not k.startswith('_')}