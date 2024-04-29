import streamlit as st
import base64
import pandas as pd
import numpy as np


@st.cache_data
def read_onedrive_csv (onedrive_link):
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    df=pd.read_csv(resultUrl)
    return df

df=read_onedrive_csv('https://1drv.ms/u/s!Agfa0F4-51Tw_mQSgIgtlQQJlQg_?e=YpfpZo')
df['province_id'] = df['sbd'].astype(str).str[-8:-6]
province_list = """
1 - THÀNH PHỐ HÀ NỘI
2 - THÀNH PHỐ HỒ CHÍ MINH
3 - THÀNH PHỐ HẢI PHÒNG
4 - THÀNH PHỐ ĐÀ NẴNG
5 - TỈNH HÀ GIANG
6 - TỈNH CAO BẰNG
7 - TỈNH LAI CHÂU
8 - TỈNH LÀO CAI
9 - TỈNH TUYÊN QUANG
10 - TỈNH LẠNG SƠN
11 - TỈNH BẮC KẠN
12 - TỈNH THÁI NGUYÊN
13 - TỈNH YÊN BÁI
14 - TỈNH SƠN LA
15 - TỈNH PHÚ THỌ
16 - TỈNH VĨNH PHÚC
17 - TỈNH QUẢNG NINH
18 - TỈNH BẮC GIANG
19 - TỈNH BẮC NINH
21 - TỈNH HẢI DƯƠNG
22 - TỈNH HƯNG YÊN
23 - TỈNH HÒA BÌNH
24 - TỈNH HÀ NAM
25 - TỈNH NAM ĐỊNH
26 - TỈNH THÁI BÌNH
27 - TỈNH NINH BÌNH
28 - TỈNH THANH HÓA
29 - TỈNH NGHỆ AN
30 - TỈNH HÀ TĨNH
31 - TỈNH QUẢNG BÌNH
32 - TỈNH QUẢNG TRỊ
33 - TỈNH THỪA THIÊN - HUẾ
34 - TỈNH QUẢNG NAM
35 - TỈNH QUẢNG NGÃI
36 - TỈNH KON TUM
37 - TỈNH BÌNH ĐỊNH
38 - TỈNH GIA LAI
39 - TỈNH PHÚ YÊN
40 - TỈNH ĐẮK LẮK
41 - TỈNH KHÁNH HÒA
42 - TỈNH LÂM ĐỒNG
43 - TỈNH BÌNH PHƯỚC
44 - TỈNH BÌNH DƯƠNG
45 - TỈNH NINH THUẬN
46 - TỈNH TÂY NINH
47 - TỈNH BÌNH THUẬN
48 - TỈNH ĐỒNG NAI
49 - TỈNH LONG AN
50 - TỈNH ĐỒNG THÁP
51 - TỈNH AN GIANG
52 - TỈNH BÀ RỊA - VŨNG TÀU
53 - TỈNH TIỀN GIANG
54 - TỈNH KIÊN GIANG
55 - THÀNH PHỐ CẦN THƠ
56 - TỈNH BẾN TRE
57 - TỈNH VĨNH LONG
58 - TỈNH TRÀ VINH
59 - TỈNH SÓC TRĂNG
60 - TỈNH BẠC LIÊU
61 - TỈNH CÀ MAU
62 - TỈNH ĐIỆN BIÊN
63 - TỈNH ĐĂK NÔNG
64 - TỈNH HẬU GIANG
"""

st.write("Dataset Điểm thi THPT Quốc gia 2023: https://1drv.ms/u/s!Agfa0F4-51Tw_mQSgIgtlQQJlQg_?e=YpfpZo")

# Process the input text to create a dictionary
province_lines = province_list.strip().split("\n")
province_dict = {line.split(" - ")[0].strip(): line.split(" - ")[1].strip() for line in province_lines}

# Map the province_id to province names
df['province_name'] = df['province_id'].map(province_dict)

# Assuming df is your DataFrame
subjects = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_li', 'hoa_hoc', 'sinh_hoc', 'lich_su', 'dia_li', 'gdcd']

# Replace NaN with -inf to ensure they are ignored in the top 3 calculation
scores_df = df[subjects].replace(np.nan, np.NINF)

# Use numpy to sort (while ignoring NaNs) and sum the top 3 scores for each row
df['highest_score'] = np.sort(scores_df.values, axis=1)[:, -3:].sum(axis=1)

# Replace any -inf back to NaN in the original DataFrame if necessary
df[subjects] = df[subjects].replace(np.NINF, np.nan)

# Calculate the top 1% threshold
top_1_percent_threshold = df['highest_score'].quantile(0.99)

# Filter the top 1% students
top_1_percent_students = df[df['highest_score'] >= top_1_percent_threshold]

# Count the number of top 1% students by province
top_1_percent_by_province = top_1_percent_students['province_name'].value_counts()

# Convert counts to DataFrame for further manipulation
top_1_percent_by_province_df = pd.DataFrame(top_1_percent_by_province).reset_index()
top_1_percent_by_province_df.columns = ['Province', 'Top 1% Count']

# Calculate the total number of top 1% students
total_top_1_percent_students = top_1_percent_by_province_df['Top 1% Count'].sum()

# Calculate percentages and round to 0 decimal places, then convert to integer for no decimal display
top_1_percent_by_province_df['Percentage of Total Top 1%'] = ((top_1_percent_by_province_df['Top 1% Count'] / total_top_1_percent_students) * 100).round(2)

# Display the top 1 provinces based on the number of top 1% students
top_10_provinces = top_1_percent_by_province_df.head(10)

st.header("Top 10 Tỉnh có học sinh thuộc top 1%")
st.write(top_10_provinces)



