import requests
import json
ETSY_API = 'https://openapi.etsy.com/v3/application/'
ETSY_API_KEY  = 'qqny8v0d71ev9ts06469ofh3'

def pushImaggesRelatedToVarients(store_id,header,product_id,data):
    shopify_url = f'https://{store_id}/admin/api/2023-01/products/{product_id}/images.json'
    img = {}
    img['image']= data;
    response = requests.post(shopify_url, headers=header, json=img)
    return response

def getVariantImagesByListingId(access_token,shop_id,listing_id):
    url = f'{ETSY_API}shops/{shop_id}/listings/{listing_id}/variation-images'
    headers = {
        'x-api-key': f'{ETSY_API_KEY}',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url,params=None,headers=headers)
    return json.loads(response.text)

def importListingToShopify(shop_id,listing_id,etsy,access_token,store_id,shopify_token):

    options = {}
    optionsListWithDict = []
    variants = []
    images = []
    variantImages = []


    for item in etsy['inventory']['products']:
        variant = {}
        variant['sku'] = item['sku']
        variant['inventory_quantity'] = item['offerings'][0]['quantity']
        variant['price'] = item['offerings'][0]['price']['amount'] / item['offerings'][0]['price']['divisor']
        variant['inventory_management'] = 'shopify'
        properties = item['property_values']
        for index, property in enumerate(properties):
            opt = 'option'+str(index+1)
            variant[opt] = properties[index]['values'][0]
            key = options.get(properties[index]['property_name'])

            if key is not None:
                values2 = options[properties[index]['property_name']]
                values2.add(properties[index]['values'][0])
                options[properties[index]['property_name']] = values2
            else:
                values = set()    
                values.add(properties[index]['values'][0])
                options[properties[index]['property_name']] = values

        variants.append(variant)
    
    for key in options.keys():
        option = {
        'name': key,
        'values': list(options[key])
        }
        optionsListWithDict.append(option)

    variant_images = getVariantImagesByListingId(access_token=access_token,shop_id=shop_id,listing_id=listing_id)

    for img in etsy['images']:
        image = {}
        flag = True
        for variantImg in variant_images['results']:
            if img['listing_image_id'] == variantImg['image_id']:
                variantImage = {}
                variantImage['src'] = img['url_fullxfull']
                variantImage['optionValue'] = variantImg['value']
                variantImages.append(variantImage)
                flag = False
        if flag == True:
            image['src'] = img['url_fullxfull']
            images.append(image)

    product = {
    'title': etsy['title'],
    'body_html': etsy['description'],
    'status': etsy['state'],
    'quantity': etsy['quantity'],
    'tags': etsy['tags'],
    'options': optionsListWithDict,
    'variants': variants,
    'images': images
    }

    listing = {}
    listing['product'] = product

    header = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": f"{shopify_token}"
    }
    shopify_url = f'https://{store_id}/admin/api/2023-01/products.json'

    response = requests.post(shopify_url, headers=header, json=listing)

    productShopify = json.loads(response.content)
    
    for variantImg in variantImages:
        img = {}
        img['src'] = variantImg['src']
        img['variant_ids'] = []
        for shopifyV in productShopify['product']['variants']:
            if variantImg['optionValue'] == shopifyV['option1'] or variantImg['optionValue'] == shopifyV['option2'] or variantImg['optionValue'] == shopifyV['option3']:
                img['variant_ids'].append(shopifyV['id'])
        pushImaggesRelatedToVarients(store_id=store_id,header=header,product_id= productShopify['product']['id'],data=img)
    


