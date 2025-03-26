from table import draw_table

def test_table_format():
    expected = '''
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
'''.strip()
    


    fields = ["Name", "Code", "Country", "Employees", "CEO Name", "CEO Year Born"]
    data = [["Pfizer Inc.", "PFE", "United States", 78500, "Dr. Albert Bourla D.V.M., DVM, Ph.D.", 1962]]
    title = ' 5 stocks with most youngest CEOs '
    assert draw_table(fields, data, title) == expected


from request import request

def test_requst_caching():
    url = "http://www.randomnumberapi.com/api/v1.0/random?min=100&max=1000"
    resp = request(url)
    assert resp.status_code == 200
    resp2 = request(url)
    assert resp.status_code == 200

    assert resp.text == resp2.text