import urllib.request
from selenium import webdriver

figure_number = 0
url_principal = 'https://patentscope.wipo.int'


def guarda_imagen( image ):
    global figure_number
    # download the image
    src = image.get_attribute('src')
    print("obteniendo imagen de: "+src)
    urllib.request.urlretrieve(src, f"figure_{figure_number}.png")
    figure_number+=1


driver = webdriver.Chrome()
driver.get(f'{url_principal}/search/en/detail.jsf?docId=US212445360&tab=DRAWINGS')

#//*[@id="detailMainForm:j_idt5099_list"]
container = driver.find_element_by_css_selector("div[id*='detailMainForm:j_idt']")
#container = driver.find_element_by_css_selector('#detailMainForm\\:j_idt3869_list')

images = container.find_elements_by_tag_name( 'img' )

[ guarda_imagen( element ) for element in images ]

driver.close()