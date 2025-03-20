import os
import yaml
from dotenv import load_dotenv
import shopify

class ShopifyPublisher:
    def __init__(self):
        load_dotenv()
        self.setup_shopify_session()

    def setup_shopify_session(self):
        shop_url = os.getenv('SHOPIFY_SHOP_URL')
        access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')
        api_version = '2024-01'  # Using latest stable version
        
        shopify.Session.setup(api_key=os.getenv('SHOPIFY_API_KEY'),
                             secret=os.getenv('SHOPIFY_API_SECRET'))
        
        session = shopify.Session(shop_url, api_version, access_token)
        shopify.ShopifyResource.activate_session(session)

    def load_product_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'product_page.yaml')
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)['product']

    def create_product(self):
        config = self.load_product_config()
        
        # Create new product
        product = shopify.Product()
        product.title = config['title']
        product.body_html = config['description']
        product.vendor = os.getenv('SHOPIFY_STORE_NAME')
        product.product_type = 'Capa de Sofá'
        product.tags = config['seo']['tags']
        product.handle = config['seo']['url_handle']
        
        # Set variants
        variants = []
        for variant_config in config['variants']:
            variant = shopify.Variant({
                'price': variant_config['price'],
                'sku': variant_config['sku'],
                'option1': variant_config['color'],
                'inventory_management': 'shopify' if config['inventory']['track_inventory'] else None,
                'inventory_quantity': config['inventory']['quantity'],
                'compare_at_price': config['compare_at_price']
            })
            variants.append(variant)
        
        product.variants = variants
        
        # Set options
        product.options = [{
            'name': 'Cor',
            'values': [v['color'] for v in config['variants']]
        }]
        
        # Save product
        if product.save():
            print(f"Product created successfully: {product.title}")
            print(f"Product URL: {os.getenv('SHOPIFY_SHOP_URL')}/products/{product.handle}")
            return product
        else:
            print("Failed to create product:")
            print(product.errors.full_messages())
            return None

    def close_session(self):
        shopify.ShopifyResource.clear_session()

def publish_product():
    publisher = ShopifyPublisher()
    try:
        product = publisher.create_product()
        return product is not None
    finally:
        publisher.close_session()

if __name__ == '__main__':
    publish_product()