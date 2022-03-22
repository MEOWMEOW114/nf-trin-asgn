import asyncio
import boto3
import os
from bs4 import BeautifulSoup
import pandas as pd

from dotenv import load_dotenv
load_dotenv()
import datetime as dt
from io import StringIO


async def main():
    dest_s3_bucket = os.getenv('DEST_S3_BUCKET')
    dest_aws_access_key_id = os.getenv('DEST_S3_ACCESS_KEY')
    dest_aws_secret_access_key =  os.getenv('DEST_S3_SECRET_ACCESS_KEY')
    dest_s3_primary_bucket = 'nft-question2-scraping-primary'

    s3_target = boto3.client('s3', region_name="ap-northeast-1",aws_access_key_id=dest_aws_access_key_id, aws_secret_access_key=dest_aws_secret_access_key)
        
    sample_key = 'raw/2022/03/22/michaelkors_global/woman/handbags/source.html'
    obj = s3_target.get_object(Bucket='nft-question2-scraping-raw', Key=sample_key)
    html = (obj['Body'].read())
    soup = BeautifulSoup(html, 'lxml') 
    
    data = []

    type1_products = soup.find_all('div', class_="product-tile")
    print(len(type1_products))

    for product in type1_products:
        name =  product.find('li', class_='product-name-container').find('a').string
        price = product.find('li', class_='product-price-container').find('span', class_='ada-link productAmount').string
        price = price.replace('HK$', '').replace(',', '').strip()
        print(name, price)
        data.append([dt.datetime.now(),name, price])
