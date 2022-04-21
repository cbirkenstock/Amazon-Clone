from werkzeug.security import generate_password_hash
import csv
from faker import Faker
from wonderwords import RandomWord



num_users = 100
num_sellers = 50
num_products = 200
num_purchases = 100
num_product_reviews = 40
num_seller_reviews = 40
num_cart_entries = 70
num_saved = 100

Faker.seed(0)
fake = Faker()
r = RandomWord()



def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name = profile['name']
            balance = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            image = fake.random_element(elements=(
                "tiger",
                "monkey",
                "frog",
                "elephant",
                "gorilla"))
            writer.writerow([uid, email, password, name, balance, image])
        print(f'{num_users} generated')
    return



def gen_sellers(num_sellers):
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for uid in range(num_sellers):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            address = fake.address()
            writer.writerow([uid, address])
        print(f'{num_sellers} generated')
    return

def get_product(category):
    ad = r.word(include_parts_of_speech=["adjectives"])
    adj = ad[0].upper() + ad[1:]
    product = [" Candle", "https://images.urbndata.com/is/image/Anthropologie/58037110_001_b10?$a15-pdp-detail-shot$&fit=constrain&qlt=80&wid=640"]

    if(category == "Furniture"):
        product = fake.random_element(elements=([' Couch', "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.amazon.com%2FVelvet-Century-Living-Modern-Pillows%2Fdp%2FB08LNFZFVC&psig=AOvVaw1l1xXhUiRAro0vT3QgV_mf&ust=1638986338094000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCJDr84Wi0vQCFQAAAAAdAAAAABAE"],
         [' Chair', "https://theinside.imgix.net/products/IxIhjrCc8AL4QBNQE6vRyCRjzKxoc5Krdn3pXXck.jpeg?auto=compress%2Cformat&ixlib=react-9.0.3"], 
         [' Bed', "https://b3h2.scene7.com/is/image/BedBathandBeyond/86569456731_imageset?$690$&wid=690&hei=690"], 
         [" Nightstand", "https://stylecaster.com/wp-content/uploads/2018/09/animal-decor-10.jpeg?w=400&h=600"],
        [" Desk", "https://images.urbndata.com/is/image/Anthropologie/60438686_010_b"],
        [" Coffee Table", "https://images.urbndata.com/is/image/Anthropologie/60439320_001_b?$a15-pdp-detail-shot$&fit=constrain&qlt=80&wid=640"],
        [" Lamp", "https://i.pinimg.com/originals/2d/83/98/2d8398d7fb16848b776ceae9065be2bb.jpg"]
        ))
    elif(category == "Clothing"):
        product = fake.random_element(elements=(
            [' Dress', "https://i.pinimg.com/originals/5a/87/e5/5a87e5a4db14a4cd0c89797d84d21007.jpg"],
         [' Skirt', "https://media.vogue.co.uk/photos/5d5d01439a39110008ed1d2f/master/w_1920,h_1280,c_limit/Leopard%2021.87.19%207.jpg"], 
         [' Suit', "https://cdn.shopify.com/s/files/1/0234/5963/products/16A6665-615-Edit_42d506f1-ddb8-4e97-a4bc-c740d96e770a_large.jpg?v=1638445431"], 
         [" Pants", "https://media.missguided.com/i/missguided/RCO9346927_02?$product-page__main--2x$"],
        [" Jeans", "https://img.ltwebstatic.com/images3_pi/2020/11/30/16067350169ffafe2f5f0ae446f77d546abdcea44a_thumbnail_600x.webp"],
        [" Shirt", "https://img.ltwebstatic.com/images2_pi/2018/05/25/1527234348541259296.webp"],
        [" Costume", "https://images.halloweencostumes.com/products/32205/1-1/child-deluxe-lion-costume-update.jpg"]
        ))
    elif(category == "Sports"):
        product = fake.random_element(elements=(
            [' Football', "https://www.si.com/.image/ar_4:3%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTc0NDU1OTQyMjAzNjQ3NjIy/college-football-covid-symptoms-cases-players.jpg"],
         [' Basketball', "https://m.media-amazon.com/images/I/91vdgs5FY4L._AC_SL1500_.jpg"], 
         [' Volleyball', "https://m.media-amazon.com/images/I/61lj9PFLqaL._AC_SL1500_.jpg"], 
         [" Softball", "https://cdn.vox-cdn.com/thumbor/uW3cZFPag8gDwzFcoeQw-UpKJ_A=/0x0:1050x700/1200x800/filters:focal(441x266:609x434)/cdn.vox-cdn.com/uploads/chorus_image/image/69272529/10215943_web1_thinkstockphotos_softball_509935540.0.jpg"],
        [" Soccer Ball", "https://m.media-amazon.com/images/I/61Jigwd1kKL._AC_SX425_.jpg"],
        [" Frisbee", "https://i5.walmartimages.com/asr/11848b8b-1b25-450a-bea8-6e4caa0fec67_1.4e38c701da096e2c570efa6cc0a58d8a.jpeg?odnHeight=612&odnWidth=612&odnBg=FFFFFF"],
        [" Golf Clubs", "https://m.media-amazon.com/images/I/81phSCzbHWL._AC_SX425_.jpg"]
        ))
    
    final_product = adj + product[0]
    return [final_product, product[1]]

