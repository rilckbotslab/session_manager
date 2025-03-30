from logger import logger
from database.models import YudqsLogs
from .ariba import Ariba
from typing import List
import ast
from .settings import settings
from selenium.common.exceptions import StaleElementReferenceException

class SupplierAward(Ariba):
    
    def get_pending_awards(self) -> List[dict]:
        #SELECT process_information FROM yduqs_logs WHERE type = 'Quotation' AND status = 'success' AND (processed = 0 OR processed is NULL) order by id desc;
        records:List[str] =  YudqsLogs.objects.filter(
            type='Quotation',
            status='success',
            processed__in=[0, None]
        ).order_by('id').values_list('process_information', flat=True)
        
        logger.debug(f'Found {len(records)} pending awards')
        for record in records:
            try:
                as_dict = ast.literal_eval(record.replace("''", '"'))                
                yield as_dict
            except Exception as e:                
                continue        


    def get_sdc_additional_information(self, sdc_number:str) -> dict:
        # "SELECT process_information FROM yduqs_logs WHERE type = %s AND sdc_id = %s;",
        #             ("SDC", sdc_number)
        result:str = YudqsLogs.objects.filter(
            type='SDC',
            sdc_id=sdc_number
        ).values_list('process_information', flat=True).first()
        
        if not result:
            return 'Sem leitura de RC'
        result = result.replace("Timestamp('", "'").replace("')", "'")
        try:
            return ast.literal_eval(result)
        except (SyntaxError, ValueError) as e:
            return f'Erro ao interpretar o literal: {e}'


    def get_quotation(self, purchase_requisition_number):
        print('Processando Cotação {}'.format(purchase_requisition_number))
        try:
            self.find_element('//*[@class="a-srch-portlet-category-dropdown"]') 
            self.click("//[@id='_1qxz8d']")
        except:
            try:
                self.click('//*[@title="Logotipo da empresa"]')
                self.find_element('//[@class="a-srch-portlet-category-dropdown"]') 
                self.click("//*[@id='_1qxz8d']") 
            except:
                try:
                    self.click("//*[@id='_rjr7bd']")
                except:
                    pass

        try:
            self.send_text_and_press_enter("//*[@id='_2wupab']", purchase_requisition_number)
        except:
            self.driver.execute_script("window.history.go(-1)")
            self.click('//*[@title="Logotipo da empresa"]')
            print('Não existem fornecedores disponíveis com resposta à cotação')
            logger.warning('Não existem fornecedores disponíveis com resposta à cotação')
        #sourcing_project_title
        self.click("//a[contains(@title, '{}')]".format(purchase_requisition_number))
        try:
            #sourcing_project_title_open
            self.click("//*[@id='_ydjglb']")
        except:
            #open_phase
            self.click("//a[@role='treeitem']/div/div")
            #sourcing_project_title_open
            self.click("//*[@id='_ydjglb']")
        #open_button
        self.click("//*[@id='_fd8uxc']") 
        #task_tab
        self.click("//a[contains(text(), 'Tarefas')]")


    def finish_preparation_task(self):
        try:
            #dropdown_task
            self.click("//a[contains(text(), 'Preparação')]")
            #start_task
            self.click("//a[contains(text(), 'Marcar como iniciada')]")
        except:
            #task_tab
            self.click("//a[contains(text(), 'Tarefas')]")
        try:
            #open_phase
            open_phase = self.find_elements("//a[@role='treeitem']/div/div")[0]
            # Rolar para o elemento visível
            self.hover(open_phase)
            #self.actions.move_to_element(open_phase).perform()
            # Clicar no elemento

            open_phase.click()
            self.click("//a[contains(text(), 'Validar Membros da Equipe')]")
            if self.find_element("//a[contains(text(), 'Validar Membros da Equipe') and not(@title='Tarefa - Concluído')]"):
                self.click("//a[contains(text(), 'Validar Membros da Equipe')]")
                #finish_task
                self.click("//*[@id='_6sz$pd']")
                #dropdown_task
                self.click("//a[contains(text(), 'Preparação')]")
                #start_task
                self.click("//a[contains(text(), 'Marcar como concluída')]")
                #task_tab
                self.click("//a[contains(text(), 'Tarefas')]")
        except:
           pass


    def finish_quotation_task(self):
        try:
            #dropdown_task
            self.click("//a[contains(text(), 'Cotação')]")
            #start_task
            self.click("//a[contains(text(), 'Marcar como iniciada')]")
        except:
            #task_tab
            self.click("//a[contains(text(), 'Tarefas')]")
        try:
            open_phase = self.find_elements("//a[@role='treeitem']/div/div")[1]
            open_phase.click()
            
            dropdown_task = self.find_element("//a[contains(text(), 'Definir Regras da RFP - Estácio')]")
            if dropdown_task.get_attribute('title') != 'Tarefa - Concluído':
                self.click("//a[contains(text(), 'Definir Regras da RFP - Estácio')]")
                #finish_task
                self.click("//*[@id='_bw2xv']")
                #dropdown_task
                self.click("//a[contains(text(), 'Cotação')]")
                #start_task
                self.click("//a[contains(text(), 'Marcar como concluída')]")
                #task_tab
                self.driver.find_element("//a[contains(text(), 'Tarefas')]")
        except:
            pass
        

    def finish_review_task(self):
        try:
            #dropdown_task
            self.click("//a[contains(text(), 'Revisão')]")
            #start_task
            self.click('xpath', "//a[contains(text(), 'Marcar como iniciada')]")
        except:
            #task_tab
            self.click("//a[contains(text(), 'Tarefas')]")
        try:
            #open_phase = self.driver.find_elements('xpath', "//a[@role='treeitem']")[2].click()
            #time.sleep(3)
            dropdown_task = self.find_element("//a[contains(text(), 'Revisão')]")
            if dropdown_task.get_attribute('title') != 'Fase - Concluído':
                #dropdown_task
                self.click("//a[contains(text(), 'Revisão')]")
                #finish_task 
                self.click("//*[@id='_lbkmid']")
        except:
            #open_phase
            self.find_elements("//a[@role='treeitem']/div/div")[2].click()
            dropdown_task = self.find_element("//a[contains(text(), 'Revisão')]")
            if dropdown_task.get_attribute('title') != 'Fase - Concluído':
                #dropdown_task
                self.click("//a[contains(text(), 'Revisão')]")
                #finish_task
                self.click("//*[@id='_lbkmid']")
        #task_tab  
        self.click("//a[contains(text(), 'Tarefas')]")


    def finish_update_task(self):
        #task_tab
        self.click("//a[contains(text(), 'Tarefas')]")
        try:
            #dropdown_task
            self.click("//a[contains(text(), 'Atualização')]")
            #start_task
            self.click("//a[contains(text(), 'Marcar como iniciada')]")
        except:
            #task_tab
            self.click("//a[contains(text(), 'Tarefas')]")
            
        try:
            #open_phase
            self.find_elements("//a[@role='treeitem']/div/div")[3].click()
            dropdown_task = self.find_element("//a[contains(text(), 'Informar na Visão Geral do Projeto o Valor Negociado')]")
            if dropdown_task.get_attribute('title') != 'Tarefa - Concluído':
                #dropdown_task
                self.click("//a[contains(text(), 'Informar na Visão Geral do Projeto o Valor Negociado')]")
                #finish_task
                self.click("//*[@id='_yq4w6b']")
            
            alert_message = self.find_element("//div[contains(text(), 'Reiniciar essa tarefa reativará ou criará novas rodadas de todas as tarefas sucessoras')]")
            #cancel_button
            self.click("//*[@id='_ggy80']")
        except:
            #task_tab
            self.click("//a[contains(text(), 'Tarefas')]")
        #task_tab
        self.click('xpath', "//a[contains(text(), 'Tarefas')]")

           
    def start(self):
        logger.info('Starting Supplier Award process')
        self.login(
            settings.USERNAME,
            settings.PASSWORD
        )
        
        pending_awards = self.get_pending_awards()

        for award in pending_awards:            
            process_information = self.get_sdc_additional_information(award['sdc'])
            logger.info(f'Processing SDC: {award["sdc"]}')
            logger.info(f'Processing Quotation: {process_information["project_name"]}')
            self.search()

            self.get_quotation(award['sdc'])

            try:
                self.finish_preparation_task()
                self.finish_quotation_task()
                self.finish_review_task()
                self.finish_update_task()

            except:
                pass

        logger.info(f'Found {len(pending_awards)} pending awards')
        
