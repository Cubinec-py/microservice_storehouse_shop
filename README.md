# Microservice info:
## STORAGE on Django REST framework
- Adding a description of the book and book items (summed up and transferred to the store as an available quantity) with the place where they are located in storehouse through the admin panel;
- Order processing through the admin panel where can see the customer's email, delivery address and books that ordered with their quantity;
- When the status of order changed, an email automatically sent to the customer's email with an updated order status, and books status change to unavailable and deducted from the total number of available books;
![alt text](https://github.com/Cubinec-py/microservice_storehouse_shop/blob/main/storehouse/storehouse_model_visualized.png?raw=true)

## SHOP on Django
- Registration/login (using modal window) + logout;
- Page with a list of all the books that are in the store, can search by book title, filter by price (from cheap to expensive), genre, author;
- Button with book-detail information (using modal window) + add to cart button (if not available, the button is not active "Out of stock");
- Shopping cart is available to registered/anonymous users;
- In the cart can add/reduce the number of selected books or remove them from the cart;
- If user anonymous, need to input name, email and delivery address, if user logged in, enough to enter the delivery address;
- Order and its status can be checked in "My orders" tab, if user anonymous, need to enter the order number which was sent to the user email specified in the order, if the user is logged in, the order list of this account will be immediately visible;
![alt text](https://github.com/Cubinec-py/microservice_storehouse_shop/blob/main/shop/shop_model_visualized.png?raw=true)

## Docker run
First of all create .env file in shop/core with environments.
```sh
  SECRET_KEY=''
  
  DB_NAME=""
  DB_USER=""
  DB_PASSWORD=""
  DB_HOST=""
  DB_PORT=""
```
The same for .env file in storehouse/core.
```sh
  SECRET_KEY=''
  
  DB_NAME=""
  DB_USER=""
  DB_PASSWORD=""
  DB_HOST=""
  DB_PORT=""
```
Next, need to build Docker images.
```sh
docker-compose build
```
This will create image and pull in the necessary dependencies.

For start microservice need to run this command
```sh
docker-compose up -d
```
After running need to make migrations for shop
```sh
docker-compose exec shop bash

./manage.py migrate

Ctrl+C or ⌃⌘ for exit
```
The same need to make for storehouse
```sh
docker-compose exec storehouse bash

./manage.py migrate

Ctrl+C or ⌃⌘ for exit
```
The last one thing which need to do, put secret token from storehouse
```sh
docker-compose exec storehouse bash

./manage.py createsuperuser

Username: example
Email address: example@example.com
Password: example
Password (again): example
Superuser created successfully.

Ctrl+C or ⌃⌘ for exit
```
That's all