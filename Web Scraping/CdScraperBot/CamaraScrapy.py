# PARTE 1 - Web Scraping com Selenium atraves de uma classe
# Importando as libs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

dir_path = os.getcwd()
chrome_options = Options()
chrome_options.add_argument('--headless')

class GastosParlamentaresBot:

    def __init__(self):
        self.bot = webdriver.Chrome(dir_path + '\\chromedriver.exe', chrome_options = chrome_options)
        print('>>>>> GASTOS DOS DEPUTADOS FEDERAIS EM 2019 <<<<<\n\n')

    def buscaDep(self): # fazendo a pesquisa do dep no portal
        bot = self.bot
        bot.get('https://www2.camara.leg.br/deputados/pesquisa')
        time.sleep(3) # delay de 3 segundos para terminar o carregamento da página
        nomedep = bot.find_element_by_xpath('//*[@id="formDepAtual"]/div[1]/div/span/input')
        clique = bot.find_element_by_xpath('//*[@id="Pesquisa"]')
        nomedep.send_keys(input('Digite o nome do parlamentar: '))
        clique.click()
        
    def exibirInformacoes(self): # printando os dados obtidos
        print(f'\n\nGASTOS DO PARLAMENTAR {self.nome} EM 2019:')
        print(f'Auxílio-moradia: {self.moradia}')
        print(f'Verba de Gabinete: {self.verbagabinete}')
        print(f'Cota Parlamentar: {self.cotaparlamentar}\n\n')

    def capturarDados(self): # obtendo os dados
        bot = self.bot
        self.nome = bot.find_element_by_xpath('//*[@id="nomedeputado"]').text
        self.moradia = bot.find_element_by_xpath('//*[@id="recursos-section"]/div/ul/li[3]/div/span/a').text
        self.verbagabinete = bot.find_element_by_xpath('//*[@id="percentualgastoverbagabinete-chart"]/div[1]/div/div[3]/div/div/div/span[2]').text                
        self.cotaparlamentar = bot.find_element_by_xpath('//*[@id="percentualgastocotaparlamentar-chart"]/div[1]/div/div[3]/div/div/div/span[2]').text


# PARTE 2 - Web Scraping com Request e BeautifulSoup atraves de uma função
# Importando as libs
import requests
from bs4 import BeautifulSoup as soup

def cctci():
    html = requests.get('https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/cctci')
    html_bs = soup(html.text)
    cctci = html_bs.find('table') # acessando a tabela com as próximas reuniões

    print('>>> PRÓXIMAS REUNIÕES DA COMISSÃO DE CIÊNCIA DE TECNOLOGIA <<<\n\n')

    for i in cctci.tbody.find_all('tr'): # printando cada item da tabela
      print('Data:',i.div.text.strip())
      print('Horário:', i.div.find_next('div').text.strip())
      print('Comissão:', i.td.find_next('td').div.find_next('div').text.strip())
      print('Tipo:', i.td.find_next('td').div.find_next('div').find_next('div').text.strip())
      print('Assunto:', i.td.find_next('td').div.div.find_next('div').find_next('div').text.replace('Participe', '').strip())
      print('Local: Câmara dos Deputados,', i.td.find_next('td').div.div.find_next('div').find_next('div').find_next('div').text.replace('Participe', '').strip())
      print('Situação:', i.td.find_next('td').find_next('td').text.strip())
      print('Link:',i.td.find_next('td').div.div.a.get('href'))
      print('')
      # As tags sem ID dificultaram o acesso a elas
      # Por isso a navegação com os métodos find


# PARTE 3 - Criação de um menu simples
def menu():
    print('##### CÂMARA DOS DEPUTADOS SCRAPER #####\n\n')
    print('- Menu -\n')
    escolha = input('Digite uma opção: \n1- Gastos Parlamentares\n2- Reuniões CCTCI\n')

    if escolha == '1':
        bot = GastosParlamentaresBot() # instanciado a classe
        bot.buscaDep()
        time.sleep(3) # delay de 3 segundos para carregamento completo da página
        bot.capturarDados()
        bot.exibirInformacoes()
            
    elif escolha == '2':
        cctci()

    else:
        print('Opção inválida')

# PARTE 4 - Execução da aplicação
menu()