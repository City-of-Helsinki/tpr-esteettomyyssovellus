from django.utils.encoding import force_str
from rest_framework_xml.renderers import XMLRenderer


class CustomXmlRenderer(XMLRenderer):
    """
    Renderer which serializes data to XML
    """

    # root_tag_name = "root"
    # item_tag_name = "list-item"

    def _to_xml(self, xml, data, item_tag_name=None):
        if isinstance(data, (list, tuple)):
            for item in data:
                if item_tag_name:
                    # xml.startElement(item_tag_name, {})
                    xml.startElement("string", {})
                    self._to_xml(xml, item, item_tag_name)
                    # xml.endElement(item_tag_name)
                    xml.endElement("string")
                else:
                    xml.startElement(self.item_tag_name, {})
                    self._to_xml(xml, item, item_tag_name)
                    xml.endElement(self.item_tag_name)

        elif isinstance(data, dict):
            for key, value in data.items():
                # xml.startElement(key.replace('_set', '-items'), {})
                xml.startElement(key, {})
                # self._to_xml(xml, value, key.replace('_set', '-item'))
                self._to_xml(xml, value, key)
                # xml.endElement(key.replace('_set', '-items'))
                xml.endElement(key)

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(force_str(data))
