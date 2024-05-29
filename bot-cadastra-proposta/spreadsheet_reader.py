import pandas as pd
from initiative import Initiative


def read_csv_to_initiative_list(filename):
    df = pd.read_csv(filename)

    initiative_list = []

    for index, row in df.iterrows():
        initiative = Initiative(
            index=index,
            name=row["Nome da Iniciativa"],
            description=row["Descrição"],
            responsible_organization=row["Nome/Organização Resposável"],
            email=row["Email"],
            phone=row["Telefone Público"],
            address=row["Endereço"],
            city=row["Município"],
            state=row["Estado"],
            category=row["Categoria"],
            status=row["Status"],
        )
        initiative_list.append(initiative)

    return initiative_list


def add_text_to_initiative_attribute(filename, initiative_name, attribute, text):
    df = pd.read_csv(filename)

    if initiative_name in df["Nome da Iniciativa"].values:
        df.loc[df["Nome da Iniciativa"] == initiative_name, attribute] = text
        df.to_csv(filename, index=False)
        print(f"Updated {attribute} of initiative '{initiative_name}' with '{text}'.")
    else:
        print(f"Initiative '{initiative_name}' not found.")
