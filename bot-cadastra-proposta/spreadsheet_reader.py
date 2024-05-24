import pandas as pd
from initiative import Initiative


def read_csv_to_initiative_list(filename):
    df = pd.read_csv(filename)

    initiative_list = []

    for index, row in df.iterrows():
        initiative = Initiative(
            name=row["Nome da Iniciativa"],
            description=row["Descrição"],
            responsible_organization=row["Nome/Organização Resposável"],
            email=row["Email"],
            phone=row["Telefone Público"],
            address=row["Endereço"],
            city=row["Município"],
            state=row["Estado"],
            category=row["Categoria"],
        )
        initiative_list.append(initiative)

    return initiative_list
