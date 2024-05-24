class Initiative:
    def __init__(
        self,
        name,
        description,
        responsible_organization,
        email,
        phone,
        address,
        city,
        state,
        category,
    ):
        self.name = name
        self.description = description
        self.responsible_organization = responsible_organization
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.category = category

    def __repr__(self):
        return f"Initiative({self.name}, {self.description}, {self.responsible_organization}, {self.email}, {self.phone}, {self.address}, {self.city}, {self.state}, {self.category})"
