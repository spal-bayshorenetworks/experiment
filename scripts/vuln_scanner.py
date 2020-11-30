#!/usr/bin/env python

import scanner

#target_url = "https://gsagis.pbs.gsa.gov/gsagis/rest"
target_url = "http://testfire.net/"
login_url = "http://testfire.net/login.jsp"
links_to_ignore = ["http://testfire.net/logout.jsp"]

data_dict = {'uid':'admin', 'passw':'admin', 'btnSubmit':'Login'}

vuln_scanner = scanner.Scanner(target_url,links_to_ignore)
vuln_scanner.session.post(login_url,data=data_dict)
vuln_scanner.crawl()
forms = vuln_scanner.extract_forms("http://testfire.net/bank/main.jsp")
print(forms)
response = vuln_scanner.submit_form(forms[0],'testtest',"http://testfire.net/bank/main.jsp")
print(response.content)
vuln_scanner.run_scanner()

