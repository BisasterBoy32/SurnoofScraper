from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webScraper.settings import pusher_client
import json
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def check_if_bill_match(html_body ,bill):
    bill = '$' + bill 
    real_bill = html_body.find_all("md-select-value", {"id" : "select_value_label_1"})[0].span.text.strip()
    return bill == real_bill

def scrape_data_9(soup ,url ,bill):
        entry = {
            "url" : None,
            "UPFRONT COST AFTER INCENTIVES" :None ,
            "20-YEAR BENEFITS" : None,
            "TOTAL 20-YEAR SAVINGS" : None,
            "YEARS UNTIL PAYBACK" :None ,  
            "Up-front cost of installation" : None,
            "Total payments over 20 years": None,
            "State and Federal Incentives": None,
            "Solar Renewable Energy Credits (SRECs)" :None ,
            "Total 20-year cost with solar":None ,
            "Total 20-year cost without solar": None,
            "Total 20-year savings" : None,
            "Bill" : None,
            "Size (Kw)" : None,
            "Size (ft^2)": None
        }
        entry["url"] = url
        entry["Bill"] = bill 

        try:
            kw = soup.find_all("div", {"class" : "recommended-kw"})
            kw =  kw[0].text.strip()
            entry["Size (Kw)"] = kw
        except:
            pass

        try:
            ft = soup.find_all("div", {"class" : "recommended-area"})
            ft = ft[0].text.strip()
            entry["Size (ft^2)"] = ft 
        except:
            pass

        try:
            part1 = soup.findAll("div", {"class": "cost-tab-values"})
            part1[0].findAll("div", {"class": "cost-cell-value"})[0].text
            upfront_cost = part1[0].findAll("div", {"class": "cost-cell-value"})[0].text
            entry["UPFRONT COST AFTER INCENTIVES"] = upfront_cost.strip() 
        except:
            pass
        
        try:
            years_benefit = part1[0].findAll("div", {"class": "cost-cell-value"})[1].text
            entry["20-YEAR BENEFITS"] =  years_benefit.strip()
        except:
            pass

        try:
            years_saving = part1[0].findAll("div", {"class": "cost-cell-value"})[2].text
            entry["Total 20-year savings"] = years_saving.strip()
        except:
            pass

        try:
            years_untill_payback = part1[0].findAll("div", {"class": "cost-cell-value"})[3].text
            entry["YEARS UNTIL PAYBACK"] = years_untill_payback.strip()
        except:
            pass 

        try:
            part2 = soup.findAll("div", {"class": "show-more-content"})[0].find_all("tr")
            for tr in part2:
                # if this is not a divider
                if not tr.find("td", {"class": "details-divider"}):
                    heading = tr.find("div" , { "class" : "details-heading"}).text.strip()
                    value = tr.find("td" , { "class" : "details-number"}).text.strip()
                    if heading == "Up-front cost of installation":
                        entry["Up-front cost of installation"] = value
                    elif heading == "Total payments over 20 years":
                        entry["Total payments over 20 years"] = value
                    elif heading == "State and Federal Incentives":
                        entry["State and Federal Incentives"] = value
                    elif heading == "Solar Renewable Energy Credits (SRECs)":
                        entry["Solar Renewable Energy Credits (SRECs)"] = value
                    elif heading == "Total 20-year cost with solar":
                        entry["Total 20-year cost with solar"] = value
                    elif heading == "Total 20-year cost without solar":
                        entry["Total 20-year cost without solar"] = value
                    elif heading == "Total 20-year savings":
                        entry["Total 20-year savings"] = value
        except:
            pass

        return entry
        print("this site has been scraped succefully : ", url)

# def get_data(lat, lon, bill, d_type):
#     try:
#         f = d_type
#         url = f"https://www.google.com/get/sunroof/building/{lat}/{lon}/#?f={f}&b={bill}"
#         driver.get(url)
#         # r = session.get(url)
#         time.sleep(5)
#         htmlSource = driver.page_source
#         # htmlSource = r.html.render()
#         soup = BeautifulSoup(htmlSource, 'html.parser')
#         size = soup.findAll("div", {"class": "show-more-content"})[0].find_all("tr")

#         if len(size) and check_if_bill_match(soup, bill):
#             return scrape_data_9(soup, url ,bill)

#     except Exception as e:
#         print(e)
#         print("This URL doesn't conain any data2 : ",url )
#         return False

def scrape_data(url, bill, d_type):
    # binary = FirefoxBinary('/app/vendor/firefox/firefox')
    # driver = webdriver.Firefox(firefox_binary=binary)
    # driver = webdriver.Firefox()
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    # execution_path=CHROMEDRIVER_PATH,chrome_options=chrome_options
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        # r = session.get(url)
        time.sleep(10)
        htmlSource = driver.page_source
        # htmlSource = r.html.render()
        # htmlSource = requests.get(url)
        # htmlSource = htmlSource.text if htmlSource.status_code == 200 else None
        soup = BeautifulSoup(htmlSource, 'html.parser')
        size = soup.findAll("div", {"class": "show-more-content"})[0].find_all("tr")

        if len(size) and check_if_bill_match(soup, bill):
            result = scrape_data_9(soup, url ,bill)
            print("successssssssss : yessssssssssssssssssssssssssssssssss")
            print("successssssssss : yessssssssssssssssssssssssssssssssss")
            print("successssssssss : yessssssssssssssssssssssssssssssssss")
            print("successssssssss : yessssssssssssssssssssssssssssssssss")
            print("successssssssss : yessssssssssssssssssssssssssssssssss")
            print("successssssssss : yessssssssssssssssssssssssssssssssss")
            print(result)
            # push data to the frontend
            # message = json.dump(result)
            mes = { 
                "type" : "success",
                "message" : "This URL "+ url + " has been scrapped succefully",
                "data" : result
            }
            mes = json.dumps(mes)
            pusher_client.trigger('webScraper', 'url-scraped', {'message': mes})
            driver.close()
            return result

    except Exception as e:
        print(e)
        print("This URL doesn't conain any data : ",url )
        mes = { 
            "type" : "danger",
            "message" : "This URL doesn't conain any data : "+url
        }
        mes = json.dumps(mes)
        pusher_client.trigger('webScraper', 'url-scraped', {'message': mes})
        driver.close()
        return False

