from .username import Username

class GroupName(Username):
    @classmethod
    def __modify_schema__(cls, field_schema):
        super().__modify_schema__(field_schema)
        field_schema.update(
            example='Алкашня'
        )
