from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import getpass
import time
import getpass

parser = argparse.ArgumentParser(description='Location file names')
parser.add_argument('filenames', nargs='*')
args=parser.parse_args()

options = Options()
options.add_argument("no-sandbox")
options.add_argument('--no-proxy-server')
options.add_argument("start-maximized")
options.add_argument("window-size=1900,1080"); 
driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())

base='https://fusiontables.google.com/DataSource?dsrcid=implicit'

def getcreds():
	u=getpass.getpass(prompt='User: ', stream=None) 
	p=getpass.getpass(prompt='Pass ', stream=None)
	return [u,p]

def openpages(n,usps):
	for i in range(0,n):
		if i!=0:
			driver.execute_script("window.open('','_blank');")#open a blank window
			driver.switch_to.window(driver.window_handles[i])#switch to the new window
		driver.get(base)
		try:
			driver.find_element_by_id("yDmH0d")#look for the body of the login page
			WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,'yDmH0d')))#if its there wait until its fully loaded
		except:
			continue#if this fails im already logged in on that page
		#else send the creds
		driver.find_element_by_id("identifierId").send_keys(usps[0]+'\n')
		WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.NAME,'password')))
		driver.find_element_by_name("password").send_keys(usps[1]+'\n')

def finloadfiles():
	for page in driver.window_handles:
		driver.switch_to.window(page)
		WebDriverWait(driver,40).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[8]/div/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div')))
		but=driver.find_element_by_xpath('/html/body/div[8]/div/table/tbody/tr[2]/td/div/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[3]/div')
		driver.find_element_by_xpath('/html/body/div[8]/div/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div').click()#to get labels menu
		driver.find_element_by_id('gwt-uid-121').click()#to click none for labels
		but.click()#continue twice to notebook
		but.click()

def loadfiles():
	for page,fname in zip(driver.window_handles,args.filenames):
		driver.switch_to.window(page)
		WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.NAME,"uploadFormElement")))
		driver.find_element_by_name("uploadFormElement").send_keys(fname)#get ready for the upload
		but=driver.find_element_by_xpath('/html/body/div[8]/div/table/tbody/tr[2]/td/div/table/tbody/tr[4]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[3]/div')
		but.click()#start upload
	finloadfiles()#finish file uploads, having this here reduces some of the waiting time while working other tabs


def changetype():
	for page in driver.window_handles:
		driver.switch_to.window(page)
		WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[6]/div[2]/div/div[3]/div/div[3]/div/div[3]/div/div[4]/div/div[3]/div/div[2]/div/div[2]/div/div[3]/div/div[4]/div/div[4]/div/div[1]/div[3]/table/thead/tr/th[1]')))#waits for tbody cell to load
		ActionChains(driver).move_to_element(driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[3]/div/div[3]/div/div[3]/div/div[4]/div/div[3]/div/div[2]/div/div[2]/div/div[3]/div/div[4]/div/div[4]/div/div[1]/div[3]/table/thead/tr/th[1]')).perform()#hover over cell we want to get submenu for
		WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,'grid-header-menu-icon')))
		driver.find_element_by_class_name('grid-header-menu-icon').click()#click the little arrow
		driver.find_element_by_id('gwt-uid-418').click()#click change

		WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[6]/div[3]/div/div[3]/div/div[3]/div/div[4]/div/ul[4]/li[2]/div/div[1]')))#wait for type selection menu
		driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[3]/div/div[3]/div/div[4]/div/ul[4]/li[2]/div/div[1]').click()#click type selection menu
		driver.find_element_by_id('gwt-uid-503').click()#select 'location'
		driver.find_element_by_id('gwt-uid-500').click()#select two column location
		driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[3]/div/div[2]').click()#click save

def openmap():
	for page in driver.window_handles:
		driver.switch_to.window(page)
		driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[3]/div/div[2]/div/div[4]/div/div').click()#click '+' to begin adding map
		driver.find_element_by_id('gwt-uid-192').click()#click add map
		WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[6]/div[2]/div/div[3]/div/div[2]/div/div[4]/div/div/div/div/div')))
		driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[3]/div/div[2]/div/div[2]').click()
		WebDriverWait(driver,30).until(EC.invisibility_of_element_located((By.CLASS_NAME,'gux-confirm-panel-c')))#wait for 'loading' to dissapear
		driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[3]/div/div[2]/div/div[4]/div/div/div/div/div').click()

sttime=time.time()
openpages(len(args.filenames),getcreds())
loadfiles()
changetype()
openmap()
print('tot time= %s'%(time.time()-sttime))



