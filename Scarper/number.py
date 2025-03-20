import re
given_string='or job information call the given number +91-9582381585 We are hiring for Computer Operator and Back Office and Cashier and Data Entry Job Location All Pan India 12 Pass, Graduation, Any Graduation and Any SkillsnCall the given number and apply for the job +91-9582381585'
pattern='\\b[6789]\\d{9}\\b'
number=re.findall(pattern,given_string)
print(number)