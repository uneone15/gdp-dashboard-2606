import streamlit as st
import pandas as pd
import math
from pathlib import Path

st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:',
)

# -----------------------------------------------------------------------------
# Region mapping (World Bank classification)

REGION_MAP = {
    # East Asia & Pacific
    'AUS':'East Asia & Pacific','BRN':'East Asia & Pacific','CHN':'East Asia & Pacific',
    'FJI':'East Asia & Pacific','HKG':'East Asia & Pacific','IDN':'East Asia & Pacific',
    'JPN':'East Asia & Pacific','KHM':'East Asia & Pacific','KIR':'East Asia & Pacific',
    'KOR':'East Asia & Pacific','LAO':'East Asia & Pacific','MAC':'East Asia & Pacific',
    'MHL':'East Asia & Pacific','MMR':'East Asia & Pacific','MNG':'East Asia & Pacific',
    'MYS':'East Asia & Pacific','NRU':'East Asia & Pacific','NZL':'East Asia & Pacific',
    'PHL':'East Asia & Pacific','PLW':'East Asia & Pacific','PNG':'East Asia & Pacific',
    'PRK':'East Asia & Pacific','SGP':'East Asia & Pacific','SLB':'East Asia & Pacific',
    'THA':'East Asia & Pacific','TLS':'East Asia & Pacific','TON':'East Asia & Pacific',
    'TUV':'East Asia & Pacific','TWN':'East Asia & Pacific','VNM':'East Asia & Pacific',
    'VUT':'East Asia & Pacific','WSM':'East Asia & Pacific',
    # Europe & Central Asia
    'ALB':'Europe & Central Asia','AND':'Europe & Central Asia','ARM':'Europe & Central Asia',
    'AUT':'Europe & Central Asia','AZE':'Europe & Central Asia','BEL':'Europe & Central Asia',
    'BGR':'Europe & Central Asia','BIH':'Europe & Central Asia','BLR':'Europe & Central Asia',
    'CHE':'Europe & Central Asia','CYP':'Europe & Central Asia','CZE':'Europe & Central Asia',
    'DEU':'Europe & Central Asia','DNK':'Europe & Central Asia','ESP':'Europe & Central Asia',
    'EST':'Europe & Central Asia','FIN':'Europe & Central Asia','FRA':'Europe & Central Asia',
    'FRO':'Europe & Central Asia','GBR':'Europe & Central Asia','GEO':'Europe & Central Asia',
    'GRC':'Europe & Central Asia','GRL':'Europe & Central Asia','HRV':'Europe & Central Asia',
    'HUN':'Europe & Central Asia','IMN':'Europe & Central Asia','IRL':'Europe & Central Asia',
    'ISL':'Europe & Central Asia','ITA':'Europe & Central Asia','KAZ':'Europe & Central Asia',
    'KGZ':'Europe & Central Asia','LIE':'Europe & Central Asia','LTU':'Europe & Central Asia',
    'LUX':'Europe & Central Asia','LVA':'Europe & Central Asia','MCO':'Europe & Central Asia',
    'MDA':'Europe & Central Asia','MKD':'Europe & Central Asia','MNE':'Europe & Central Asia',
    'NLD':'Europe & Central Asia','NOR':'Europe & Central Asia','POL':'Europe & Central Asia',
    'PRT':'Europe & Central Asia','ROU':'Europe & Central Asia','RUS':'Europe & Central Asia',
    'SMR':'Europe & Central Asia','SRB':'Europe & Central Asia','SVK':'Europe & Central Asia',
    'SVN':'Europe & Central Asia','SWE':'Europe & Central Asia','TJK':'Europe & Central Asia',
    'TKM':'Europe & Central Asia','TUR':'Europe & Central Asia','UKR':'Europe & Central Asia',
    'UZB':'Europe & Central Asia','XKX':'Europe & Central Asia',
    # Latin America & Caribbean
    'ARG':'Latin America & Caribbean','ATG':'Latin America & Caribbean',
    'BHS':'Latin America & Caribbean','BLZ':'Latin America & Caribbean',
    'BOL':'Latin America & Caribbean','BRA':'Latin America & Caribbean',
    'BRB':'Latin America & Caribbean','CHL':'Latin America & Caribbean',
    'COL':'Latin America & Caribbean','CRI':'Latin America & Caribbean',
    'CUB':'Latin America & Caribbean','DMA':'Latin America & Caribbean',
    'DOM':'Latin America & Caribbean','ECU':'Latin America & Caribbean',
    'GRD':'Latin America & Caribbean','GTM':'Latin America & Caribbean',
    'GUY':'Latin America & Caribbean','HND':'Latin America & Caribbean',
    'HTI':'Latin America & Caribbean','JAM':'Latin America & Caribbean',
    'KNA':'Latin America & Caribbean','LCA':'Latin America & Caribbean',
    'MEX':'Latin America & Caribbean','NIC':'Latin America & Caribbean',
    'PAN':'Latin America & Caribbean','PER':'Latin America & Caribbean',
    'PRY':'Latin America & Caribbean','SLV':'Latin America & Caribbean',
    'SUR':'Latin America & Caribbean','TCA':'Latin America & Caribbean',
    'TTO':'Latin America & Caribbean','URY':'Latin America & Caribbean',
    'VCT':'Latin America & Caribbean','VEN':'Latin America & Caribbean',
    # Middle East & North Africa
    'ARE':'Middle East & North Africa','BHR':'Middle East & North Africa',
    'DJI':'Middle East & North Africa','DZA':'Middle East & North Africa',
    'EGY':'Middle East & North Africa','IRN':'Middle East & North Africa',
    'IRQ':'Middle East & North Africa','ISR':'Middle East & North Africa',
    'JOR':'Middle East & North Africa','KWT':'Middle East & North Africa',
    'LBN':'Middle East & North Africa','LBY':'Middle East & North Africa',
    'MAR':'Middle East & North Africa','MLT':'Middle East & North Africa',
    'OMN':'Middle East & North Africa','PSE':'Middle East & North Africa',
    'QAT':'Middle East & North Africa','SAU':'Middle East & North Africa',
    'SYR':'Middle East & North Africa','TUN':'Middle East & North Africa',
    'YEM':'Middle East & North Africa',
    # North America
    'BMU':'North America','CAN':'North America','USA':'North America',
    # South Asia
    'AFG':'South Asia','BGD':'South Asia','BTN':'South Asia','IND':'South Asia',
    'LKA':'South Asia','MDV':'South Asia','NPL':'South Asia','PAK':'South Asia',
    # Sub-Saharan Africa
    'AGO':'Sub-Saharan Africa','BDI':'Sub-Saharan Africa','BEN':'Sub-Saharan Africa',
    'BFA':'Sub-Saharan Africa','BWA':'Sub-Saharan Africa','CAF':'Sub-Saharan Africa',
    'CIV':'Sub-Saharan Africa','CMR':'Sub-Saharan Africa','COD':'Sub-Saharan Africa',
    'COG':'Sub-Saharan Africa','COM':'Sub-Saharan Africa','CPV':'Sub-Saharan Africa',
    'ERI':'Sub-Saharan Africa','ETH':'Sub-Saharan Africa','GAB':'Sub-Saharan Africa',
    'GHA':'Sub-Saharan Africa','GIN':'Sub-Saharan Africa','GMB':'Sub-Saharan Africa',
    'GNB':'Sub-Saharan Africa','GNQ':'Sub-Saharan Africa','KEN':'Sub-Saharan Africa',
    'LBR':'Sub-Saharan Africa','LSO':'Sub-Saharan Africa','MDG':'Sub-Saharan Africa',
    'MLI':'Sub-Saharan Africa','MOZ':'Sub-Saharan Africa','MRT':'Sub-Saharan Africa',
    'MUS':'Sub-Saharan Africa','MWI':'Sub-Saharan Africa','NAM':'Sub-Saharan Africa',
    'NER':'Sub-Saharan Africa','NGA':'Sub-Saharan Africa','RWA':'Sub-Saharan Africa',
    'SDN':'Sub-Saharan Africa','SEN':'Sub-Saharan Africa','SLE':'Sub-Saharan Africa',
    'SOM':'Sub-Saharan Africa','SSD':'Sub-Saharan Africa','STP':'Sub-Saharan Africa',
    'SWZ':'Sub-Saharan Africa','SYC':'Sub-Saharan Africa','TCD':'Sub-Saharan Africa',
    'TGO':'Sub-Saharan Africa','TZA':'Sub-Saharan Africa','UGA':'Sub-Saharan Africa',
    'ZAF':'Sub-Saharan Africa','ZMB':'Sub-Saharan Africa','ZWE':'Sub-Saharan Africa',
}

