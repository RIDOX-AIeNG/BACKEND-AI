class Pet:
    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species

    def display_info(self):
        print(f"Name: {self.name} \nSpecies: {self.species} \nAge:{self.age}")

    def celebrate_birthday(self):
        print(f"Happy birthday: {self.name}")

EkpoDavid = Pet('Ekpo',150,'Rat')
EkpoDavid.display_info()
EkpoDavid.celebrate_birthday()

