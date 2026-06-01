def update_model(*, session, schema):
    for field, value in schema.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(session, field, value)
