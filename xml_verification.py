# -*- coding: utf-8 -*-
from lxml import etree
import logging

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler('processing.log', 'a', 'utf-8'), logging.StreamHandler()],
)


def xml_verification(xml_file: str, xsd_file: str) -> bool:
    try:
        xsd_etree = etree.parse(xsd_file)
        xml_etree = etree.parse(xml_file)
        xsd_schema = etree.XMLSchema(xsd_etree)
    except etree.XMLSyntaxError as exp:
        raise exp
    except IOError as exp:
        raise exp
    except etree.XMLSchemaParseError as exp:
        raise exp

    return xsd_schema.validate(xml_etree)


def xml_transformation(xml_file: str, xslt_file: str, output_file: str):
    try:
        xslt = etree.parse(xslt_file)
        xml_etree = etree.parse(xml_file)
        transform = etree.XSLT(xslt)
        newdom = transform(xml_etree)
        with open(output_file, mode='w', encoding='utf-8') as file:
            file.write(etree.tostring(newdom, pretty_print=True, encoding='utf-8').decode('utf-8'))
    except etree.XMLSyntaxError as exp:
        raise exp
    except etree.XSLTParseError as exp:
        raise exp
    except IOError as exp:
        raise exp


def xml_processing(xml_file: str, xsd_file: str, xslt_file: str, output_file: str):
    try:
        if xml_verification(xml_file, xsd_file):
            logging.info('Входящий xml файл прошел валидацию')
            xml_transformation(xml_file, xslt_file, output_file)
            logging.info(f'Трансформация xml файла. Исходящи файл {output_file}')
            if xml_verification(output_file, xsd_file):
                logging.info(f'Результирующий файл {output_file} прошел валидацию')
            else:
                logging.warning(f'Результирующий файл {output_file} не прошел валидацию')
        else:
            logging.warning('Входящий xml файл не прошел валидацию')

    except etree.XMLSyntaxError:
        logging.exception('Incorrect XML file')
    except etree.XMLSchemaParseError:
        logging.exception('Incorrect XSD schema')
    except etree.XSLTParseError:
        logging.exception('Incorrect XSLT file')
    except OSError:
        logging.exception('file missing')

