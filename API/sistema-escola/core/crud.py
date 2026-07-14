def update_model(*, obj, schema):
    for field, value in schema.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(obj, field, value)
