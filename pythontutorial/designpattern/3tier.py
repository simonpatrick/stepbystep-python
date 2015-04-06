# _*_ coding=utf-8 _*_
__author__ = 'patrick'


class Model(object):
    """ Data Store Class """

    products = {
        'milk': {'price': 1.50, 'quantity': 10},
        'eggs': {'price': 0.20, 'quantity': 100},
        'cheese': {'price': 2.00, 'quantity': 10}
    }

    def __get__(self, obj, klas):
        print ("(Fetching from Data Store)")
        return {'products': self.products}


class BusinessObject(object):
    model = Model()
    print type(model.products)

    def product_list(self):
        return self.model['products'].keys()

    def product_information(self, product):
        return self.model['products'].get(product, None)


class View(object):
    """ UI interaction class """

    def __init__(self):
        self.business_logic = BusinessObject()

    def get_product_list(self):
        print('PRODUCT LIST:')
        for product in self.business_logic.product_list():
            print(product)
            yield product
        print('')

    def get_product_information(self, product):
        product_info = self.business_logic.product_information(product)
        if product_info:
            print('PRODUCT INFORMATION:')
            print('Name: {0}, Price: {1:.2f}, Quantity: {2:}'.format(
                product.title(), product_info.get('price', 0),
                product_info.get('quantity', 0)))
        else:
            print('That product "{0}" does not exist in the records'.format(
                product))

if __name__ == '__main__':
    ui = View()
    ui.get_product_list()
    ui.get_product_information('cheese')
    ui.get_product_information('eggs')
    ui.get_product_information('milk')
    ui.get_product_information('arepas')