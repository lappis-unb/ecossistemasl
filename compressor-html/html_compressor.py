import re

arquivo_entrada = 'index.html'
arquivo_saida = 'newindex.html'

with open(arquivo_entrada, 'r') as arquivo:
    conteudo = arquivo.read()

novo_conteudo = re.sub(r'(?<!https:)\/\/.*\n', '', conteudo)

novo_conteudo = novo_conteudo.replace('\n', '')

with open(arquivo_saida, 'w') as arquivo:
    arquivo.write(novo_conteudo)

print(novo_conteudo)
