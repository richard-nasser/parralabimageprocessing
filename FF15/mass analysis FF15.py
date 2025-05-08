import pandas as pd


ff151l2l = pd.read_xml('FF15A/CellCounter_FF151L2L.xml', engine='python')

print(ff151l2l.shape)