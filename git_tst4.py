from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver  # for chrome open library for scraping
import time  # time library for sleep
from selenium.webdriver.chrome.service import Service
import pandas as pd



t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print("Last Active Time : ", current_time)



opt = webdriver.ChromeOptions()
opt.add_argument('--incognito')
opt.add_argument('--start-maximized')
opt.add_argument('--disable-application-cache')
opt.add_argument('--aggressive-cache-discard')

s = Service("C:/Program Files (x86)/chromedriver103.exe")
driver = webdriver.Chrome(service=s, options=opt)
print(driver.title)

driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})

skipInitial = 0
skipEnd = 194

rowCount = 6

# for keeping track of product serial
productSerial = skipEnd

# since it will be put on range so ++
skipEnd += 1

# putting a value of 0 will mean we are erasing header
if skipInitial == 0:
    skipInitial += 1

# product list csv
data = pd.read_csv("darazProductListOptimizedEmergency.csv", skiprows=range(skipInitial, skipEnd), nrows=rowCount)

# Make a list containing the values in column username
category = list(data['Category'])
sub_category = list(data['Sub Category'])
link = list(data['Link'])

print(skipEnd)

# Print one value per line:
for l,c,s in zip(link, category, sub_category):
    print(l)
    print(c)
    print(s)

    productSerial += 1
    print(productSerial)

    productLink = l
    driver.get("https://" + productLink)

    if driver.find_elements(By.CLASS_NAME, "comm-error"):
        time.sleep(5)
        continue
    category = c
    subcategory = s

    try:

        # keep page count
        pageNo = 0

        # create CSV for Saving Data of mobile phones with sentiment polarity
        data = open('emergencyFrom101to200.csv', 'a', encoding="utf-8")

        # writing header for the FILE
        data.write("User Name,Category,Sub Category,Product Name,Comment,Comment Date,Rating,Positive Feedback\n")


        # PRODUCT NAME
        productName = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='module_product_title_1']/div/div"))
        )
        productNameClean = str(productName.text).replace('\n', ' ')
        productNameClean = productNameClean.replace('\t', ' ')  # same as above defined
        productNameClean = productNameClean.replace('\n\n', ' ')  # same as above defined
        productNameClean = productNameClean.replace(',', ' ')  # same as above defined
        productNameClean = productNameClean.replace('\r', ' ')  # same as above defined
        productNameClean = productNameClean.strip()  # same as above defined

        print(productName.text + '\n')

        time.sleep(1)
        driver.find_element(By.XPATH, "//html").click()

        time.sleep(1)


        # Scroll down 1500px
        driver.execute_script("window.scrollTo(0, 2500)")


        print('paisi pagination')
        # zoom in out
        driver.execute_script("document.body.style.zoom='100%'")

        pageNext = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='module_product_review']/div/div/div[3]/div[2]/div/button[2]"))
        )
        hasNextPage = pageNext.get_property("disabled")

        # TAKES A RANGE OF NUMBER - PAGE NUMBER AND GETS THE INFO WE NEED
        while hasNextPage == False:

            driver.execute_script("document.body.style.zoom='50%'")
            time.sleep(.5)

            # Scroll down 1500px
            driver.execute_script("window.scrollTo(0, 2500)")


            driver.execute_script("document.body.style.zoom='100%'")
            time.sleep(.5)

            hasNextPage = pageNext.get_property("disabled")
            print(hasNextPage)

            time.sleep(2)

            # Scroll down 1500px
            driver.execute_script("window.scrollTo(0, 2500)")


            elementScroll = driver.find_element(By.XPATH, "//*[@id='module_product_review']/div/div/div[3]/div[1]")
            elementScroll.location_once_scrolled_into_view

            pageNo+=1


            for j in range(5):
                print(j + 1)

                wait = WebDriverWait(driver, 10)

                time.sleep(2)

                user = wait.until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "//*[@id='module_product_review']/div/div/div[3]/div[1]/div[" + str(
                                                            j + 1) + "]/div[2]/span[1]"))
                )
                print(user.text)

                time.sleep(1)
                review = wait.until(EC.presence_of_element_located(
                        (By.XPATH,
                         "//*[@id='module_product_review']/div/div/div[3]/div[1]/div[" + str(
                             j + 1) + "]/div[3]/div[1]")))
                print(review.text)
                reviewClean = str(review.text).replace('\n', ' ')
                reviewClean = reviewClean.replace('\t', ' ')  # same as above defined
                reviewClean = reviewClean.replace('\n\n', ' ')  # same as above defined
                reviewClean = reviewClean.replace(',', ' ')  # same as above defined
                reviewClean = reviewClean.replace('\r', ' ')  # same as above defined
                reviewClean = reviewClean.strip()  # same as above defined


                time.sleep(1)
                dateOfReview = wait.until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "//*[@id='module_product_review']/div/div/div[3]/div[1]/div[" + str(
                                                            j + 1) + "]/div[1]/span"))
                )
                print(dateOfReview.text)


                time.sleep(1)
                ratingCount = 0
                for k in range(5):
                    rating4 = wait.until(
                        EC.presence_of_element_located((By.XPATH,
                                                            "//*[@id='module_product_review']/div/div/div[3]/div[1]/div[" + str(
                                                                    j + 1) + "]/div[1]/div/img[" + str(
                                                                k + 1) + "]"))
                    )
                    rating3 = rating4.get_attribute("src")

                    if (rating3 == "https://laz-img-cdn.alicdn.com/tfs/TB19ZvEgfDH8KJjy1XcXXcpdXXa-64-64.png"or
                            rating3 == "//laz-img-cdn.alicdn.com/tfs/TB19ZvEgfDH8KJjy1XcXXcpdXXa-64-64.png"):
                        ratingCount += 1


                print("product rating : " + str(ratingCount))

                time.sleep(2)


                feedbackRating = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='module_product_review']/div/div/div[3]/div[1]/div[" + str(
                                    j + 1) + "]/div[3]/div[3]/span[1]/span/span"))
                )

                print(feedbackRating.text)

                data.write(
                        str(user.text) + "," + category + "," + subcategory + "," + str(productNameClean) + "," + str(
                            reviewClean) + "," + str(dateOfReview.text) + "," + str(ratingCount) + "," + str(
                            feedbackRating.text))  # writing in the CSV
                data.write('\n')  # writing in the CSV end line
                time.sleep(2)

                pageNext = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='module_product_review']/div/div/div[3]/div[2]/div/button[2]"))
                )

            continue





    except Exception as e:
        print(e)
        driver.quit()

driver.quit()
