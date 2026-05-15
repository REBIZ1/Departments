class DataMapper:
    db_model = None
    schema = None

    @classmethod
    def map_to_domain_entity(cls, data):
        """
        Преобразует ORM объект с данными в Pydantic схему
        """
        return cls.schema.model_validate(data, from_attributes=True)
