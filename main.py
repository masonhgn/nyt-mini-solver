from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get("https://www.nytimes.com/crosswords/game/mini")

wait = WebDriverWait(driver, 20)


###button needs to be clickable
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "xwd__modal--subtle-button")))


buttons = driver.find_elements(By.CLASS_NAME, "xwd__modal--subtle-button")
for button in buttons:
    if button.text == "Play without an account":
        button.click()
        break


check_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='check']")))
check_button.click()

#autocheck needs to be enabled
autocheck_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Autocheck')]")))
autocheck_button.click()

characters = list('abcdefghijklmnopqrstuvwxyz')

def click_cell_by_number(driver, cell_number):
    cell_id = f"cell-id-{cell_number}"
    wait = WebDriverWait(driver, 10)
    
    cell = wait.until(EC.element_to_be_clickable((By.ID, cell_id)))
    
    actions = ActionChains(driver)
    actions.move_to_element(cell).click().perform()
    for char in characters:
        
        actions.move_to_element(cell).click()
        
        actions.send_keys(char).perform()

        
        cell = wait.until(EC.presence_of_element_located((By.ID, cell_id)))
        cell_classes = cell.get_attribute("class")
        
        
        if "xwd__assistance--confirmed" in cell_classes or "xwd__cell--block" in cell_classes:
            print(f"correct guess '{char}' for cell {cell_number}")
            break #we guessed the right word


        if cell_number == 48:
            try:
                
                keep_trying_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'pz-moment__button')]")))
                keep_trying_button.click()
                print("Clicked 'Keep trying' button.")
            except:
                
                print("'Keep trying' button not found after last character input.")


def type_characters_rapidly(driver, start_cell_number, end_cell_number, characters):
    for cell_number in range(start_cell_number, end_cell_number + 1):
        cell_id = f"cell-id-{cell_number}"
        cell = driver.find_element(By.ID, cell_id)
        
        cell.click()
        if cell_number < 48: 
            for char in characters:
                cell.send_keys(char)
                cell.send_keys(Keys.BACKSPACE)

                cell_classes = cell.get_attribute("class")
                if "xwd__assistance--confirmed" in cell_classes or "xwd__cell--block" in cell_classes: break
        else:
            for char in characters:
                try:
                    WebDriverWait(driver, 0.1).until(EC.visibility_of_element_located((By.CLASS_NAME, "xwd__rats-modal")))
                    close_button = driver.find_element(By.XPATH, "//div[contains(@class,'xwd__modal--close')]")
                    close_button.click()
                    time.sleep(0.1)
                except:
                    
                    pass
                cell.send_keys(char)
                cell.send_keys(Keys.BACKSPACE)

try:
    type_characters_rapidly(driver, 1, 48, characters)
except:
    print('oops')


input('press enter to close...')
driver.quit()