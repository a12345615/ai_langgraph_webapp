import traceback
from grapy import graph_app

try:
    print("Invoking graph_app.invoke with: What is 2+2?")
    out = graph_app.invoke({"user_input":"What is 2+2?","intent":"general","answer":""})
    print("OUT:", out)
except Exception as e:
    print("EXCEPTION:", e)
    traceback.print_exc()
