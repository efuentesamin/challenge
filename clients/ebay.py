from xml.etree import ElementTree

import requests

from models import Category


class EBayClient:
    _nsmap = {'n': 'urn:ebay:apis:eBLBaseComponents'}
    _url = 'https://api.sandbox.ebay.com/ws/api.dll'
    _headers = {
        'content-type': 'application/soap+xml',
        # 'content-type': 'text/xml',
        'X-EBAY-API-CALL-NAME': 'GetCategories',
        'X-EBAY-API-APP-NAME': 'EchoBay62-5538-466c-b43b-662768d6841',
        'X-EBAY-API-CERT-NAME': '00dd08ab-2082-4e3c-9518-5f4298f296db',
        'X-EBAY-API-DEV-NAME': '16a26b1b-26cf-442d-906d-597b60c41c19',
        'X-EBAY-API-SITEID': '0',
        'X-EBAY-API-COMPATIBILITY-LEVEL': '861'
    }
    _body = """
        <?xml version="1.0" encoding="utf-8"?>
        <GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
            <RequesterCredentials>
                <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**PlLuWA**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GlDpaDpAudj6x9nY+seQ**LyoEAA**AAMAAA**wSd/jBCbxJHbYuIfP4ESyC0mHG2Tn4O3v6rO2zmnoVSF614aVDFfLSCkJ5b9wg9nD7rkDzQayiqvwdWeoJkqEpNQx6wjbVQ1pjiIaWdrYRq+dXxxGHlyVd+LqL1oPp/T9PxgaVAuxFXlVMh6wSyoAMRySI6QUzalepa82jSQ/qDaurz40/EIhu6+sizj0mCgjcdamKhp1Jk3Hqmv8FXFnXouQ9Vr0Qt+D1POIFbfEg9ykH1/I2CYkZBMIG+k6Pf00/UujbQdne6HUAu6CSj9wGsqQSAEPIXXvEnVmtU+6U991ZUhPuA/DMFEfVlibvNLBA7Shslp2oTy2T0wlpJN+f/Jle3gurHLIPc6EkEmckEpmSpFEyuBKz+ix4Cf4wYbcUk/Gr3kGdSi20XQGu/ZnJ7Clz4vVak9iJjN99j8lwA2zKW+CBRuHBjZdaUiDctSaADHwfz/x+09bIU9icgpzuOuKooMM5STbt+yJlJZdE3SRZHwilC4dToTQeVhAXA4tFZcDrZFzBmJsoRsJYrCdkJBPeGBub+fqomQYyKt1J0LAQ5Y0FQxLHBIp0cRZTPAuL/MNxQ/UXcxQTXjoCSdZd7B55f0UapU3EsqetEFvIMPxCPJ63YahVprODDva9Kz/Htm3piKyWzuCXfeu3siJvHuOVyx7Q4wyHrIyiJDNz5b9ABAKKauxDP32uqD7jqDzsVLH11/imKLLdl0U5PN+FP30XAQGBAFkHf+pAvOFLrdDTSjT3oQhFRzRPzLWkFg</eBayAuthToken>
            </RequesterCredentials>
            <DetailLevel>ReturnAll</DetailLevel>
            <ErrorLanguage>en_US</ErrorLanguage>
        </GetCategoriesRequest>
    """

    @classmethod
    def get_categories(cls):
        """
        Request eBay API to get categories XML data
        :return: 
        """
        print('--------> Requesting eBay API...')
        response = requests.post(cls._url, data=cls._body, headers=cls._headers)
        return cls.parse_response(response.content)

    @classmethod
    def parse_response(cls, content):
        """
        Parse the XML response from eBay API
        :param content: XML data to parse
        :return: Categories dictionary
        """
        print('--------> Parsing response from eBay...')
        categories = []
        root = ElementTree.fromstring(content)
        ack_node = root.find('n:Ack', namespaces=cls._nsmap)

        # Verify whether response is success
        if ack_node is not None and ack_node.text == 'Success':
            count = root.find('n:CategoryCount', namespaces=cls._nsmap).text
            print('--------> {} categories found!'.format(count))
            categories_root = root.find('n:CategoryArray', namespaces=cls._nsmap)

            # Traverse the categories
            for node in categories_root.findall('n:Category', namespaces=cls._nsmap):
                category = Category(
                    cls.get_node_attrib(node, 'n:CategoryID'),
                    cls.get_node_attrib(node, 'n:CategoryName'),
                    cls.get_node_attrib(node, 'n:CategoryLevel'),
                    cls.get_node_attrib(node, 'n:CategoryParentID'),
                    cls.get_node_attrib(node, 'n:BestOfferEnabled'),
                    cls.get_node_attrib(node, 'n:Expired'),
                    cls.get_node_attrib(node, 'n:LeafCategory')
                )
                categories.append(category)
        else:
            print('--------> Error in eBay response!')

        return categories

    @classmethod
    def get_node_attrib(cls, node, attrib):
        """
        Get node attribute text if it exists
        :param node: XML node
        :param attrib: Searched attribute
        :return: Node attribute text
        """
        attr = node.find(attrib, namespaces=cls._nsmap)

        if attr is not None:

            if attr.text == 'true':
                return True
            elif attr.text == 'false':
                return False
            elif attr.text.isdigit():
                return int(attr.text)

            return attr.text

        return None
