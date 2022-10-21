import parsel
import yaml



def extract_field(element, item_type):
    if item_type == 'Text':
        texts = [i.strip() for i in element.xpath('.//text()').getall() if i.strip()]
        content = " ".join(texts)
    
    
    return content


class Extractor:
    """selector class"""
    def __init__(self, config):
        self.config = config
        

    

    @classmethod
    def from_yaml_file(cls, yaml_filename: str):
        
        with open(yaml_filename) as yaml_fileobj:
            config = yaml.safe_load(yaml_fileobj.read())
        return cls(config)


    def extract(self, html: str, base_url: str = None):
       
        sel = parsel.Selector(html, base_url=base_url)
        if base_url:
            sel.root.make_links_absolute()
        fields_data = {}
        for selector_name, selector_config in self.config.items():
            fields_data[selector_name] = self._extract_selector(selector_config, sel)
        return fields_data


    def _extract_selector(self, field_config, parent_parser):
        if field_config.get("xpath") is not None:
            elements = parent_parser.xpath(field_config['xpath'])
        else:
            css = field_config['css']
            if css == '':
                elements = [parent_parser]
            else:
                elements = parent_parser.css(field_config['css'])
        item_type = field_config.get('type', 'Text')
        if not elements:
            return None
        values = []


        for element in elements:
            if 'children' in field_config:
                value = self._get_child_item(field_config, element)
            else:
                value = extract_field(element, item_type)

            if field_config.get('multiple') is not True:
                return value
            else:
                values.append(value)

        return values


    def _get_child_item(self, field_config, element):
        children_config = field_config['children']
        child_item = {}
        for field in children_config:
            child_value = self._extract_selector(children_config[field], element)
            child_item[field] = child_value
        return child_item

