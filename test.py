from selenium import webdriver                    
from selenium.webdriver.common.keys import Keys   
import time                                       
URL = 'https://www.electroplanet.ma/p1854449-hp-cz112ae.html'      
browser = webdriver.Safari()       

browser.get('https://www.electroplanet.ma/p1854449-hp-cz112ae.html')      

search = browser.find_elements_by_id('subjectInput')[1]    
search.send_keys('cz109ae')                        
search.send_keys(Keys.ENTER)     
time.sleep(5)                                            


browser.quit()