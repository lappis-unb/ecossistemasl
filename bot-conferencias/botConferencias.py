import time
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://brasilparticipativo.presidencia.gov.br/users/sign_in")

df = pd.read_csv('Consolidado Conferências - Estaduais.csv')
df = df.values

df2 = pd.read_csv("Consolidado Conferências - Livres.csv")
df2 = df2.values

botaoInscrever = driver.find_element(By.CSS_SELECTOR, ".button--social")
botaoInscrever.click()

input("Aguarde até resolver o captcha manualmente e pressione Enter para continuar...")

botaoOpcoes = driver.find_element(By.CSS_SELECTOR, ".br-sign-in")
botaoOpcoes.click()

time.sleep(1)

botaoAdm = driver.find_elements(By.CSS_SELECTOR, ".br-item")
botaoAdm = botaoAdm[6]
botaoAdm.click()

botaoAssembleia = driver.find_element(By.CSS_SELECTOR, ".icon--dial")
botaoAssembleia.click()

botaoConse = driver.find_element(By.XPATH, '//a[@href="/admin/assemblies/cnsan6/edit"]')
botaoConse.click()

botaoAgenda = driver.find_element(By.XPATH, '//a[@href="/admin/assemblies/cnsan6/components/22/manage/"]')
botaoAgenda.click()

botaoNovaReuniao = driver.find_element(By.CSS_SELECTOR, ".button--simple")
botaoNovaReuniao.click()

def novaConferenciaEstadual(estado, diaInicio, diaFinal):
    campos = driver.find_elements(By.CSS_SELECTOR, ".js-hashtags")
    titulo = campos[0]
    titulo.send_keys("Conferência Estadual de Segurança Alimentar e Nutricional de " + estado)

    descricao = driver.find_element(By.CSS_SELECTOR, ".ql-editor")
    descricao.send_keys("As Conferências Estaduais e do Distrito Federal têm como objetivos, sem prejuízo de atender objetivos específicos:\n" +
        "    - Analisar a conjuntura estadual e nacional em relação à SAN;\n" +
        "Debater e elaborar propostas baseadas no lema, nos objetivos e nos eixos da 6ª Conferência Nacional visando ao 3º Plano Nacional de Segurança Alimentar e Nutricional;\n" +
        "Estimular a realização de Conferências Municipais, Regionais e Territoriais;\n" +
        "Eleger os(as) delegados(as) para a etapa nacional.\n\n" +
        "É fundamental que tanto o poder executivo como legislativo dos estados e do Distrito Federal estejam comprometidos com o processo de realização das Conferências Estaduais e Distrital, garantindo apoio logístico e recursos orçamentários.\n" +
        "A Conferência Estadual de SAN poderá ser convocada por meio de Resolução do Consea Estadual ou por ato específico do Poder Executivo Estadual. Os estados deverão informar ao Consea Nacional, por meio do e-mail 6conferenciasan@presidencia.gov.br, o calendário de realização das respectivas Conferências Estaduais, do Distrito Federal, Municipais e/ou Regionais ou Territoriais, tão logo o calendário estadual esteja definido.\n" +
        "O prazo final para a realização das Conferências Estaduais e do Distrito Federal é 30 de outubro de 2023.")

    tipoReuniao = driver.find_element(By.CSS_SELECTOR, "#meeting_type_of_meeting")
    tipoReuniao.click()
    time.sleep(0.5)
    presencial = driver.find_element(By.XPATH, '//option[@value="online"]')
    presencial.click()
    time.sleep(0.5)
    endereco = driver.find_element(By.CSS_SELECTOR, "#meeting_online_meeting_url")
    endereco.send_keys("https://aconfirmar.com.br")
    time.sleep(0.5)
    # local = driver.find_element(By.CSS_SELECTOR, "#meeting_location_pt__BR")
    # local.send_keys(estado)
    # time.sleep(0.5)
    inicio = driver.find_element(By.CSS_SELECTOR, "#meeting_start_time")
    inicio.click()
    inicio.send_keys(diaInicio + "/2023 08:00")
    inicio.send_keys(Keys.ENTER)
    time.sleep(0.5)
    final = driver.find_element(By.CSS_SELECTOR, "#meeting_end_time")
    final.click()
    final.send_keys(diaFinal + "/2023 18:00")
    final.send_keys(Keys.ENTER)
    time.sleep(0.5)
    tipoRegistro = driver.find_element(By.CSS_SELECTOR, "#meeting_registration_type")
    tipoRegistro.click()
    time.sleep(0.5)
    desativado = driver.find_element(By.XPATH, '//option[@value="registration_disabled"]')
    desativado.click()

    divCriar = driver.find_element(By.CSS_SELECTOR, ".button--double")

    criar = divCriar.find_element(By.CSS_SELECTOR, ".button")
    criar.click()

    return

