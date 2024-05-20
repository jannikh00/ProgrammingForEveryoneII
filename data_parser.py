# Program that contains two functions, one that parses an JSON string to a Python dictionary
# and one that parses a XML string into a nested Python dictionary. Both functions get tested
# by three small example strings.

#################################### IMPORTING ####################################
import json
import xml.etree.cElementTree as ET

#################################### FUNCTIONS ####################################
def json_parser(json_string):
    # Use built-in function to parse string
    parsed_string = json.loads(json_string)
    return parsed_string        

def xml_parser(xml_string):
    root = ET.fromstring(xml_string)  # Parse the XML string into an Element
    
    def parse_element(element):
        # If the element is a leaf node
        if not list(element) and not element.attrib:
            return element.text
        
        # Handling elements with attributes or children
        result = {}
        if element.attrib:
            result['attributes'] = element.attrib
        
        # Grouping children by tag, handling multiple elements with the same tag
        for child in element:
            child_result = parse_element(child)
            if child.tag not in result:
                result[child.tag] = child_result
            else:
                if not isinstance(result[child.tag], list):
                    # Convert to list if there's more than one child with the same tag
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_result)
        
        return result

    return {root.tag: parse_element(root)}


#################################### JSON TESTS ####################################
json_1 = '''
{
  "person": {
    "name": "John Doe",
    "age": 30,
    "email": "johndoe@example.com"
  }
}
'''
json_2 = '''
{
  "product": {
    "id": "101",
    "name": "Laptop",
    "price": 799.99
  }
}
'''
json_3 = '''
{
  "event": {
    "title": "Concert",
    "date": "2024-05-01",
    "location": "City Arena"
  }
}
'''
json_4 = '''
{
    "data":{
        "countries":[
            {
                "name": "Liechtenstein",
                "rank": 1,
                "year": 2008,
                "gdppc": 141100,
                "neighbors":[
                    {
                        "name": "Austria",
                        "direction": "E"
                    },
                    {
                        "name": "Switzerland",
                        "direction": "W"
                    }
                ]
            },
            {
                "name": "Singapore",
                "rank": 4,
                "year": 2011,
                "gdppc": 59900,
                "neighbors":[
                {
                    "name": "Malaysia",
                    "direction": "N"
                }
                ]
            },
            {
                "name": "Panama",
                "rank": 68,
                "year": 2011,
                "gdppc": 13600,
                "neighbors":[
                {
                    "name": "Costa Rica",
                    "direction": "W"
                },
                {
                    "name": "Colombia",
                    "direction": "E"
                }
                ]
            }
        ]
    }
}
'''
json_string_list = [json_1, json_2, json_3, json_4]
print("\nJSON to Dictionary Tests:\n")
for i in json_string_list:
    try:
        print(f"Type: \n{type(json_parser(i))}")
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e.msg)
    except Exception as e:
        print("An unknown Error has occured:", str(e))
    try:
        print(f"Dictionary: \n{json_parser(i)}\n")
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e.msg)
    except Exception as e:
        print("An unknown Error has occured:", str(e))
print("\n\n")

#################################### XML TESTS ####################################
xml_1 = '''
<person>
  <name>John Doe</name>
  <age>30</age>
  <email>johndoe@example.com</email>
</person>
'''
xml_2 = '''
<product>
  <id>101</id>
  <name>Laptop</name>
  <price>799.99</price>
</product>
'''
xml_3 = '''
<event>
  <title>Concert</title>
  <date>2024-05-01</date>
  <location>City Arena</location>
</event>
'''
xml_4 = '''
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
'''
xml_string_list = [xml_1, xml_2, xml_3, xml_4]
print("\nXML to Dictionary Tests:\n")
for i in xml_string_list:
    try:
        print(f"Type: \n{type(xml_parser(i))}")
    except Exception as e:
        print("An Error has occured:", str(e))
    try:
        print(f"Dictionary: \n{xml_parser(i)}\n")
    except Exception as e:
        print("An Error has occured:", str(e))
print("\n\n")