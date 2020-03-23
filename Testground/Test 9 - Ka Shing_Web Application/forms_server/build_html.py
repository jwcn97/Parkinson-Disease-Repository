def build_html(tag, attr=None, content='', enclose=True):
    """
    Generates a html tag with the given attributes, enclosing the desired content. 
    Contents are only added if the tag is enclosed. Otherwise, it is dropped. 

    Parameters
    ----------
    tag (str)
        The HTML tag
    attr (dictionary, {})
        Dictionary containing the attributes and their values
        Each key is the attribute
        Each value is the corresponding attribute's value
        Both keys and values are cast to strings
        e.g. a key-value pair of 'class': 'test' will be generated as 'class'='test'
    content (str)
        The content that goes between the opening and closing tags.
    enclose (boolean)
        Whether an enclosing tag should be added. 

    Result
    ------
    string (str)
        HTML string
    """
    string = '' # HTML string

    # Opening tag
    string += '<' + tag

    # Add attributes
    if attr is not None: 
        for k, v in attr.items():
            string += ' ' + str(k) + '=\'' + str(v) + '\';'

    string += '>'
    
    # Check if enclosing tag
    # If there is an enclosing tag, we can add the contents and the enclosing tag
    # Else, we return as is
    if enclose:
        string += content
        string += '</' + tag + '>'

    return string


def build_notification(success='success', tag='', message=''):
    """
    A function making use of the build_html() function to generate notifications.
    This function is hard-coded based on the values in style.css.

    Parameters
    ----------
    success (str)
        Either 'success', 'warning', or 'error'. The appropriate CSS style will be used.
    tag(str)
        The content of the tag, eg. '[INFO]', '[ERROR]', etc.
    message (str)
        The message to be printed out after the tag.

    Returns
    -------
    string (str)
        The HTML notification, encased in a <div>
    """
    notification_type = ''

    if success == 'success':
        notification_type = 'notification-success'
    elif success == 'warning':
        notification_type = 'notification-warning'
    elif success == 'error':
        notification_type = 'notification-error'

    return build_html('div', content=''.join([
        build_html('label', attr={'class': notification_type}, content=tag),
        ' ',
        message
    ])).strip()