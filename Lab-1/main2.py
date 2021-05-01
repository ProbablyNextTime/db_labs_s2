import json
import os
import webbrowser
from typing import List, Tuple
from urllib.request import urlopen
from lxml import etree
import xml.etree.cElementTree as ET

INITIAL_URL = 'https://zvetsad.com.ua/catalog/klematisyi/'


def parse_zvetsad_website() -> None:
    xml_root = ET.Element("shop")
    htmlparser = etree.HTMLParser()
    # parse initial page to get list of urls to parse
    urls_to_parse: List[str] = parse_initial_page(htmlparser)

    # parse each url to get product info
    for url in urls_to_parse:
        response = urlopen(url)
        tree = etree.parse(response, htmlparser)
        parse_product_page(xml_root, tree, url)

    # wrtie parsed xml to zvetsad_website.xml
    xml_tree = ET.ElementTree(xml_root)
    xml_tree.write("zvetsad_website.xml", encoding="UTF-8")

    # get transform config
    transform = etree.XSLT(etree.parse("./transform.xsl"))
    # transform .xml to .xhtml
    result = transform(etree.parse("./zvetsad_website.xml"))
    # write result to parsed_zvetsad.xhtml
    result.write("./parsed_zvetsad.xhtml", pretty_print=True, encoding="UTF-8")
    webbrowser.open('file://' + os.path.realpath("./parsed_zvetsad.xhtml"))
    return


def parse_initial_page(htmlparser) -> List[str]:
    response = urlopen(INITIAL_URL)
    tree = etree.parse(response, htmlparser)
    urls = tree.xpath("//a[@class='product-image__body']/@href")
    urls_to_parse = urls[1:20]

    return urls_to_parse


def parse_product_page(xml_root, tree, url) -> None:
    product_name = parse_product_name(tree)
    product_price = parse_product_price(tree)
    product_description = parse_product_description(tree)
    product_image_url = parse_product_img_url(tree, product_name)

    page = ET.SubElement(xml_root, "product", url=url)
    ET.SubElement(page, "name").text = product_name
    ET.SubElement(page, "price").text = product_price
    ET.SubElement(page, "description").text = product_description
    ET.SubElement(page, "image").text = product_image_url
    return


def parse_product_img_url(tree, product_name) -> str:
    product_img_url = tree.xpath(f"//img/@src")[2]
    return product_img_url


def parse_product_description(tree) -> str:
    product_descriptions = tree.xpath("//div[@class='typography']//p/text()")
    product_description = ''

    for desc_part in product_descriptions:
        product_description += desc_part + '\n'

    return product_description


def parse_product_price(tree) -> str:
    product_price = tree.xpath("//div[@class='product__prices']/text()")[0]
    return product_price


def parse_product_name(tree) -> str:
    product_name = tree.xpath("//h1[@class='product__name']/text()")[0]
    return product_name


parse_zvetsad_website()
