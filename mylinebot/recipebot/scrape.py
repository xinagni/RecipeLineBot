from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests
import re


class Food(ABC):

    def __init__(self, food):
        self.food = food
    
    @abstractmethod
    def scrape(self):
        pass

class Recipe(Food):

    def scrape(self):
        
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        executable_path = 'C:\chromedriver\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        driver.get("https://www.ytower.com.tw")

        response = requests.get("https://www.ytower.com.tw/recipe/")
        soup = BeautifulSoup(response.content, "html.parser")

        #處理使用者輸入資訊
        elements = driver.find_element(By.ID, "keyword")
        foodlist = self.food.split(" ")

        elements.send_keys(foodlist[0])
        for i in range(1,len(foodlist)):
            elements.send_keys(" and " + foodlist[i])

        #爬蟲搜索資訊
        elements.send_keys(Keys.ENTER)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        #爬出每一項食譜名稱
        name = ''
        content = []
        result = []

        
        for i in range(1, 6):
            info = ""
            steps = ""
            recipe_xpath_str = f"//body/div[@id='main']/div[@id='rightmain']/div[2]/div[4]/ul[1]/li[{i}]/a[1]/picture[1]/img[1]"
            item = driver.find_element(By.XPATH, recipe_xpath_str)
            driver.execute_script("arguments[0].click();", item)
            time.sleep(2)
                
            soup = BeautifulSoup(driver.page_source, "html.parser")

            #食譜名
            div = soup.find('div', {'id' : 'recipe_name'})
            h2 = div.find('h2')
            recipe_name = div.find('a').get_text()
            recipe_name = re.sub(r'\([^()]*\)', '', recipe_name)
            print(recipe_name)

            #所需食材、調味料
            div = soup.find('div', {'id' : 'recipe_item'})
            count = 0
            ingredient_count = 0
            
            if div:

                ul_elements = div.find_all('ul', {'class' : 'ingredient'})
                for ul in ul_elements:
                    
                    count += 1
                    ingredient_count += 1
                    if ingredient_count == 1:
                        info = info + "<食材>"
                        print("<食材>")
                    elif ingredient_count == 2:
                        info = info + "\n\n<調味料>"
                        print("<調味料>")
                    else:
                        info = info + "\n\n<醃料>"
                        print("<醃料>")

                    first_li = ul.find('li')

                    if first_li:

                        sibling_li_elements = first_li.find_next_siblings('li')

                        for li in sibling_li_elements:

                            if count != 3:

                                ingredient = li.find('span', {'class' : 'ingredient_name'})
                                ingredient_name = ingredient.find('a')
                                ingredient_amount = ingredient.find('span', {'class' : 'ingredient_amount'})

                                if ingredient_name and ingredient_amount and ingredient_name.text != '':
                                
                                    info = info + "\n" +(ingredient_name.text + '---' + ingredient_amount.text)
                                    print(ingredient_name.text + '---' + ingredient_amount.text)

                            else:

                                ingredient = li.find('span', {'class' : 'ingredient_name'})
                                ingredient_name = ingredient.find('a')
                                ingredient_amount = li.find('span', {'class' : 'ingredient_amount'})

                                if ingredient_name and ingredient_amount and ingredient_name.text != '':
                                    info = info + "\n" + (ingredient_name.text + '---' + ingredient_amount.text)
                                    print(ingredient_name.text+'---'+ingredient_amount.text)
                            
                            
            #步驟

            step_ul = soup.find('ul', attrs={'style': 'clear:both;'})
            step_li = step_ul.find_all('li')

            for step in step_li:
                steps = steps  + step.text.strip() + "\n----------\n"
                

            #圖片
            recipe_pic = soup.find('div', {'id' : 'recipe_mainpic'})
            recipe_pic_img = recipe_pic.find('img')
            src = recipe_pic_img.get('src')
            print(src)

            driver.back()
            time.sleep(2)

            #食譜名稱, 食材, 做法, 圖片
            content = [recipe_name, info, steps, src, info[:40]]
            result.append(content)

        time.sleep(5)
        driver.close()
        print("Successful")

        return result