def gen_products(num_products, num_sellers):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 10 == 0:
                print(f'{pid}', end=' ', flush=True)
            seller_id = f'{str(fake.random_int(max=num_sellers-1))}'
            category = fake.random_element(elements=('Furniture', 'Clothing', 'Sports'))
            product = get_product(category)
            name = product[0]
            quantity = f'{str(fake.random_int(max=100))}'
            description = fake.sentence(nb_words=10)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            image = product[1]
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, seller_id, name, quantity, category, description, price, available, image])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids



def gen_purchases(num_purchases, num_users):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        num_ordered_items=0
        for id in range(num_purchases):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            total_amount = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            num_items = f'{str(fake.random_int(min=1, max=10))}'
            num_ordered_items += int(num_items)
            time_purchased = fake.date_time()
            address = fake.address()
            fulfillment_status = fake.random_element(elements=('true', 'false'))
            writer.writerow([id, uid, total_amount, num_items, time_purchased, address, fulfillment_status])
        print(f'{num_purchases} generated')
    return num_ordered_items



def gen_product_reviews(num_product_reviews, num_users, num_products):
    with open('ProductReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Reviews...', end=' ', flush=True)
        for id in range(num_product_reviews):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_int(min=0, max=num_products-1)
            time_purchased = fake.date_time()
            rating = f'{str(fake.random_int(min=1, max=5))}'
            description = fake.sentence(nb_words=10)[:-1]
            writer.writerow([uid, pid, time_purchased, rating, description])
        print(f'{num_product_reviews} generated')
    return


def gen_seller_reviews(num_seller_reviews, num_users, num_sellers):
    with open('SellerReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Reviews...', end=' ', flush=True)
        for id in range(num_product_reviews):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            sid = fake.random_int(min=0, max=num_sellers-1)
            time_purchased = fake.date_time()
            rating = f'{str(fake.random_int(min=1, max=5))}'
            description = fake.sentence(nb_words=10)[:-1]
            writer.writerow([uid, sid, time_purchased, rating, description])
        print(f'{num_seller_reviews} generated')
    return


def gen_cart_entries(num_cart_entries, num_users, available_pids):
    with open('CartEntries.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart Entries...', end=' ', flush=True)
        for id in range(num_cart_entries):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            num_items = f'{str(fake.random_int(min=1, max=10))}'
            writer.writerow([uid, pid, num_items])
        print(f'{num_cart_entries} generated')
    return


def gen_ordered_items(num_ordered_items, num_purchases, num_products):
    with open('OrderedItems.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Ordered Items...', end=' ', flush=True)
        for id in range(num_ordered_items):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            oid = f'{str(fake.random_int(max=num_purchases-1))}'
            pid = f'{str(fake.random_int(max=num_products-1))}'
            fulfillment_status = fake.random_element(elements=('true', 'false'))
            
            quantity = f'{str(fake.random_int(max=100))}'
            
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            
            writer.writerow([oid, pid, fulfillment_status, quantity, price])
        print(f'{num_ordered_items} generated')
    return 



def gen_saved(num_saved, num_users, num_products):
    with open('SavedForLater.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Saved For Later...', end=' ', flush=True)
        for id in range(num_saved):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = f'{str(fake.random_int(max=num_products-1))}'
            writer.writerow([uid, pid])
        print(f'{num_sellers} generated')
    return

gen_users(num_users)
gen_sellers(num_sellers)
available_pids = gen_products(num_products, num_sellers)
num_ordered_items = gen_purchases(num_purchases, num_users)
gen_product_reviews(num_product_reviews, num_users, num_products)
gen_seller_reviews(num_seller_reviews, num_users, num_sellers)
gen_cart_entries(num_cart_entries, num_users, available_pids)
gen_ordered_items(num_ordered_items, num_purchases, num_products)
gen_saved(num_saved, num_users, num_products)





