from logger import logger
from database.models import YudqsLogs
from .ariba import Ariba
from datetime import datetime, timedelta
from typing import List
import ast
from . import settings
from selenium.common.exceptions import StaleElementReferenceException

class AdditionalIntegration(Ariba):
    
    not_allowed_buyers_group = ('CC7',' CC2', 'CC3', 'CG2', 'CC5', 'CT6', 'CE1', 'CT2', 'CT3', 'CT7', 'CG5', 'CN4')
    
    @staticmethod
    def get_pending_integrations() -> List[YudqsLogs]:
        """Retrieve eligible sourcing projects for processing."""        
        
        # Set cutoff date once to avoid multiple calculations
        cutoff_date = datetime.now() - timedelta(days=15)
        
        # Get the SDC IDs of unprocessed quotations first
        unprocessed_quotation_ids = YudqsLogs.objects.filter(
            type='Quotation',
            processed__in=[0, None]
        ).values_list('sdc_id', flat=True)
        
        # Then retrieve the eligible sourcing projects
        records = YudqsLogs.objects.filter(
            type='Sourcing Project',
            process_information__isnull=False,
            log_datetime__gte=cutoff_date
        ).exclude(
            sdc_id__in=unprocessed_quotation_ids
        ).only(
            'process_information'
        )
        logger.debug(f'Found {records.count()} eligible sourcing projects')
        
        valid_records = []
        for record in records:
            try:
                process_information = ast.literal_eval(record.process_information.replace("''", '"'))
                if process_information['buyer_group'] in AdditionalIntegration.not_allowed_buyers_group:
                    logger.info(f"SDC {record.sdc_id} is within a buyer group that should not be integrated")
                    continue
                valid_records.append(record)
            except Exception as e:
                logger.error(f"Error processing SDC {record.sdc_id} - {e}")
                continue
        
        return valid_records

    def select_tab(self, tab_name: str):
        try:
            while not self.find_elements(
                f"//li[contains(@class,'w-tabitem-selected')]//a[contains(., '{tab_name}')]",
                wait=False
            ):
                self.click(f"//a[contains(text(), '{tab_name}')]")
        except StaleElementReferenceException:
            pass
        
    def is_approval_task_ready(self) -> bool:  
        try:
            dropdown_task_exists = self.find_element("//a[contains(@title, 'Tarefa de revisão/aprovação')]")
            dropdown_task = self.find_elements("//a[contains(@title, 'Tarefa de revisão/aprovação - Concluído Antecessor(es): Informar na Visão Geral do Projeto o Valor Negociado')]")
        except:
            open_phase = self.find_elements("//a[@role='treeitem']/div/div")[4].click()
            dropdown_task = self.find_elements("//a[contains(@title, 'Tarefa de revisão/aprovação - Concluído')]")
        if len(dropdown_task) > 0:
            return True
        else:
            return False
    

    def open_award_process(self):
        #award_label
        self.click('//*[@id="_rvvak"]')
        #open_button
        self.click('//*[@id="_d46lj"]')
        #open_RFP
        self.click('//*[@id="_hw6hvc"]')
        #open_button
        self.click('//*[@id="_dytdwd"]')

    def set_integration_sap(self, quotation):
        #task_tab
        self.click("//a[contains(text(), 'Situação')]")
        #select_manual_situation
        self.click("//td[contains(text(), '{}')]/preceding-sibling::td/preceding-sibling::td/preceding-sibling::td/preceding-sibling::td/preceding-sibling::td/span/div".format('Atribuído'))
        
        #actions_button
        self.click("//*[@id='_rjo0yb']")
        #send_quotations_to_external_system
        self.click("//a[contains(text(), 'Enviar cotações ao sistema externo')]")
        try:
            #ok_button
            self.click("//*[@id='_gtq2i']")
        except:
            if len(self.find_elements("//div[contains(text(), 'As cotações já foram enviadas ao sistema externo. Deseja enviá-las novamente?')]")) > 0 or len(self.find_elements("//div[contains(text(), 'As cotações já foram processadas pelo sistema externo. Deseja enviá-las novamente? Para obter informações adicionais, consulte o registro do evento ou o painel de mensagens.')]")) > 0:
                #cancel_button
                self.click("//*[@id='_znpni']")
                #logo
                self.click("//*[@title='Logotipo da empresa']")
                save_processed_item = YudqsLogs(quotation,'integration_sap', 'Integração SAP feita pelo comprador')
                #save_processed_item = YudqsLogs(sdc_dict['sdc'],'integration_sap', 'Integração SAP feita pelo comprador')
                #db.saveProcessedItem(sdc_dict['sdc'], 'integration_sap', 'Integração SAP feita pelo comprador') 
                save_processed_item.save()
                print('A RFP já foi integrada ao SAP')
                logger.warning('A RFP já foi integrada ao SAP')

    def get_quotation(self, quotation_id: str):
        
        found = self.search(
            category='Projeto de sourcing', 
            search_text=quotation_id
            )        
        if not found:
            return False
        
        self.click(f"//a[contains(@title, '{quotation_id}')]")
        
        # click in Tarefas tab until it is selected
        self.select_tab('Tarefas')
        is_ready = self.is_approval_task_ready()
        if not is_ready:
            logger.warning(f"SDC {quotation_id} is still open for approval")
            return False
        self.open_award_process()
        self.set_integration_sap(quotation_id)
        print('Integração - OK: {}'.format(quotation_id))
        #print('Integração - OK: {}'.format(sdc_dict['sdc']))
        #logger.info('Integração - OK: {}'.format(sdc_dict['sdc']))
        logger.info('Integração - OK: {}'.format(quotation_id))

        #sdc_dict = supplier_award.getContracts(sdc_dict)
        x = 1

        
      
    def start(self):        
        quotations = self.get_pending_integrations() 
        if not quotations:
            logger.info("No sourcing projects to process")
            return
        self.login(
            settings.USERNAME_ARIBA,
            settings.PASSWORD_ARIBA
        )
        for quotation in quotations:
            self.get_quotation(quotation.sdc_id)