# <li class="product-tile left medium-3 small-6">
# <div class="product-tile-container"><div class="image-panel">
# <a title="Eva Large Logo Stripe Tote Bag" href="/en_HK/eva-large-logo-stripe-tote-bag/_/R-30T9GV0T7B?color=7988">
# <div class="product-image-container"><div><div class="LazyLoad">
# <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAADYCAIAAADj3H/WAAAACXBIWXMAAAsTAAALEwEAmpwYAAAKT2lDQ1BQaG90b3Nob3AgSUNDIHByb2ZpbGUAAHjanVNnVFPpFj333vRCS4iAlEtvUhUIIFJCi4AUkSYqIQkQSoghodkVUcERRUUEG8igiAOOjoCMFVEsDIoK2AfkIaKOg6OIisr74Xuja9a89+bN/rXXPues852zzwfACAyWSDNRNYAMqUIeEeCDx8TG4eQuQIEKJHAAEAizZCFz/SMBAPh+PDwrIsAHvgABeNMLCADATZvAMByH/w/qQplcAYCEAcB0kThLCIAUAEB6jkKmAEBGAYCdmCZTAKAEAGDLY2LjAFAtAGAnf+bTAICd+Jl7AQBblCEVAaCRACATZYhEAGg7AKzPVopFAFgwABRmS8Q5ANgtADBJV2ZIALC3AMDOEAuyAAgMADBRiIUpAAR7AGDIIyN4AISZABRG8lc88SuuEOcqAAB4mbI8uSQ5RYFbCC1xB1dXLh4ozkkXKxQ2YQJhmkAuwnmZGTKBNA/g88wAAKCRFRHgg/P9eM4Ors7ONo62Dl8t6r8G/yJiYuP+5c+rcEAAAOF0ftH+LC+zGoA7BoBt/qIl7gRoXgugdfeLZrIPQLUAoOnaV/Nw+H48PEWhkLnZ2eXk5NhKxEJbYcpXff5nwl/AV/1s+X48/Pf14L7iJIEyXYFHBPjgwsz0TKUcz5IJhGLc5o9H/LcL//wd0yLESWK5WCoU41EScY5EmozzMqUiiUKSKcUl0v9k4t8s+wM+3zUAsGo+AXuRLahdYwP2SycQWHTA4vcAAPK7b8HUKAgDgGiD4c93/+8//UegJQCAZkmScQAAXkQkLlTKsz/HCAAARKCBKrBBG/TBGCzABhzBBdzBC/xgNoRCJMTCQhBCCmSAHHJgKayCQiiGzbAdKmAv1EAdNMBRaIaTcA4uwlW4Dj1wD/phCJ7BKLyBCQRByAgTYSHaiAFiilgjjggXmYX4IcFIBBKLJCDJiBRRIkuRNUgxUopUIFVIHfI9cgI5h1xGupE7yAAygvyGvEcxlIGyUT3UDLVDuag3GoRGogvQZHQxmo8WoJvQcrQaPYw2oefQq2gP2o8+Q8cwwOgYBzPEbDAuxsNCsTgsCZNjy7EirAyrxhqwVqwDu4n1Y8+xdwQSgUXACTYEd0IgYR5BSFhMWE7YSKggHCQ0EdoJNwkDhFHCJyKTqEu0JroR+cQYYjIxh1hILCPWEo8TLxB7iEPENyQSiUMyJ7mQAkmxpFTSEtJG0m5SI+ksqZs0SBojk8naZGuyBzmULCAryIXkneTD5DPkG+Qh8lsKnWJAcaT4U+IoUspqShnlEOU05QZlmDJBVaOaUt2ooVQRNY9aQq2htlKvUYeoEzR1mjnNgxZJS6WtopXTGmgXaPdpr+h0uhHdlR5Ol9BX0svpR+iX6AP0dwwNhhWDx4hnKBmbGAcYZxl3GK+YTKYZ04sZx1QwNzHrmOeZD5lvVVgqtip8FZHKCpVKlSaVGyovVKmqpqreqgtV81XLVI+pXlN9rkZVM1PjqQnUlqtVqp1Q61MbU2epO6iHqmeob1Q/pH5Z/YkGWcNMw09DpFGgsV/jvMYgC2MZs3gsIWsNq4Z1gTXEJrHN2Xx2KruY/R27iz2qqaE5QzNKM1ezUvOUZj8H45hx+Jx0TgnnKKeX836K3hTvKeIpG6Y0TLkxZVxrqpaXllirSKtRq0frvTau7aedpr1Fu1n7gQ5Bx0onXCdHZ4/OBZ3nU9lT3acKpxZNPTr1ri6qa6UbobtEd79up+6Ynr5egJ5Mb6feeb3n+hx9L/1U/W36p/VHDFgGswwkBtsMzhg8xTVxbzwdL8fb8VFDXcNAQ6VhlWGX4YSRudE8o9VGjUYPjGnGXOMk423GbcajJgYmISZLTepN7ppSTbmmKaY7TDtMx83MzaLN1pk1mz0x1zLnm+eb15vft2BaeFostqi2uGVJsuRaplnutrxuhVo5WaVYVVpds0atna0l1rutu6cRp7lOk06rntZnw7Dxtsm2qbcZsOXYBtuutm22fWFnYhdnt8Wuw+6TvZN9un2N/T0HDYfZDqsdWh1+c7RyFDpWOt6azpzuP33F9JbpL2dYzxDP2DPjthPLKcRpnVOb00dnF2e5c4PziIuJS4LLLpc+Lpsbxt3IveRKdPVxXeF60vWdm7Obwu2o26/uNu5p7ofcn8w0nymeWTNz0MPIQ+BR5dE/C5+VMGvfrH5PQ0+BZ7XnIy9jL5FXrdewt6V3qvdh7xc+9j5yn+M+4zw33jLeWV/MN8C3yLfLT8Nvnl+F30N/I/9k/3r/0QCngCUBZwOJgUGBWwL7+Hp8Ib+OPzrbZfay2e1BjKC5QRVBj4KtguXBrSFoyOyQrSH355jOkc5pDoVQfujW0Adh5mGLw34MJ4WHhVeGP45wiFga0TGXNXfR3ENz30T6RJZE3ptnMU85ry1KNSo+qi5qPNo3ujS6P8YuZlnM1VidWElsSxw5LiquNm5svt/87fOH4p3iC+N7F5gvyF1weaHOwvSFpxapLhIsOpZATIhOOJTwQRAqqBaMJfITdyWOCnnCHcJnIi/RNtGI2ENcKh5O8kgqTXqS7JG8NXkkxTOlLOW5hCepkLxMDUzdmzqeFpp2IG0yPTq9MYOSkZBxQqohTZO2Z+pn5mZ2y6xlhbL+xW6Lty8elQfJa7OQrAVZLQq2QqboVFoo1yoHsmdlV2a/zYnKOZarnivN7cyzytuQN5zvn//tEsIS4ZK2pYZLVy0dWOa9rGo5sjxxedsK4xUFK4ZWBqw8uIq2Km3VT6vtV5eufr0mek1rgV7ByoLBtQFr6wtVCuWFfevc1+1dT1gvWd+1YfqGnRs+FYmKrhTbF5cVf9go3HjlG4dvyr+Z3JS0qavEuWTPZtJm6ebeLZ5bDpaql+aXDm4N2dq0Dd9WtO319kXbL5fNKNu7g7ZDuaO/PLi8ZafJzs07P1SkVPRU+lQ27tLdtWHX+G7R7ht7vPY07NXbW7z3/T7JvttVAVVN1WbVZftJ+7P3P66Jqun4lvttXa1ObXHtxwPSA/0HIw6217nU1R3SPVRSj9Yr60cOxx++/p3vdy0NNg1VjZzG4iNwRHnk6fcJ3/ceDTradox7rOEH0x92HWcdL2pCmvKaRptTmvtbYlu6T8w+0dbq3nr8R9sfD5w0PFl5SvNUyWna6YLTk2fyz4ydlZ19fi753GDborZ752PO32oPb++6EHTh0kX/i+c7vDvOXPK4dPKy2+UTV7hXmq86X23qdOo8/pPTT8e7nLuarrlca7nuer21e2b36RueN87d9L158Rb/1tWeOT3dvfN6b/fF9/XfFt1+cif9zsu72Xcn7q28T7xf9EDtQdlD3YfVP1v+3Njv3H9qwHeg89HcR/cGhYPP/pH1jw9DBY+Zj8uGDYbrnjg+OTniP3L96fynQ89kzyaeF/6i/suuFxYvfvjV69fO0ZjRoZfyl5O/bXyl/erA6xmv28bCxh6+yXgzMV70VvvtwXfcdx3vo98PT+R8IH8o/2j5sfVT0Kf7kxmTk/8EA5jz/GMzLdsAAAAgY0hSTQAAeiUAAICDAAD5/wAAgOkAAHUwAADqYAAAOpgAABdvkl/FRgAAAVxJREFUeNrs0UERAAAIwzDAv9698bFLJTSbZNTbWQBYgAVYgAVYgAUYsAALsAALsAALMGABFmABFmABFmABBizAAizAAizAAgxYgAVYgAVYgAUYsAALsAALsAALsAADFmABFmABFmABBizAAizAAizAAgxYgAVYgAVYgAVYgAELsAALsAALsAADFmABFmABFmABFmDAAizAAizAAizAgAVYgAVYgAVYgAELsAALsAALsAALMGABFmABFmABFmDAAizAAizAAizAgAVYgAVYgAVYgAUYsAALsAALsAALMGABFmABFmABFmABBizAAizAAizAAgxYgAVYgAVYgAUYsAALsAALsAALsAADFmABFmABFmABBizAAizAAizAAgxYgAVYgAVYgAVYgAELsAALsAALsAADFmABFmABFmABFmDAAizAAizAAizAgAVYgAVYgAVYgAGrswcAAP//AwBPugSSpkSJwgAAAABJRU5ErkJggg==" alt="Eva Large Logo Stripe Tote Bag" data-altsrc="//michaelkors.scene7.com/is/image/MichaelKors/30T9GV0T7B-7988_2?$categoryMediumNew$&amp;fmt=pjpeg" data-src="//michaelkors.scene7.com/is/image/MichaelKors/30T9GV0T7B-7988_IS?$categoryMediumNew$&amp;fmt=pjpeg" class="product-image">