with st.expander("View the code"):
    code1 = """
import streamlit as st
import base64
import pandas as pd
import numpy as np


@st.cache_data
def read_onedrive_csv (onedrive_link):
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    df=pd.read_csv(resultUrl)
    return df



df=read_onedrive_csv('https://1drv.ms/u/s!Agfa0F4-51Tw_mQSgIgtlQQJlQg_?e=YpfpZo')
df['province_id'] = df['sbd'].astype(str).str[-8:-6]"""
    code2="""
province_list = \'''
1 - THÀNH PHỐ HÀ NỘI
2 - THÀNH PHỐ HỒ CHÍ MINH
3 - THÀNH PHỐ HẢI PHÒNG
4 - THÀNH PHỐ ĐÀ NẴNG
5 - TỈNH HÀ GIANG
6 - TỈNH CAO BẰNG
7 - TỈNH LAI CHÂU
8 - TỈNH LÀO CAI
9 - TỈNH TUYÊN QUANG
10 - TỈNH LẠNG SƠN
11 - TỈNH BẮC KẠN
12 - TỈNH THÁI NGUYÊN
13 - TỈNH YÊN BÁI
14 - TỈNH SƠN LA
15 - TỈNH PHÚ THỌ
16 - TỈNH VĨNH PHÚC
17 - TỈNH QUẢNG NINH
18 - TỈNH BẮC GIANG
19 - TỈNH BẮC NINH
21 - TỈNH HẢI DƯƠNG
22 - TỈNH HƯNG YÊN
23 - TỈNH HÒA BÌNH
24 - TỈNH HÀ NAM
25 - TỈNH NAM ĐỊNH
26 - TỈNH THÁI BÌNH
27 - TỈNH NINH BÌNH
28 - TỈNH THANH HÓA
29 - TỈNH NGHỆ AN
30 - TỈNH HÀ TĨNH
31 - TỈNH QUẢNG BÌNH
32 - TỈNH QUẢNG TRỊ
33 - TỈNH THỪA THIÊN - HUẾ
34 - TỈNH QUẢNG NAM
35 - TỈNH QUẢNG NGÃI
36 - TỈNH KON TUM
37 - TỈNH BÌNH ĐỊNH
38 - TỈNH GIA LAI
39 - TỈNH PHÚ YÊN
40 - TỈNH ĐẮK LẮK
41 - TỈNH KHÁNH HÒA
42 - TỈNH LÂM ĐỒNG
43 - TỈNH BÌNH PHƯỚC
44 - TỈNH BÌNH DƯƠNG
45 - TỈNH NINH THUẬN
46 - TỈNH TÂY NINH
47 - TỈNH BÌNH THUẬN
48 - TỈNH ĐỒNG NAI
49 - TỈNH LONG AN
50 - TỈNH ĐỒNG THÁP
51 - TỈNH AN GIANG
52 - TỈNH BÀ RỊA - VŨNG TÀU
53 - TỈNH TIỀN GIANG
54 - TỈNH KIÊN GIANG
55 - THÀNH PHỐ CẦN THƠ
56 - TỈNH BẾN TRE
57 - TỈNH VĨNH LONG
58 - TỈNH TRÀ VINH
59 - TỈNH SÓC TRĂNG
60 - TỈNH BẠC LIÊU
61 - TỈNH CÀ MAU
62 - TỈNH ĐIỆN BIÊN
63 - TỈNH ĐĂK NÔNG
64 - TỈNH HẬU GIANG
'''"""
    code3="""
st.write("Dataset Điểm thi THPT Quốc gia 2023: https://1drv.ms/u/s!Agfa0F4-51Tw_mQSgIgtlQQJlQg_?e=YpfpZo")

# Process the input text to create a dictionary
province_lines = province_list.strip().split("\n")
province_dict = {line.split(" - ")[0].strip(): line.split(" - ")[1].strip() for line in province_lines}

# Map the province_id to province names
df['province_name'] = df['province_id'].map(province_dict)

# Assuming df is your DataFrame
subjects = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_li', 'hoa_hoc', 'sinh_hoc', 'lich_su', 'dia_li', 'gdcd']

# Replace NaN with -inf to ensure they are ignored in the top 3 calculation
scores_df = df[subjects].replace(np.nan, np.NINF)

# Use numpy to sort (while ignoring NaNs) and sum the top 3 scores for each row
df['highest_score'] = np.sort(scores_df.values, axis=1)[:, -3:].sum(axis=1)

# Replace any -inf back to NaN in the original DataFrame if necessary
df[subjects] = df[subjects].replace(np.NINF, np.nan)

# Calculate the top 1% threshold
top_1_percent_threshold = df['highest_score'].quantile(0.99)

# Filter the top 1% students
top_1_percent_students = df[df['highest_score'] >= top_1_percent_threshold]

# Count the number of top 1% students by province
top_1_percent_by_province = top_1_percent_students['province_name'].value_counts()

# Convert counts to DataFrame for further manipulation
top_1_percent_by_province_df = pd.DataFrame(top_10_percent_by_province).reset_index()
top_1_percent_by_province_df.columns = ['Province', 'Top 1% Count']

# Calculate the total number of top 1% students
total_top_1_percent_students = top_1_percent_by_province_df['Top 1% Count'].sum()

# Calculate percentages and round to 0 decimal places, then convert to integer for no decimal display
top_1_percent_by_province_df['Percentage of Total Top 1%'] = ((top_1_percent_by_province_df['top 1% Count'] / total_top_10_percent_students) * 100).round(2)

# Display the top 1 provinces based on the number of top 1% students
top_10_provinces = top_1_percent_by_province_df.head(10)

st.header("top 1 Tỉnh có học sinh thuộc top 1%")
st.write(top_10_provinces)
"""
    st.code(code1, language='python')
    st.code(code2, language='python')
    st.code(code3, language='python')