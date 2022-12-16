# %%
import mysql.connector
import pandas as pd
from send_sms import send_sms_epic_to
import pandas as pd
token_dict = pd.read_json('D:/BYUI/fall 2020/Side Projects/token_dict.json')
config = {"user":'root', 
            "password":'Yoho1mes',
            "host":'127.0.0.1',
            "database":"cars"}
path = "D:/BYUI/fall 2020/Side Projects/porterbmoody.github.io/Facebook Marketplace Project/data/cars.csv"
dat1 = pd.read_csv(path)
dat1 = dat1.where(pd.notnull(dat1), None)
columns_titles = ['title', 'year', 'miles', 'price', 'link', 'location']
dat = dat1.reindex(columns=columns_titles)

# %%
def main():
    mydb = mysql.connector.connect(**config, auth_plugin='mysql_native_password')
    mycursor2 = mydb.cursor()
    mycursor1 = mydb.cursor()
    mycursor = mydb.cursor()

    cols = "`,`".join([str(i) for i in dat.columns.tolist()])
    print(cols)
    

    ### query epic data 
    query = "SELECT * FROM cars WHERE year >= 2008 AND miles <= 150000 AND price <= 4500;"
    mycursor1.execute(query)
    data = []
    for row in mycursor:
        data.append(row)
    dat_epic_before = pd.DataFrame(data, columns = ['id','title','year','miles','price','link','location'])

    ##### insert new data
    for i, row in dat.iterrows():
        insert_statement = "INSERT INTO `cars` (`id`,`" + cols + "`) VALUES (DEFAULT," + "%s," * (len(row)-1) + "%s)"
        mycursor.execute(insert_statement, tuple(row))
        mydb.commit()

    ################################ deleting duplicate rows sql
    # title, year, miles, price, link, location
    mysql_commands =    ["USE cars;",
                        "CREATE TEMPORARY TABLE unique_cars (`id` INT NOT NULL AUTO_INCREMENT, `title` VARCHAR(100) NULL, `year` FLOAT(20) NULL, `miles` FLOAT NULL, `price` FLOAT(20) NULL, `link` VARCHAR(100) NULL, `location` VARCHAR(60) NULL, PRIMARY KEY (`id`), UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);",
                        "INSERT INTO unique_cars SELECT MIN(id),title,year, miles,price,link,location FROM cars GROUP BY title,year, miles,	price,link,location;",
                        "TRUNCATE cars;",
                        "INSERT INTO cars SELECT id, title, year, miles, price, link, location FROM unique_cars;",
                        "DROP TABLE unique_cars;"]
    print('excecuting MYSQL')
    for command in mysql_commands:
        # print(command)
        mycursor.execute(command)
        mydb.commit()
    
    ### query epic data 
    query = "SELECT * FROM cars WHERE year >= 2008 AND miles <= 150000 AND price <= 4500;"
    mycursor2.execute(query)
    data = []
    for row in mycursor:
        data.append(row)
    mydb.close()
    dat_epic_after = pd.DataFrame(data, columns = ['id','title','year','miles','price','link','location'])

    print("Length before: ", len(dat_epic_before), "Length after: ", len(dat_epic_after))
    if len(dat_epic_after) > len(dat_epic_before):
        print(dat_epic_before)
        print()
        print(dat_epic_after)

        dat_deals = dat_epic_after.merge(dat_epic_before, on='id', how='left').query('price_y.isna()')
        print(dat_deals)
        ### testing
        recipients = ["+17193385009", "+17192002926"]

        titles = list(dat_deals['title_x'])
        miles  = list(dat_deals['miles_x'])
        prices  = list(dat_deals['price_x'])
        links  = list(dat_deals['link_x'])
        body   = "\n\n" + str(len(dat_deals.index)) + " New epic deal(s) ------pogs------\n"
        for title, mile, price, link in zip(titles, miles, prices, links):
            # body += "\n\n\nTitle:   " + title + "Link: " + link + "\n\n\n"
            body += "\nTitle:   " + title + "   Price: $" + str(price) + "   Link:   " + link + "\n\n"
        for recipient in recipients:
            send_sms_epic_to(recipient, body, account_sid = token_dict['account_sid'][0], auth_token = token_dict['auth_token'][0])
        print(body)

#%%

if __name__ == "__main__":
    main()
# %%
