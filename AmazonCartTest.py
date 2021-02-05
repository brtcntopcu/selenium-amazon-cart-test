from AmazonCartTestClass import AmazonCartTest

amazon = AmazonCartTest()
mail = ''
password = ''
product_url = 'https://www.amazon.com.tr/TOPLUM-S%C3%96ZLE%C5%9EMES%C4%B0-C%C4%B0LTS%C4%B0Z-Jacques-Rousseau/dp/9754589488/ref=pd_cart_crc_cko_bxgy_1_1/260-5786755-6409164?_encoding=UTF8&pd_rd_i=9754589488&pd_rd_r=08eab1e6-4175-410c-ad1b-5cc3e342393f&pd_rd_w=cCBWx&pd_rd_wg=q1glV&pf_rd_p=9f763341-826b-4e2d-9dec-7dcd00c7a0e5&pf_rd_r=NQVGMPDSHS217XR4A9JH&psc=1&refRID=NQVGMPDSHS217XR4A9JH'

# Basic Cart Total Check 
# Cart Should Be Empty Before Add Product to Cart


amazon.login(mail, password)
if amazon.cartCheck() > 0:
    amazon.goCart()
    amazon.clearCart()
amazon.addCartAnyProduct(product_url)
amazon.goCart()
amazon.cartTotalCheck()
amazon.closeBrowser()


