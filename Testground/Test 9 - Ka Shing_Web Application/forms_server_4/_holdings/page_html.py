# === Imports ===
from flask import Flask, render_template

# === HTML Home Page ===
class Home():
    """
    A class to handle the HTML elements on the home page.
    """
    def __init__(self, inputs):
        """
        Constructor class.
        Instantiates the number of inputs during data requests.

        Parameters
        ----------
        inputs = {}[]
            key: id (str)
            value: description (str)
        """
        self.inputs = inputs
        

    def reload(self):
        """
        Reloads the page to its default value.
        """
        # === Head ===
        # No arguments required
        self.head = None  

        # === Upload bar ===
        # No arguments required
        self.upload = None 

        # === Notification bar ===
        self.notifications = []

        # === Data Request ===
        self.sessions = []

        # === Metric Display ===
        self.metric_display = []


    def update_notification(self, **kwargs): 
        """ 
        Appends the given message to the list of existing notifications.

        Parameters
        ----------
        **kwargs
            success(str)
                Either 'success', 'warning', or 'error'. The appropriate CSS style will be used.
            color (str)
                Color of the tag
            tag(str)
                The content of the tag, eg. '[INFO]', '[ERROR]', etc.
            msg (str)
                The message to be printed out after the tag.
        """
        try:
            success = kwargs["success"]

            if success == "success":
                color = "green"
                tag = "[SUCCESS]"
            elif success == "warning":
                color = "orange"
                tag = "[WARNING]"
            elif success == "error":
                color = "red"
                tag = "[ERROR]"
        except KeyError:
            success = ""

        if not success: 
            try:
                color = kwargs["color"]
            except KeyError:
                color = ""

            try:
                tag = kwargs["tag"]
            except KeyError:
                tag = ""

        try:
            message = kwargs["msg"]
        except KeyError:
            message = ""

        self.notifications.append({
            "color": color,
            "tag": tag,
            "msg": message
        })


    def update_data_requests(self, index, name, descriptions=[], inputs={}):
        """
        Updates the data requests form section.

        Parameters
        ----------
        index (int)
            Session index
        name (str)
            Session name
        description (str[])
            A list of descriptions for the session
        inputs ({}[])
            An array of dictionaries. 
            Each dictionary contains the input-default value pair. 
        """
        # defaults = {}
        # for i in self.inputs:
        #     try:
        #         defaults[i] = defaults[i]
        #     except KeyError:
        #         defaults[i] = ''
        
        # self.sessions.append({
        #     "session_name": session_name,
        #     "index": index,
        #     "additional_info": add_info,
        #     "defaults": defaults,
        # })
        
        self.sessions.append({
            "index": index,
            "name": name,
            "descriptions": descriptions,
            "inputs": inputs
        })


    def render(self):
        """
        Returns the collection of HTML.

        Returns
        -------
        html (str)
            The HTML page element.
        """
        html = ''

        # === Head ===
        html += render_template('head.html')

        # === Upload bar ===
        html += render_template('home_page/upload.html')

        # === Notifications bar === 
        if self.notifications:
            html += '<hr>'
            html += render_template(
                'home_page/notifications.html',
                num=len(self.notifications),
                colors=[t["color"] for t in self.notifications],
                tags=[t["tag"] for t in self.notifications],
                msgs=[t["msg"] for t in self.notifications]
            )

        # # === Data requests ===
        # if self.sessions:
        #     # print([t["defaults"] for t in self.sessions])
        #     html += '<hr>'
        #     html += render_template(
        #         "home_page/data-requests.html",
        #         indexes=[t["index"] for t in self.sessions],
        #         rows=len(self.sessions),
        #         session_names=[t["session_name"] for t in self.sessions],
        #         additional=[t["additional_info"] for t in self.sessions],
        #         inputs=self.inputs,
        #         descriptions=self.descriptions,
        #         defaults=[t["defaults"] for t in self.sessions]
        #     )

        # === Data requests ===
        if self.sessions:
            html += '<hr>'
            html += render_template(
                "home_page/data-requests.html",
                headers=self.inputs,
                sessions=self.sessions
            )

            print(self.sessions)

            # input_ids = []

            # for i in range(len(self.sessions)):
            #     columns_of_inputs = []

            #     for j in range(len(self.descriptions)):
            #         columns_of_inputs.append('-'.join([self.inputs[j], str(i)]))

            #     input_ids.append(columns_of_inputs)                    

            # # print([t["defaults"] for t in self.sessions])
            # html += '<hr>'
            # html += render_template(
            #     "home_page/data-requests.html",
            #     indexes=[t["index"] for t in self.sessions],
            #     rows=len(self.sessions),
            #     session_names=[t["session_name"] for t in self.sessions],
            #     additional=[t["additional_info"] for t in self.sessions],
            #     input_id=input_ids,
            #     descriptions=self.descriptions, 
            #     defaults=[t["defaults"] for t in self.sessions]
            # )

            # print('DEFAULTS:', [t["defaults"] for t in self.sessions])


        # html = ''

        # html += self.head
        # html += self.upload
        # if self.notifications != '':
        #     html += '<hr>'
        #     html += self.notifications
        # # html += '<hr>'
        # # html += self.data_request
        # # html += '<hr>'
        # # html += self.metric_display

        return html


    @staticmethod
    def post_files(request):
        """
        Extracts the files from the request passed.
        
        Parameters
        ----------
        request

        Returns
        -------
        (FileStorage[])
        """
        return request.files.getlist("files")


    @staticmethod
    def post_form(request):
        """
        Extracts the parameters within the form and compiles it to one string per session.
        Then, returns the array of strings. 

        Parameters
        ----------
        request

        Returns
        -------
        (dictionary array, {}[])
            key: "index" (str)
                 
        """
        # Instantiate form data
        # Dictionary array
        form_data = {}

        # print(':: Request form:', request.form)

        for k, v in request.form.items():
            # Split key into index-test_id
            key = k.split('-', maxsplit=1)

            index = int(key[0])
            test_id = key[1]
            test_value = v 

            try:
                form_data[index].append({
                    "test_id": test_id,
                    "test_value": test_value
                })
            except KeyError:
                form_data[index] = [{
                    "test_id": test_id,
                    "test_value": test_value
                }]

        return form_data

