from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class CrawlerTJCE:

    def acessar_site(numero_processo):
      #Ocultando o Chrome 
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-notifications')    

        url = f'https://esaj.tjce.jus.br/cpopg/show.do?processo.codigo=01Z081I9T0000&processo.foro=1&processo.numero={numero_processo}'
               
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.get(url)
   
     # Expandir mais detalhes:
        mais_detalhes = driver.find_element(By.CLASS_NAME, 'unj-link-collapse')
        mais_detalhes.click()

        return driver

    def coletar_dados_do_processo(driver):
        try:
            def find_element_text(element_id):
                try:
                    element = driver.find_element_by_id(element_id)
                    return element.text
                except NoSuchElementException:
                    return ""

            classe = find_element_text('classeProcesso')
            area = find_element_text('areaProcesso')
            assunto = find_element_text('assuntoProcesso')
            data_distribuicao = find_element_text('dataHoraDistribuicaoProcesso')
            partes_do_processo = find_element_text('tablePartesPrincipais')
            movimentacoes = find_element_text('tabelaUltimasMovimentacoes')

            dados_do_processo = {
                'Classe': classe,
                'Área': area,
                'Assunto': assunto,
                'Data de Distribuição': data_distribuicao,
                'Partes do Processo': partes_do_processo,
                'Movimentações': movimentacoes
            }
            
        except NoSuchElementException:
            dados_do_processo = {
                'Classe': "",
                'Área': "",
                'Assunto': "",
                'Data de Distribuição': "",
                'Partes do Processo': "",
                'Movimentações': ""
            }
        finally:
            driver.quit()
            return dados_do_processo

    def acessar_site_segundo_grau(numero_processo):
            numero_proc_ano = numero_processo[:15]
            
            #Ocultando o Chrome
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-notifications')

            url2grau = f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={numero_proc_ano}&foroNumeroUnificado=0001&dePesquisaNuUnificado={numero_processo}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO'
            
            driver2 = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            driver2.get(url2grau)

            selecionar_processo = driver2.find_element_by_id('processoSelecionado')
            selecionar_processo.click()
            botao_selecionar =  driver2.find_element_by_id('botaoEnviarIncidente')
            botao_selecionar.click()
            mais_detalhes = driver2.find_element_by_css_selector('a[href="#maisDetalhes"]')
            mais_detalhes.click()
            
            return driver2

    def coletar_dados_segundo_grau(driver2):
            try:
                def find_element_text(element_id):
                    try:
                        element = driver2.find_element_by_id(element_id)
                        return element.text
                    except NoSuchElementException:
                        return ""

                secao = find_element_text('secaoProcesso')
                orgao_julgador = find_element_text('orgaoJulgadorProcesso')
                classe = find_element_text('classeProcesso')
                assunto = find_element_text('assuntoProcesso')
                area = find_element_text('areaProcesso')
                partes_do_processo = find_element_text('tablePartesPrincipais')
                movimentacoes = find_element_text('tabelaUltimasMovimentacoes')
     
                dados_do_processo2 = {
                    'Órgão Julgador': orgao_julgador,
                    'Seção': secao,
                    'Classe' : classe,
                    'Assunto': assunto,
                    'Área': area,
                    'Partes do Processo': partes_do_processo,
                    'Movimentações': movimentacoes
                }

            except NoSuchElementException:
                dados_do_processo2 = {
                    'Órgão Julgador': "",
                    'Seção': "",
                    'Vara': "",
                    'Classe': "",
                    'Assunto': "",
                    'Área': "",
                    'Movimentações': "",
                    'Partes do Processo': "",
                }

            return dados_do_processo2
