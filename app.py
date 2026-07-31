import streamlit as st
import pandas as pd
import numpy as np
import pickle

lr = pickle.load(open('Logistic_Regression.pkl','rb'))
dt = pickle.load(open('Decision_Tree.pkl','rb'))
rf = pickle.load(open('Random_Forest.pkl','rb'))
#knn = pickle.load(open('knn.pkl','rb'))


model = st.sidebar.selectbox('Select the Model',['Decision Tree','Random Forest',
                                                 'Logistic Regression'])

st.header('Smart Inventory Risk Prediction')

col1,col2,col3 = st.columns(3)

with col1:
    current_stock = st.slider('Current Stock', min_value=0, max_value=3500)
    reorder_point = st.slider('Reorder Point', min_value=0, max_value=3000)
    safety_stock = st.slider('Safety Stock', min_value=0, max_value=1100)
    lead_time_days = st.slider('Lead Time Days', min_value=1, max_value=15)
    units_sold = st.slider('Units Sold', min_value=0, max_value=300)
    unit_price = st.slider('Unit Price', min_value=0, max_value=1500)
    supplier_reliability = st.slider('Supplier Reliability', min_value=0, max_value=1)

with col2:
    days_of_supply = st.slider('Days of Supply', min_value=0, max_value=40)
    is_reorder_needed = st.selectbox('Is Reorder Needed', [0, 1])
    stock_buffer = st.slider('Stock Buffer', min_value=-350, max_value=2500)
    month = st.selectbox('Month', list(range(1, 13)))
    day_of_week = st.selectbox('Day of Week', list(range(0, 7)))
    is_weekend = st.selectbox('Is Weekend', [0, 1])

with col3:
   risk_score = st.slider('Risk Score', min_value=0, max_value=100)
   category = st.selectbox('Category', ['Electronics', 'Fashion', 'Grocery', 'Beauty','Home & Kitchen',
       'Office Supplies', 'Sports', 'Toys'])
   warehouse = st.selectbox('Warehouse', ['WH002', 'WH003', 'WH004', 'WH005'])
   promotion = st.selectbox('Promotion', ['Yes', 'No'])
   holiday = st.selectbox('Holiday', ['Yes', 'No'])
   season = st.selectbox('Season', ['Monsoon', 'Summer', 'Winter'])

if category == 'Electronics':
    category_electronics = 1
    category_fashion = 0
    category_grocery = 0
    category_home_kitchen = 0
    category_office_supplies = 0
    category_sports = 0
    category_toys = 0
elif category == 'Fashion':
    category_electronics = 0
    category_fashion = 1
    category_grocery = 0
    category_home_kitchen = 0
    category_office_supplies = 0
    category_sports = 0
    category_toys = 0
elif category == 'Grocery':
    category_electronics = 0
    category_fashion = 0
    category_grocery = 1
    category_home_kitchen = 0
    category_office_supplies = 0
    category_sports = 0
    category_toys = 0
elif category == 'Home & Kitchen':
    category_electronics = 0
    category_fashion = 0
    category_grocery = 0
    category_home_kitchen = 1
    category_office_supplies = 0
    category_sports = 0
    category_toys = 0
elif category == 'Office Supplies':
    category_electronics = 0
    category_fashion = 0
    category_grocery = 0
    category_home_kitchen = 0
    category_office_supplies = 1
    category_sports = 0
    category_toys = 0
elif category == 'Sports':
    category_electronics = 0
    category_fashion = 0
    category_grocery = 0
    category_home_kitchen = 0
    category_office_supplies = 0
    category_sports = 1
    category_toys = 0
else:
    category_electronics = 0
    category_fashion = 0
    category_grocery = 0
    category_home_kitchen = 0
    category_office_supplies = 0
    category_sports = 0
    category_toys = 1



if warehouse == 'WH002':
    warehouse_wh002 = 1
    warehouse_wh003 = 0
    warehouse_wh004 = 0
    warehouse_wh005 = 0
elif warehouse == 'WH003':
    warehouse_wh002 = 0
    warehouse_wh003 = 1
    warehouse_wh004 = 0
    warehouse_wh005 = 0
elif warehouse == 'WH004':
    warehouse_wh002 = 0
    warehouse_wh003 = 0
    warehouse_wh004 = 1
    warehouse_wh005 = 0
else:
    warehouse_wh002 = 0
    warehouse_wh003 = 0
    warehouse_wh004 = 0
    warehouse_wh005 = 1


if promotion == 'Yes':
    promotion_yes = 1
    promotion_no = 0
else:
    promotion_yes = 0
    promotion_no = 1

if holiday == 'Yes':
    holiday_yes = 1
    holiday_no = 0
else:
    holiday_yes = 0
    holiday_no = 1

if season == 'Monsoon':
    season_monsoon = 1
    season_summer = 0
    season_winter = 0
elif season == 'Summer':
    season_monsoon = 0
    season_summer = 1
    season_winter = 0
else:
    season_monsoon = 0
    season_summer = 0
    season_winter = 1


test = np.array([current_stock, reorder_point, safety_stock, lead_time_days,
                 units_sold, unit_price, supplier_reliability, days_of_supply,
                 is_reorder_needed, stock_buffer, month, day_of_week,
                 is_weekend, risk_score, category_electronics, category_fashion,
                 category_grocery, category_home_kitchen, category_office_supplies,
                 category_sports, category_toys, warehouse_wh002, warehouse_wh003,
                 warehouse_wh004, warehouse_wh005, promotion_yes,
                 holiday_yes, season_monsoon, season_summer, season_winter])

test_data = np.array(test).reshape(1,30)
test_df = pd.DataFrame(test_data, columns=['Current_Stock', 'Reorder_Point', 'Safety_Stock', 'Lead_Time_Days',
       'Units_Sold', 'Unit_Price', 'Supplier_Reliability', 'Days_of_Supply',
       'Is_Reorder_Needed', 'Stock_Buffer', 'Month', 'DayOfWeek',
       'Is_Weekend', 'Risk_Score', 'Category_Electronics', 'Category_Fashion',
       'Category_Grocery', 'Category_Home & Kitchen',
       'Category_Office Supplies', 'Category_Sports', 'Category_Toys',
       'Warehouse_WH002', 'Warehouse_WH003', 'Warehouse_WH004',
       'Warehouse_WH005', 'Promotion_Yes', 'Holiday_Yes', 'Season_Monsoon',
       'Season_Summer', 'Season_Winter'])

st.write(test_df)

predict_button = st.button('Predict Inventory Risk')

risk_labels = {
    0: "High Risk",
    1: "Low Risk",
    2: "Medium Risk"
}

if predict_button:
    if model == 'Decision Tree':
        raw_pred = dt.predict(test_df)[0]
        readable_pred = risk_labels.get(raw_pred, "Unknown Risk Level")
        st.success(f"Predicted Risk Level: {readable_pred}")

    elif model == 'Random Forest':
         raw_pred = rf.predict(test_df)[0]
         readable_pred = risk_labels.get(raw_pred, "Unknown Risk Level")
         st.success(f"Predicted Risk Level: {readable_pred}")

    elif model == 'Logistic Regression':
        raw_pred = lr.predict(test_df)[0]
        readable_pred = risk_labels.get(raw_pred, "Unknown Risk Level")
        st.success(f"Predicted Risk Level: {readable_pred}")