REGIONS = [
    'All Regions',
    'East Asia & Pacific',
    'Europe & Central Asia',
    'Latin America & Caribbean',
    'Middle East & North Africa',
    'North America',
    'South Asia',
    'Sub-Saharan Africa',
]

# -----------------------------------------------------------------------------
# Data loading

@st.cache_data
def get_gdp_data():
    DATA_FILENAME = Path(__file__).parent / 'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    gdp_df = raw_gdp_df.melt(
        ['Country Name', 'Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    gdp_df['GDP'] = pd.to_numeric(gdp_df['GDP'], errors='coerce')
    gdp_df['Region'] = gdp_df['Country Code'].map(REGION_MAP).fillna('Other')
    return gdp_df


gdp_df = get_gdp_data()

# code → name lookup
code_to_name = (
    gdp_df[['Country Code', 'Country Name']]
    .drop_duplicates()
    .set_index('Country Code')['Country Name']
    .to_dict()
)

# -----------------------------------------------------------------------------
# Page header

'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

''
''

# -----------------------------------------------------------------------------
# Filters

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value],
)

# 4. 지역 필터
selected_region = st.selectbox('Filter by region', REGIONS)

if selected_region == 'All Regions':
    region_codes = set(gdp_df['Country Code'].unique())
else:
    region_codes = {c for c, r in REGION_MAP.items() if r == selected_region}

