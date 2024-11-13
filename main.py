class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class AuthSystem:
    def __init__(self):
        self.users = {
            'admin': User('admin', 'adminpass', 'Admin'),
            'user': User('user', 'userpass', 'User')
        }

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None

class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.product_id] = product

    def edit_product(self, product_id, **kwargs):
        if product_id in self.products:
            for key, value in kwargs.items():
                setattr(self.products[product_id], key, value)

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]

    def view_all_products(self):
        for product in self.products.values():
            print(product.__dict__)

class InventoryManager:
    def __init__(self):
        self.inventory = Inventory()

    def check_stock_levels(self, threshold):
        for product in self.inventory.products.values():
            if product.stock_quantity < threshold:
                print(f"Stock of {product.name} is low. Consider restocking.")

    def search_by_name(self, name):
        for product in self.inventory.products.values():
            if product.name == name:
                print(product.__dict__)

    def filter_by_category(self, category):
        for product in self.inventory.products.values():
            if product.category == category:
                print(product.__dict__)

    def find_product(self, product_id):
        try:
            product = self.inventory.products.get(product_id)
            if not product:
                raise InventoryError("Product not found.")
            return product
        except InventoryError as e:
            print(e)

class InventoryError(Exception):
    pass

def main():
    auth_system = AuthSystem()
    inventory_manager = InventoryManager()

    username = input("Enter username: ")
    password = input("Enter password: ")

    user = auth_system.login(username, password)
    if not user:
        print("Invalid login credentials.")
        return

    while True:
        if user.role == 'Admin':
            print("1. Add product")
            print("2. Edit product")
            print("3. Delete product")
            print("4. View all products")
            print("5. Check stock levels")
            option = int(input("Choose an option: "))

            if option == 1:
                product_id = input("Enter product ID: ")
                name = input("Enter product name: ")
                category = input("Enter product category: ")
                price = float(input("Enter product price: "))
                stock_quantity = int(input("Enter product stock quantity: "))
                product = Product(product_id, name, category, price, stock_quantity)
                inventory_manager.inventory.add_product(product)
            elif option == 2:
                product_id = input("Enter product ID to edit: ")
                updates = {}
                updates['name'] = input("Enter new product name (or press enter to skip): ")
                updates['category'] = input("Enter new product category (or press enter to skip): ")
                updates['price'] = float(input("Enter new product price (or press enter to skip): "))
                updates['stock_quantity'] = int(input("Enter new stock quantity (or press enter to skip): "))
                inventory_manager.inventory.edit_product(product_id, **{k: v for k, v in updates.items() if v})
            elif option == 3:
                product_id = input("Enter product ID to delete: ")
                inventory_manager.inventory.delete_product(product_id)
            elif option == 4:
                inventory_manager.inventory.view_all_products()
            elif option == 5:
                threshold = int(input("Enter stock threshold: "))
                inventory_manager.check_stock_levels(threshold)

        elif user.role == 'User':
            inventory_manager.inventory.view_all_products()
        
        if input("Do you want to logout? (yes/no): ").lower() == 'yes':
            break

if __name__ == "__main__":
    main()