etsyListing = {'listing_id': 1395779480, 'user_id': 749170381, 'shop_id': 40753525, 'title': 'Vivobook 15 OLED (X1505)', 'description': 'This product has only been tested for compatibility with the Windows 11 operating system and may encounter compatibility issues if Windows 10 or older OS versions are installed.', 'state': 'draft', 'creation_timestamp': 1675502650, 'created_timestamp': 1675502650, 'ending_timestamp': 1685867050, 'original_creation_timestamp': 1675502650, 'last_modified_timestamp': 1675597230, 'updated_timestamp': 1675597230, 'state_timestamp': 1675502650, 'quantity': 35, 'shop_section_id': None, 'featured_rank': -1, 'url': 'https://www.etsy.com/listing/1395779480/vivobook-15-oled-x1505', 'num_favorers': 0, 'non_taxable': False, 'is_taxable': True, 'is_customizable': False, 'is_personalizable': False, 'personalization_is_required': False, 'personalization_char_count_max': None, 'personalization_instructions': None, 'listing_type': 'physical', 'tags': ['Asus', 'Vivobook'], 'materials': [], 'shipping_profile_id': 193533280661, 'return_policy_id': 1137811818665, 'processing_min': 1, 'processing_max': 2, 'who_made': 'someone_else', 'when_made': '2020_2023', 'is_supply': False, 'item_weight': None, 'item_weight_unit': None, 'item_length': None, 'item_width': None, 'item_height': None, 'item_dimensions_unit': None, 'is_private': False, 'style': [], 'file_data': '', 'has_variations': True, 'should_auto_renew': True, 'language': 'en-US', 'price': {'amount': 5000000, 'divisor': 100, 'currency_code': 'INR'}, 'taxonomy_id': 851, 'production_partners': [{'production_partner_id': 2660448, 'partner_name': 'Asus', 'location': 'Taiwan'}], 'skus': [], 'views': 0, 'shipping_profile': None, 'shop': None, 'images': [{'listing_id': 1395779480, 'listing_image_id': 4592832960, 'hex_code': 'C7CBD2', 'red': 199, 'green': 203, 'blue': 210, 'hue': 218, 'saturation': 6, 'brightness': 83, 'is_black_and_white': False, 'creation_tsz': 1675502650, 'created_timestamp': 1675502650, 'rank': 1, 'url_75x75': 'https://i.etsystatic.com/40753525/r/il/11fa06/4592832960/il_75x75.4592832960_rf43.jpg', 'url_170x135': 'https://i.etsystatic.com/40753525/r/il/11fa06/4592832960/il_170x135.4592832960_rf43.jpg', 'url_570xN': 'https://i.etsystatic.com/40753525/r/il/11fa06/4592832960/il_570xN.4592832960_rf43.jpg', 'url_fullxfull': 'https://i.etsystatic.com/40753525/r/il/11fa06/4592832960/il_fullxfull.4592832960_rf43.jpg', 'full_height': 800, 'full_width': 800, 'alt_text': None}, {'listing_id': 1395779480, 'listing_image_id': 4641074065, 'hex_code': 'CED0D8', 'red': 206, 'green': 208, 'blue': 216, 'hue': 228, 'saturation': 5, 'brightness': 85, 'is_black_and_white': False, 'creation_tsz': 1675502650, 'created_timestamp': 1675502650, 'rank': 2, 'url_75x75': 'https://i.etsystatic.com/40753525/r/il/e86c89/4641074065/il_75x75.4641074065_incy.jpg', 'url_170x135': 'https://i.etsystatic.com/40753525/r/il/e86c89/4641074065/il_170x135.4641074065_incy.jpg', 'url_570xN': 'https://i.etsystatic.com/40753525/r/il/e86c89/4641074065/il_570xN.4641074065_incy.jpg', 'url_fullxfull': 'https://i.etsystatic.com/40753525/r/il/e86c89/4641074065/il_fullxfull.4641074065_incy.jpg', 'full_height': 800, 'full_width': 800, 'alt_text': None}, {'listing_id': 1395779480, 'listing_image_id': 4592832840, 'hex_code': 'ABAFB9', 'red': 171, 'green': 175, 'blue': 185, 'hue': 222, 'saturation': 8, 'brightness': 73, 'is_black_and_white': False, 'creation_tsz': 1675502650, 'created_timestamp': 1675502650, 'rank': 3, 'url_75x75': 'https://i.etsystatic.com/40753525/r/il/a990ef/4592832840/il_75x75.4592832840_ma6d.jpg', 'url_170x135': 'https://i.etsystatic.com/40753525/r/il/a990ef/4592832840/il_170x135.4592832840_ma6d.jpg', 'url_570xN': 'https://i.etsystatic.com/40753525/r/il/a990ef/4592832840/il_570xN.4592832840_ma6d.jpg', 'url_fullxfull': 'https://i.etsystatic.com/40753525/r/il/a990ef/4592832840/il_fullxfull.4592832840_ma6d.jpg', 'full_height': 80, 'full_width': 80, 'alt_text': None}, {'listing_id': 1395779480, 'listing_image_id': 4592833116, 'hex_code': '050F53', 'red': 5, 'green': 15, 'blue': 83, 'hue': 232, 'saturation': 94, 'brightness': 33, 'is_black_and_white': False, 'creation_tsz': 1675502650, 'created_timestamp': 1675502650, 'rank': 4, 'url_75x75': 'https://i.etsystatic.com/40753525/r/il/79f9fc/4592833116/il_75x75.4592833116_hlen.jpg', 'url_170x135': 'https://i.etsystatic.com/40753525/r/il/79f9fc/4592833116/il_170x135.4592833116_hlen.jpg', 'url_570xN': 'https://i.etsystatic.com/40753525/r/il/79f9fc/4592833116/il_570xN.4592833116_hlen.jpg', 'url_fullxfull': 'https://i.etsystatic.com/40753525/r/il/79f9fc/4592833116/il_fullxfull.4592833116_hlen.jpg', 'full_height': 800, 'full_width': 800, 'alt_text': None}, {'listing_id': 1395779480, 'listing_image_id': 4641073777, 'hex_code': '091250', 'red': 9, 'green': 18, 'blue': 80, 'hue': 232, 'saturation': 89, 'brightness': 32, 'is_black_and_white': False, 'creation_tsz': 1675502650, 'created_timestamp': 1675502650, 'rank': 5, 'url_75x75': 'https://i.etsystatic.com/40753525/r/il/95d1ff/4641073777/il_75x75.4641073777_erll.jpg', 'url_170x135': 'https://i.etsystatic.com/40753525/r/il/95d1ff/4641073777/il_170x135.4641073777_erll.jpg', 'url_570xN': 'https://i.etsystatic.com/40753525/r/il/95d1ff/4641073777/il_570xN.4641073777_erll.jpg', 'url_fullxfull': 'https://i.etsystatic.com/40753525/r/il/95d1ff/4641073777/il_fullxfull.4641073777_erll.jpg', 'full_height': 80, 'full_width': 80, 'alt_text': None}, {'listing_id': 1395779480, 'listing_image_id': 4592833074, 'hex_code': '303133', 'red': 48, 'green': 49, 'blue': 51, 'hue': 220, 'saturation': 6, 'brightness': 20, 'is_black_and_white': False, 'creation_tsz': 1675502650, 'created_timestamp': 1675502650, 'rank': 6, 'url_75x75': 'https://i.etsystatic.com/40753525/r/il/6904f1/4592833074/il_75x75.4592833074_6b00.jpg', 'url_170x135': 'https://i.etsystatic.com/40753525/r/il/6904f1/4592833074/il_170x135.4592833074_6b00.jpg', 'url_570xN': 'https://i.etsystatic.com/40753525/r/il/6904f1/4592833074/il_570xN.4592833074_6b00.jpg', 'url_fullxfull': 'https://i.etsystatic.com/40753525/r/il/6904f1/4592833074/il_fullxfull.4592833074_6b00.jpg', 'full_height': 800, 'full_width': 800, 'alt_text': None}], 'videos': [], 'user': None, 'translations': {'en-US': {'listing_id': 1395779480, 'language': 'en-US', 'translation_system_id': None, 'title': 'Vivobook 15 OLED (X1505)', 'description': 'This product has only been tested for compatibility with the Windows 11 operating system and may encounter compatibility issues if Windows 10 or older OS versions are installed.', 'tags': ['Asus', 'Vivobook']}}, 'inventory': {'products': [{'product_id': 13415649976, 'sku': '', 'is_deleted': False, 'offerings': [{'offering_id': 13374444972, 'quantity': 20, 'is_enabled': True, 'is_deleted': False, 'price': {'amount': 6000000, 'divisor': 100, 'currency_code': 'INR'}}], 'property_values': [{'property_id': 513, 'property_name': 'RAM and ROM', 'scale_id': None, 'scale_name': None, 'value_ids': [1117060863382], 'values': ['8GB 512GB']}, {'property_id': 514, 'property_name': 'Processor', 'scale_id': None, 'scale_name': None, 'value_ids': [1009562065608], 'values': ['I5']}]}, {'product_id': 13415649982, 'sku': '', 'is_deleted': False, 'offerings': [{'offering_id': 13374444980, 'quantity': 1, 'is_enabled': True, 'is_deleted': False, 'price': {'amount': 75000000, 'divisor': 100, 'currency_code': 'INR'}}], 'property_values': [{'property_id': 513, 'property_name': 'RAM and ROM', 'scale_id': None, 'scale_name': None, 'value_ids': [1117060863382], 'values': ['8GB 512GB']}, {'property_id': 514, 'property_name': 'Processor', 'scale_id': None, 'scale_name': None, 'value_ids': [1009562065678], 'values': ['I7']}]}, {'product_id': 13095491337, 'sku': '', 'is_deleted': False, 'offerings': [{'offering_id': 13215778451, 'quantity': 1, 'is_enabled': True, 'is_deleted': False, 'price': {'amount': 5000000, 'divisor': 100, 'currency_code': 'INR'}}], 'property_values': [{'property_id': 513, 'property_name': 'RAM and ROM', 'scale_id': None, 'scale_name': None, 'value_ids': [1117060863664], 'values': ['16GB 1TB']}, {'property_id': 514, 'property_name': 'Processor', 'scale_id': None, 'scale_name': None, 'value_ids': [1009562065608], 'values': ['I5']}]}, {'product_id': 13095491343, 'sku': '', 'is_deleted': False, 'offerings': [{'offering_id': 13374445000, 'quantity': 13, 'is_enabled': True, 'is_deleted': False, 'price': {'amount': 9000000, 'divisor': 100, 'currency_code': 'INR'}}], 'property_values': [{'property_id': 513, 'property_name': 'RAM and ROM', 'scale_id': None, 'scale_name': None, 'value_ids': [1117060863664], 'values': ['16GB 1TB']}, {'property_id': 514, 'property_name': 'Processor', 'scale_id': None, 'scale_name': None, 'value_ids': [1009562065678], 'values': ['I7']}]}], 'price_on_property': [513, 514], 'quantity_on_property': [513, 514], 'sku_on_property': [], 'listing': None}}
importListingToShopify(shop_id=40753525,listing_id=1395779480,etsy=etsyListing,access_token="749170381.TLzZ0roG2YCIjjww-hpNcOUhh3HU_tpn4hMWNpJalDE8z0g9FumY7SKkS6WOELXKhu6tVnasZzcIO9A2SaOMWEanjY",store_id='nex-app-test.myshopify.com',shopify_token="shpua_dafd1debf84b716b36d4a80b16c4c435")