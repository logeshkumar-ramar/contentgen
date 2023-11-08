import json
from bs4 import BeautifulSoup
from pathlib import Path


def escape_unsafe_characters(src: str) -> str:
    """
    Takes in a string str, and returns a string with any unsafe characters escaped.
    Unsafe characters are any characters which might break BEE editor's plugin configuration.
    """
    return src.replace('"', '"').replace("\\\\n","\\n")

def replace_social_content(template:str,links: list) -> str:
    soup = BeautifulSoup(template, "html.parser")

    table_class_name = 'social-table'
    
    table=soup.find('table',class_=table_class_name)
    if table:
        rows=table.find_all('tr')
        for row in rows:
            cols= row.find_all('td')
            cols[0].find('a')['href'] = links[0]
            cols[1].find('a')['href'] = links[1]
            cols[2].find('a')['href'] = links[2]
            cols[3].find('a')['href'] = links[3]
    
    return str(soup)

            # for index,col in cols:
                
                # col.find('a')['href'] = links[index]

def replace_product_details(template:str,product_url: list)-> str:
    soup = BeautifulSoup(template, "html.parser")
    image_row1 = soup.find("table", class_="row row-2")
    
    
    column1 = image_row1.find("td",class_="column column-1")
    column2 = image_row1.find("td",class_="column column-2")
    # print(column2)
    column3 = image_row1.find("td",class_="column column-3")
    # print(column3)


    column1.find("table",class_="image_block block-1").find('img')['src']=product_url[0]


    
    column1.find("table",class_="text_block block-2").find('p').string='product1'

    column2.find("table",class_="image_block block-1").find('img')['src']=product_url[0]

    column2.find("table",class_="text_block block-2").find('p').string='product2'
    

    column3.find("table",class_="image_block block-1").find('img')['src']=product_url[0]

    column3.find("table",class_="text_block block-2").find('p').string='product3'

    return str(soup)


def replace_content(template: str, replacement_content: str,content_bg_color: str) -> str:
    """
    Replaces the given content in the given template's content section. Content section is identified by
    the data attribute "data-blocktype='content-body'"

        Parameters:
            template (str): The template in which the content is to be replaced
            replacement_content (str): The content to replace with

        Returns:
            updated_template: The template with the content section updated with the given replacement_content
    """
    soup = BeautifulSoup(template, "html.parser")
    content_element = soup.select_one("span[data-blocktype='content_body']")
    if content_element is None:
        return template
    content_element.string = replacement_content








    return str(soup)



def replace_content_in_template(template: str, 
replacement_content: str , links: list,product: dict,content_bg_color: str) -> str:
    """
    Replaces the given content in the given template's content section. Content section is identified by
    the data attribute "data-blocktype='content-body'"

        Parameters:
            template (str): The template in which the content is to be replaced
            replacement_content (str): The content to replace with

        Returns:
            updated_template: The template with the content section updated with the given replacement_content
    """
    soup = BeautifulSoup(template, "html.parser")
    content_element = soup.select_one("span[data-blocktype='content_body']")
    if content_element is None:
        return template
    content_element.string = replacement_content

    content_row = soup.find("table", class_="row row-1")
    
    
    content_column = content_row.find("td",class_="column column-1")

    content_table = content_column.find("table","text_block block-2")

    content_table['style'] = 'background-color:'+content_bg_color


    #####Social###

    table_class_name = 'social-table'
    
    table=soup.find('table',class_=table_class_name)
    if table:
        rows=table.find_all('tr')
        for row in rows:
            cols= row.find_all('td')
            cols[0].find('a')['href'] = links[0]
            cols[1].find('a')['href'] = links[1]
            cols[2].find('a')['href'] = links[2]
            cols[3].find('a')['href'] = links[3]

    #####Product

    soup = BeautifulSoup(template, "html.parser")
    image_row1 = soup.find("table", class_="row row-2")
    
    
    column1 = image_row1.find("td",class_="column column-1")
    column2 = image_row1.find("td",class_="column column-2")
    # print(column2)
    column3 = image_row1.find("td",class_="column column-3")
    # print(column3)


    

    column1.find("table",class_="image_block block-1").find('img')['src']=product_url[0]


    
    column1.find("table",class_="text_block block-2").find('p').string='product1'

    column2.find("table",class_="image_block block-1").find('img')['src']=product_url[0]

    column2.find("table",class_="text_block block-2").find('p').string='product2'
    

    column3.find("table",class_="image_block block-1").find('img')['src']=product_url[0]

    column3.find("table",class_="text_block block-2").find('p').string='product3'
    
    
    return soup.prettify()