#     def reload(self):
#         """
#         Reloads the page to its default value.
#         """
#         # === Head ===
#         self.head = render_template('head.html')

#         # === Upload bar ===
#         # The upload bar is always present
#         self.upload = render_template('home_page/upload/upload.html')

#         # === Notification bar ===
#         # The notification bar is empty and needs to be populated
#         self.notifications = ""

#         # === Data Request ===
#         # The data request forms are empty and need to be initialized.
#         self.data_request = ""

#         # === Metric Display ===
#         # The metric display is empty and needs to be initialized
#         self.metric_display = ""


#     def update_notification(self, msg, **kwargs):
#         """
#         Appends the given message 'msg' to the list of existing notifications.

#         Parameters
#         ----------
#         msg (str)
#             The message to be printed out after the tag.
#         **kwargs
#             success (str)
#                 Either 'success', 'warning', or 'error'. The appropriate CSS style will be used.
#             tag(str)
#                 The content of the tag, eg. '[INFO]', '[ERROR]', etc.
#         """
#         try:
#             success = kwargs["success"]
            
#             if success == 'success':
#                 notification_type = 'notification-success'
#                 tag = '[SUCCESS]'
#             elif success == 'warning':
#                 notification_type = 'notification-warning'
#                 tag = '[WARNING]'
#             elif success == 'error':
#                 notification_type = 'notification-error'
#                 tag = '[ERROR]'
#             else:
#                 notification_type = ''
#                 tag = ''

#         except KeyError:
#             # 'success' is unused'
#             notification_type = ''
#             tag = ''

#         try:
#             tag = kwargs["tag"]
#         except KeyError:
#             # Don't replace 'tag'
#             True

#         if self.notifications != '':
#             # Add a line break if it's not the first notification
#             self.notifications += '<br>'

#         self.notifications += render_template(
#             'home_page/notifications/notification.html',
#             notification_type=notification_type,
#             tag=tag,
#             msg=msg
#         )

#     def render(self):
#         """
#         Returns the collection of HTML.

#         Returns
#         -------
#         html (str)
#             The HTML page element.
#         """
#         html = ''

#         html += self.head
#         html += self.upload
#         if self.notifications != '':
#             html += '<hr>'
#             html += self.notifications
#         # html += '<hr>'
#         # html += self.data_request
#         # html += '<hr>'
#         # html += self.metric_display

#         return html


# # === HTML Functions ===
# def build_html(tag, attr=None, content='', enclose=True):
#     """
#     Generates a html tag with the given attributes, enclosing the desired content. 
#     Contents are only added if the tag is enclosed. Otherwise, it is dropped. 

#     Parameters
#     ----------
#     tag (str)
#         The HTML tag
#     attr (dictionary, {})
#         Dictionary containing the attributes and their values
#         Each key is the attribute
#         Each value is the corresponding attribute's value
#         Both keys and values are cast to strings
#         e.g. a key-value pair of 'class': 'test' will be generated as 'class'='test'
#     content (str)
#         The content that goes between the opening and closing tags.
#     enclose (boolean)
#         Whether an enclosing tag should be added. 

#     Result
#     ------
#     string (str)
#         HTML string
#     """
#     string = '' # HTML string

#     # Opening tag
#     string += '<' + tag

#     # Add attributes
#     if attr is not None: 
#         for k, v in attr.items():
#             string += ' ' + str(k) + '=\'' + str(v) + '\';'

#     string += '>'
    
#     # Check if enclosing tag
#     # If there is an enclosing tag, we can add the contents and the enclosing tag
#     # Else, we return as is
#     if enclose:
#         string += content
#         string += '</' + tag + '>'

#     return string

