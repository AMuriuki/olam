from app.main.models.product import AttributeValue, ProductAttributeValue


def product_model(value):
    attribute = ProductAttributeValue.query.filter_by(
        product_id=value, attribute_id='96f65155-e8e3-4680-93bf-f305275062a7').first()
    print(value)
    print(attribute)
    if attribute:
        value_id = attribute.attribute_value_id
        value = AttributeValue.query.filter_by(id=value_id).first()
        return value.name
