# HTML Compressor

Este é um script simples em Python para compactar código HTML, removendo quebras de linha e comentários em uma única linha. Isso pode ser útil ao lidar com problemas de formatação ao colar código HTML em componentes como o `Page` do Decidim.

## Como Funciona

O script utiliza a biblioteca `re` para remover comentários de estilo `//` e, em seguida, remove todas as quebras de linha, compactando o código HTML em uma única linha. O código resultante é salvo em um novo arquivo.

## Requisitos

- Python 3.x

## Uso

1. Clone este repositório ou faça o download da pasta `compressor-html`.

2. Cole o codigo html que deseja comprimir dentro do arquivo `index.html`.

3. Execute o script `html_compressor.py` da seguinte maneira:

```bash
python html_compressor.py
```

4. O código HTML compactado será salvo no arquivo de saída `newindex.html` e na saida padrao do terminal.

## Exemplo

Suponhamos que você tenha um arquivo `index.html` com o seguinte conteúdo:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Exemplo</title>
</head>
<body>
    <h1>Olá, mundo!</h1>
    <p>Este é um parágrafo.</p>
</body>
</html>
```

Ao usar o script e fornecer `index.html` como arquivo de entrada, o resultado será um arquivo `newindex.html` com o seguinte conteúdo:

```html
<!DOCTYPE html><html><head><title>Exemplo</title></head><body><h1>Olá, mundo!</h1><p>Este é um parágrafo.</p></body></html>

```

O código HTML foi compactado em uma única linha.

