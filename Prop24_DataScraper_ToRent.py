import pandas as pd
import requests
from bs4 import BeautifulSoup

def ToRent_dataScraper(Area_list):
    for Area in Area_list:
        URL = f"https://www.property24.com/to-rent/{Area[0]}/cape-town/western-cape/{Area[1]}"
        req = requests.get(URL)

        soup = BeautifulSoup(req.content, 'html.parser')

        rental_list = []

        promo_info = []
        for promo_rentals in soup.findAll('div', class_='p24_content'):
            promo_info.append("Page 1")
            for description in promo_rentals.findAll('div', class_='p24_description'):
                promo_info.append(description.text.strip().split(" in ")[0])
                promo_info.append(description.text.strip().split(" in ")[1])

            for address in promo_rentals.findAll('span', class_='p24_address'):
                promo_info.append(str(address.text.strip()))

            for size in promo_rentals.findAll('span', class_='p24_size'):
                promo_info.append(float((size.text.strip()[:-2].replace(" ", ""))))

            for price in promo_rentals.findAll('div', class_='p24_price'):
                if "POA" in price.text:
                    promo_info.append("")
                    promo_info.append(price.text.strip()[:3] + ", Promoted")

                elif "per" in price.text:
                    promo_info.append(int(price.text.strip().split("\n")[0][2:]))
                    promo_info.append(price.text.strip().split("\n")[1].strip() + ", Promoted")

                else:
                    promo_info.append(int(price.text.strip()[2:].replace(" ", "")))
                    promo_info.append("" + ", Promoted")

            rental_list.append(promo_info)

        pageNum = []
        for pgNo in soup.findAll('ul', class_='pagination'):
            for num in pgNo.findAll('li'):
                pageNum.append(num.text.strip())

        numPgs = int(pageNum[-1])

        for page in range(1, numPgs + 1):
            # print(f"Page {page}")
            URL = f"https://www.property24.com/to-rent/{Area[0]}/cape-town/western-cape/{Area[1]}/p{str(page)}"

            req = requests.get(URL)

            soup = BeautifulSoup(req.content, 'html.parser')

            for rentals in soup.findAll('span', class_='p24_content'):
                rental_info = []
                rental_info.append(f"Page {page}")
                for title in rentals.findAll('span', class_="p24_title"):
                    len_rent = len(rental_info)
                    if len_rent == 1:
                        rental_info.append(title.text.strip())
                    else:
                        rental_info.append("")
                        rental_info.append(title.text.strip())

                for location in rentals.findAll('span', class_="p24_location"):
                    len_rent = len(rental_info)
                    if len_rent == 2:
                        rental_info.append(location.text.strip())
                    else:
                        rental_info.append("")
                        rental_info.append(location.text.strip())

                for address in rentals.findAll('span', class_="p24_address"):
                    len_rent = len(rental_info)
                    print(len_rent)
                    if len_rent == 3:
                        rental_info.append(str(address.text.strip()))
                    else:
                        rental_info.append("")
                        rental_info.append(str(address.text.strip()))

                for size in rentals.findAll('span', class_="p24_size"):
                    len_rent = len(rental_info)
                    if len_rent == 4:
                        rental_info.append(float((size.text.strip()[:-2].replace(" ", ""))))
                    else:
                        rental_info.append("")
                        rental_info.append(int((size.text.strip()[:-2].replace(" ", ""))))

                for price in rentals.findAll('span', class_="p24_price"):
                    len_rent = len(rental_info)
                    if len_rent == 5:
                        if "POA" in price.text:
                            rental_info.append("")
                            rental_info.append(price.text.strip()[:3])

                        elif "per" in price.text:
                            rental_info.append(int(price.text.strip().split("\n")[0][2:].replace(" ", "")))
                            rental_info.append(price.text.strip().split("\n")[1].strip())

                        else:
                            rental_info.append(int(price.text.strip()[2:].replace(" ", "")))
                            rental_info.append("")
                    else:
                        rental_info.append("")
                        if "POA" in price.text:
                            rental_info.append("")
                            rental_info.append(price.text.strip()[:3])

                        elif "per" in price.text:
                            rental_info.append(int(price.text.strip().split("\n")[0][2:]))
                            rental_info.append(price.text.strip().split("\n")[1].strip())

                        else:
                            rental_info.append(int(price.text.strip()[2:].replace(" ", "")))
                            rental_info.append("")


                    print(len(rental_info), rental_info)
                rental_list.append(rental_info)


        df = pd.DataFrame(rental_list, columns=["Page No.", "Description", "Location", "Address", "Size (m²)", "Price", "Notes"])
        # print(df)

        df.to_csv(f"ToRent_DS_{Area_list[0][0]}.csv", index=False)




# Area_list = [["rondebosch-east", "8806"]]
# Area_list = [["crawford", "8787"]]
Area_list = [["athlone", "8734"]]
# Area_list = [["belgravia", "8736"]]
ToRent_dataScraper(Area_list)