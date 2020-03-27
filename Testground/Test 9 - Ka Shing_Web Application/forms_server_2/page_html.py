# === Imports ===
from flask import Flask, render_template

# === HTML Home Page ===
class Home():
    """
    A class to handle the HTML elements on the home page.
    """
    def reload(self):
        """
        Reloads the page to its default value.
        """
        # === Head ===
        self.head = render_template('head.html')

        # === Upload bar ===
        # The upload bar is always present
        self.upload = render_template('home_page/upload/upload.html')

        # === Notification bar ===
        # The notification bar is empty and needs to be populated
        self.notifications = ""

        # === Data Request ===
        # The data request forms are empty and need to be initialized.
        self.data_request = ""

        # === Metric Display ===
        # The metric display is empty and needs to be initialized
        self.metric_display = ""


    def update_notification(self, msg, **kwargs):
        """
        Appends the given message 'msg' to the list of existing notifications.

        Parameters
        ----------
        msg (str)
            The message to be printed out after the tag.
        **kwargs
            success (str)
                Either 'success', 'warning', or 'error'. The appropriate CSS style will be used.
            tag(str)
                The content of the tag, eg. '[INFO]', '[ERROR]', etc.
        """
        try:
            success = kwargs["success"]
            
            if success == 'success':
                notification_type = 'notification-success'
                tag = '[SUCCESS]'
            elif success == 'warning':
                notification_type = 'notification-warning'
                tag = '[WARNING]'
            elif success == 'error':
                notification_type = 'notification-error'
                tag = '[ERROR]'
            else:
                notification_type = ''
                tag = ''

        except KeyError:
            # 'success' is unused'
            notification_type = ''
            tag = ''

        try:
            tag = kwargs["tag"]
        except KeyError:
            # Don't replace 'tag'
            True

        if self.notifications != '':
            # Add a line break if it's not the first notification
            self.notifications += '<br>'

        self.notifications += render_template(
            'home_page/notifications/notification.html',
            notification_type=notification_type,
            tag=tag,
            msg=msg
        )

    def render(self):
        """
        Returns the collection of HTML.

        Returns
        -------
        html (str)
            The HTML page element.
        """
        html = ''

        html += self.head
        html += self.upload
        if self.notifications != '':
            html += '<hr>'
            html += self.notifications
        # html += '<hr>'
        # html += self.data_request
        # html += '<hr>'
        # html += self.metric_display

        return html


# === HTML Functions ===
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