available_codes = sorted(
    [c for c in gdp_df['Country Code'].unique() if c in region_codes],
    key=lambda c: code_to_name.get(c, c),
)

# 1. 국가명 표시: 옵션 레이블을 "Germany (DEU)" 형태로, 기본값도 이름으로
def fmt_option(code):
    name = code_to_name.get(code, code)
    return f'{name} ({code})'

default_codes = [c for c in ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'] if c in available_codes]

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    options=available_codes,
    default=default_codes,
    format_func=fmt_option,
)

if not selected_countries:
    st.warning('Select at least one country')
    st.stop()

# 3. GDP 단위 선택
unit = st.radio(
    'GDP unit',
    ['Trillion (T)', 'Billion (B)', 'Million (M)'],
    index=1,
    horizontal=True,
)

unit_divisor = {'Trillion (T)': 1e12, 'Billion (B)': 1e9, 'Million (M)': 1e6}[unit]
unit_label   = {'Trillion (T)': 'T',  'Billion (B)': 'B',  'Million (M)': 'M'}[unit]

''
''

# -----------------------------------------------------------------------------
# Filter data

filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
].copy()

filtered_gdp_df['GDP_display'] = filtered_gdp_df['GDP'] / unit_divisor

# 2. 데이터 누락 경고
missing = (
    filtered_gdp_df.groupby('Country Code')['GDP']
    .apply(lambda s: s.isna().sum())
)
missing = missing[missing > 0]
if not missing.empty:
    parts = [f'{fmt_option(c)} → {n}yr missing' for c, n in missing.items()]
    st.warning('Missing data: ' + ' / '.join(parts))

# -----------------------------------------------------------------------------
# Line chart

st.header('GDP over time', divider='gray')

''

st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP_display',
    color='Country Code',
)

st.caption(f'Unit: USD {unit_label}')

''
''

# -----------------------------------------------------------------------------
# Metric cards

first_year_df = gdp_df[gdp_df['Year'] == from_year]
last_year_df  = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_row = first_year_df[first_year_df['Country Code'] == country]['GDP']
        last_row  = last_year_df[last_year_df['Country Code'] == country]['GDP']

        # 2. 누락 데이터 안전 처리
        first_val = first_row.iat[0] if len(first_row) else float('nan')
        last_val  = last_row.iat[0]  if len(last_row)  else float('nan')

        label = fmt_option(country)
        last_display = last_val / unit_divisor if not math.isnan(last_val) else float('nan')

        if math.isnan(last_display):
            st.metric(label=label, value='n/a')
            continue

        if math.isnan(first_val) or first_val == 0:
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_val / first_val:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=label,
            value=f'{last_display:,.1f}{unit_label}',
            delta=growth,
            delta_color=delta_color,
        )
