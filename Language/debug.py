from language import splitter, joiner

code = """
print(12 + 12)
"""

step_1 = splitter.split(code)
step_2 = joiner.rejoin(step_1)

step_2.tokenlist[1].evaluate()