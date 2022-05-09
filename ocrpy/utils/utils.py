def tesseract_region_extractor(context):
    x, y, w, h = context.get('hpos'), context.get(
        'vpos'), context.get('width'), context.get('height')
    x, y, w, h = int(x), int(y), int(w), int(h)
    x2, y2 = x+w, y+h
    return dict(x1=x, y1=y, x2=x2, y2=y2)


def tesseract_text_extractor(context):
    return_data = ''
    if context.name == 'string':
        tokens = [context]
    else:
        tokens = context.find_all('string')
    token_count = len(tokens) - 1

    for index, token in enumerate(tokens):
        return_data += token.get('content')
        next_tag = token.find_next()
        if index < token_count and next_tag is not None and next_tag.name == 'sp':
            return_data += ' '

        if index < token_count and next_tag is not None and next_tag.name == 'textline':
            return_data += '\n'

    return return_data


def tesseract_index_extraction(context):
    idx = context.get('id')
    if idx is not None:
        idx = idx.split('_')[-1]
        idx = int(idx)
    return idx


def tesseract_token_extractor(context):
    token_list = []
    for token in context.find_all('string'):
        text = token.get('content')
        region = tesseract_region_extractor(token)
        index = tesseract_index_extraction(token)
        _ = dict(text=text, region=region, idx=index,
                 meta_data=dict(text_length=len(text)))
        token_list.append(_)
    return token_list


def aws_region_extractor(block):
    x1, x2 = block['Geometry']['BoundingBox']['Left'], block['Geometry']['BoundingBox']['Left'] + \
        block['Geometry']['BoundingBox']['Width']
    y1, y2 = block['Geometry']['BoundingBox']['Top'], block['Geometry']['BoundingBox']['Top'] + \
        block['Geometry']['BoundingBox']['Height']
    return dict(x1=x1, y1=y1, x2=x2, y2=y2)


def aws_token_formator(token):
    text = token.get("Text")
    index = token.get("Id")
    region = aws_region_extractor(token)
    metadata = dict(text_length=len(text), confidence=token.get("Confidence"))
    token = dict(text=text, region=region, idx=index, metadata=metadata)
    return token