def novaconferenciaLivre(nome, data, complemento):
    campos = driver.find_elements(By.CSS_SELECTOR, ".js-hashtags")
    titulo = campos[0]
    titulo.send_keys(nome)

    descricao = driver.find_element(By.CSS_SELECTOR, ".ql-editor")
    descricao.send_keys("As Conferências livres nacionais possuem caráter deliberativo, conforme previsto no Regulamento da 6ª CNSAN. Foram definidas como uma estratégia para ampliar a participação social nos debates e formulação de propostas e para a eleição de delegados(as) da sociedade civil. As Conferências livres não competem com, e nem substituem, a realização das Conferências das etapas Municipal, Estadual/Distrito Federal e Nacional ou mesmo com os Encontros Temáticos.\n" +
        "Trata-se de atividades autogestionadas que podem ocorrer na medida da viabilidade e do interesse dos segmentos sociais interessados, visando facilitar o processo de organização de diferentes grupos da sociedade civil organizada e a análise dos diferentes temas relacionados à agenda da 6ª CNSAN.\n" + 
        "Para que estas atividades façam parte do processo preparatório oficial da Conferência Nacional e contribuam com os seus resultados, devem cumprir etapas e critérios apontados em regulamento próprio. Estas atividades poderão eleger delegados(as) para a Etapa Nacional. Estas atividades serão autogestionadas e custeadas por seus proponentes, não cabendo ao Consea Nacional nenhum tipo de responsabilidade por sua organização e financiamento." +  
        "Mais informações sobre esta conferência: " + complemento)

    tipoReuniao = driver.find_element(By.CSS_SELECTOR, "#meeting_type_of_meeting")
    tipoReuniao.click()
    time.sleep(0.5)
    presencial = driver.find_element(By.XPATH, '//option[@value="online"]')
    presencial.click()
    time.sleep(0.5)
    endereco = driver.find_element(By.CSS_SELECTOR, "#meeting_online_meeting_url")
    endereco.send_keys("https://aconfirmar.com.br")
    time.sleep(0.5)
    # local = driver.find_element(By.CSS_SELECTOR, "#meeting_location_pt__BR")
    # local.send_keys(estado)
    # time.sleep(0.5)
    inicio = driver.find_element(By.CSS_SELECTOR, "#meeting_start_time")
    inicio.click()
    inicio.send_keys(data + " 08:00")
    inicio.send_keys(Keys.ENTER)
    time.sleep(0.5)
    final = driver.find_element(By.CSS_SELECTOR, "#meeting_end_time")
    final.click()
    final.send_keys(data + " 18:00")
    final.send_keys(Keys.ENTER)
    time.sleep(0.5)
    tipoRegistro = driver.find_element(By.CSS_SELECTOR, "#meeting_registration_type")
    tipoRegistro.click()
    time.sleep(0.5)
    desativado = driver.find_element(By.XPATH, '//option[@value="registration_disabled"]')
    desativado.click()

    divCriar = driver.find_element(By.CSS_SELECTOR, ".button--double")

    criar = divCriar.find_element(By.CSS_SELECTOR, ".button")
    criar.click()

    return

for i in range (27):
    time.sleep(1)
    novaConferenciaEstadual(df[i][0], str(df[i][2]), str(df[i][3]))
    time.sleep(4)
    botaoNovaReuniao = driver.find_element(By.CSS_SELECTOR, ".button--simple")
    botaoNovaReuniao.click()

for x in range(23):
    time.sleep(1)
    if(pd.isna(df2[x][2])):
        novaconferenciaLivre(df2[x][0], str(df2[x][1]), "A confirmar")
    else:
        novaconferenciaLivre(df2[x][0], str(df2[x][1]), df2[x][2])
    time.sleep(4)
    botaoNovaReuniao = driver.find_element(By.CSS_SELECTOR, ".button--simple")
    botaoNovaReuniao.click()

driver.close()