def replace_content_in_editor_configuration(
    configuration: str, replacement_content: str , links: list,product_url: list
) -> str:
    """
    Replaces the given original content with the given replacement_content in the given BEE editor configuration

        Parameters:
            configuration (str): The BEE editor configuration to replace the content in
            replacement_content (str): The content to replace with

        Returns:
            updated_configuration (str): The updated BEE editor configuration with the given replacement_content
    """
    if replacement_content is None or "" == replacement_content.strip():
        return configuration
    configuration_json = json.loads(configuration)
    for row in configuration_json.get("page", {}).get("rows"):
        for column in row.get("columns"):
            grid_column = column.get("grid-columns")
            if grid_column == 12:
                for module in column.get("modules"):
                    if module.get("type",{}) == 'mailup-bee-newsletter-modules-social':
                        if module.get("descriptor", {}).get("iconsList") is not None:
                            icons = module["descriptor"]["iconsList"]["icons"]
                            for i in range(len(icons)):
                                icons[i]["image"]["href"] = links[i]
                    
                    elif module.get("descriptor", {}).get("text") is not None:
                        module["descriptor"]["text"]["html"] = replace_content(
                            module["descriptor"]["text"]["html"], replacement_content,"#dc9a39"
                        )
            elif grid_column == 4:
                for module in column.get("modules"):
                    if module.get("descriptor", {}).get("image") is not None:
                        module["descriptor"]["image"]["src"]=product_url[0]
                        
    return json.dumps(configuration_json)


def replace_content_in_template_for_offer(template: str, replacement_content: str) -> str:
    """
    Replaces the given content in the given template's content section. Content section is identified by
    the data attribute "data-blocktype='content-body'"

        Parameters:
            template (str): The template in which the content is to be replaced
            replacement_content (str): The content to replace with

        Returns:
            updated_template: The template with the content section updated with the given replacement_content
    """
    soup = BeautifulSoup(template, "html.parser")
    content_element = soup.select_one("span[data-blocktype='content_body']")


    if content_element is None:
        return template
    content_element.string = replacement_content


# html_body_path = "template.html"
# json_body_path = "bee2.json"

# campaign_body = "Dearest [Name], Celebrate Diwali with glowing skin', 'Body': 'Dear [Name],\\n\\nAs the festival of lights and happiness, Diwali is just around the corner, we want you to start preparing not just with lights, sweets and gorgeous outfits, but also with healthy, beautiful and glowing skin. \\n\\n[Product/Brand Name] presents you with the perfect range of skin care and grooming essentials this Diwali. From our signature facial kits to our exclusive skin care range crafted especially for Indian skin, we have got you covered. \\n\\nSo, get ready to celebrate the radiant you this festive season with [Product/Brand Name]. Hoping to see you soon. \\n\\nWarm regards, \\n[Your Name]\\n[Product/Brand Name]"

# links = ['https://facebook.com/Deyga-Organics-SkinCare-1828253520578552','https://twitter.com/deygaorganics','https://instagram.com/deyga_organics','https://linkedin.com/company/deyga-organics']
# product_url = ['https://gallery.pre-freshmarketer.io/hackathon-event-cards/20231107192054894758.png']




# resources_base = Path(__file__).parent.resolve() / "resources"
# with (resources_base / html_body_path).open() as template, (
#             resources_base / json_body_path
#         ).open() as editor_config:
#         sanitized_template_content = escape_unsafe_characters(campaign_body)

        
#         updated_template = replace_content_in_template(
#             template.read(), sanitized_template_content,links,product_url,"#dc9a39"
#         )

#         updated_configuration = replace_content_in_editor_configuration(
#             editor_config.read(),sanitized_template_content,links,product_url)
        
#         print(updated_template)
        