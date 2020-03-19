# This file stores the functions to convert Python objects to a format that can be displayed via HTML.

def dataframe_to_table(dataframe):
    """
    Converts a Pandas dataframe to a HTML table.

    Parameters
    ----------
    dataframe (DataFrame())
        The Pandas dataframe to be converted into a HTML table. 

    Returns
    -------
    html (str)
        The HTML table to be rendered. 
    """
    html = ''

    html += '<table>'

    html += '<tbody>'

    rows, cols = dataframe.shape
    
    # Headers
    html += '<td>'

    for col in range(cols):
        html += '<td>'

        html += str(dataframe.columns[col])

        html += '</td>'

    html += '</tr>'

    # Data
    for row in range(rows):
        html += '<tr>'

        for col in range(cols): 
            html += '<td>'

            html += str(dataframe.iloc[row, col])

            html += '</td>'

        html += '</tr>'

    html += '</tbody>'

    html += '</table>'

    return html 