# </div>
# </div></div></a></div></div>
# <ul class="description-panel text-left">
# <li class="product-brand-container">
# <a activeclassname="active" title="Eva Large Logo Stripe Tote Bag" aria-label="" href="/en_HK/eva-large-logo-stripe-tote-bag/_/R-30T9GV0T7B">michael michael kors</a>
# </li>
# 
# <li class="product-name-container">
# <a activeclassname="active" title="Eva Large Logo Stripe Tote Bag" aria-label="" href="/en_HK/eva-large-logo-stripe-tote-bag/_/R-30T9GV0T7B">Eva Large Logo Stripe Tote Bag</a></li><li class="product-price-container"><a title="Eva Large Logo Stripe Tote Bag" href="/en_HK/eva-large-logo-stripe-tote-bag/_/R-30T9GV0T7B"><div class="Price"><span class="ada-link"><span class="ada-link productAmount" aria-hidden="true">HK$&nbsp;3,100.00</span><span class="ada-link visually-hidden">HK$&nbsp;3,100.00</span></span></div></a></li><li class="product-color-swatches-container"><div class="lazyload-placeholder" style="height: 25px;">
# </div></li></ul></li>
    type2_products = soup.find_all('li', class_="product-tile")
    print(len(type2_products))

    for product in type2_products:
        name =  product.find('li', class_='product-name-container').find('a').string
        price = product.find('li', class_='product-price-container').find('span', class_='ada-link productAmount').string
        price = price.replace('HK$', '').replace(',', '').strip()
        # print(price)
        # print(name, price)

        data.append([dt.datetime.now(),name, price])

    df = pd.DataFrame(data, columns=['Create At', 'Name', 'Price'])
    csv_buffer = StringIO()
    # print(df)
    df.to_csv(csv_buffer)
    # s3_resource = boto3.resource('s3')
    object_key = 'primary/2022/03/22/michaelkors_global/woman/handbags/data.csv'

    s3_target.put_object(Body=csv_buffer.getvalue(), Bucket=dest_s3_primary_bucket, Key=f'{object_key}')

if __name__ == '__main__':
    asyncio.run(main())  
